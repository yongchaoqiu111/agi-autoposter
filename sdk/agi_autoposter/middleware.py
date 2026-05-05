#!/usr/bin/env python3
"""
AGI AutoPoster - 审核监督中间层
职责：
  1. 接收调度层指令
  2. 调用执行层 Worker
  3. 接收执行结果
  4. 根据结果判断下一步调度（成功记录/失败重试/超时强杀）
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum
import asyncio
import subprocess
import time
import logging
import os
import signal
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("middleware.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AGI AutoPoster - 审核监督中间层")

class Config:
    MAX_CONCURRENT = 3
    PLATFORM_INTERVAL = 10
    WORKER_TIMEOUT = 120
    MAX_RETRIES = 2
    WORKER_DIR = Path(__file__).parent

config = Config()

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"

class Platform(str, Enum):
    DOUYIN = "douyin"
    FACEBOOK = "facebook"
    KUAISHOU = "kuaishou"
    TIKTOK = "tiktok"
    X = "x"
    INSTAGRAM = "instagram"

class TaskCreate(BaseModel):
    platform: Platform
    txt_id: int
    img_id: int
    max_retries: int = Field(default=2, ge=0, le=5)
    worker_path: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    platform: Platform
    txt_id: int
    img_id: int
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[str] = None
    retry_count: int = 0

task_results: Dict[str, dict] = {}
task_counter = 0
task_queue: asyncio.Queue = asyncio.Queue()

@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    global task_counter
    task_counter += 1
    task_id = f"task_{task_counter:04d}"
    
    task_data = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "platform": task.platform.value,
        "txt_id": task.txt_id,
        "img_id": task.img_id,
        "max_retries": task.max_retries,
        "retry_count": 0,
        "worker_path": task.worker_path,
        "created_at": datetime.now().isoformat()
    }
    
    task_results[task_id] = task_data.copy()
    await task_queue.put(task_data)
    
    return TaskResponse(**task_data)

@app.get("/api/tasks", response_model=List[TaskResponse])
async def list_tasks():
    return [TaskResponse(**t) for t in task_results.values()]

@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    if task_id not in task_results:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**task_results[task_id])

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "queue_size": task_queue.qsize(),
        "total_tasks": len(task_results)
    }

@app.get("/api/success_cases")
async def get_success_cases(limit: int = 10):
    cases = [t for t in task_results.values() if t["status"] == TaskStatus.SUCCESS]
    cases.sort(key=lambda x: x.get("completed_at", ""), reverse=True)
    return [
        {
            "task_id": c["task_id"],
            "platform": c["platform"],
            "txt_id": c["txt_id"],
            "img_id": c["img_id"],
            "result": c.get("result"),
            "completed_at": c.get("completed_at")
        }
        for c in cases[:limit]
    ]

async def worker_loop():
    while True:
        task = await task_queue.get()
        await execute_and_judge(task)
        task_queue.task_done()

async def execute_and_judge(task: dict):
    task_id = task["task_id"]
    platform = task["platform"]
    
    task["status"] = TaskStatus.RUNNING
    task["started_at"] = datetime.now().isoformat()
    task_results[task_id] = task.copy()
    
    logger.info(f"执行任务 {task_id}: {platform} txt#{task['txt_id']} img#{task['img_id']}")
    
    worker_path = task.get("worker_path") or str(config.WORKER_DIR / "worker.py")
    
    try:
        proc = await asyncio.create_subprocess_exec(
            "python", worker_path,
            "--platform", platform,
            "--txtid", str(task["txt_id"]),
            "--imgid", str(task["img_id"]),
            "--auto",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=config.WORKER_TIMEOUT
            )
            
            output = stdout.decode("utf-8", errors="ignore")
            success = proc.returncode == 0
            
            result_line = [line for line in output.split("\n") if line.startswith("RESULT:")]
            if result_line:
                parts = result_line[0].split(":")
                success = parts[1] == "success"
                task["result"] = ":".join(parts[2:]) if len(parts) > 2 else output.strip()
            else:
                task["result"] = "success" if success else stderr.decode("utf-8", errors="ignore").strip()
            
            task["status"] = TaskStatus.SUCCESS if success else TaskStatus.FAILED
            
        except asyncio.TimeoutError:
            logger.warning(f"任务 {task_id} 超时，强杀")
            try:
                if os.name == "nt":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], 
                                   capture_output=True, timeout=5)
            except:
                pass
            task["status"] = TaskStatus.TIMEOUT
            task["result"] = f"Worker timeout after {config.WORKER_TIMEOUT}s"
            
    except Exception as e:
        logger.error(f"任务 {task_id} 异常: {e}")
        task["status"] = TaskStatus.FAILED
        task["result"] = f"Exception: {str(e)}"
    
    task["completed_at"] = datetime.now().isoformat()
    task_results[task_id] = task.copy()
    
    judge_and_dispatch(task)

def judge_and_dispatch(task: dict):
    status = task["status"]
    task_id = task["task_id"]
    
    if status == TaskStatus.SUCCESS:
        logger.info(f"任务 {task_id} 成功，记录结果")
    elif status in [TaskStatus.FAILED, TaskStatus.TIMEOUT]:
        if task["retry_count"] < task["max_retries"]:
            task["retry_count"] += 1
            task["status"] = TaskStatus.PENDING
            logger.info(f"任务 {task_id} 失败，第 {task['retry_count']} 次重试")
            asyncio.create_task(task_queue.put(task))
        else:
            logger.error(f"任务 {task_id} 最终失败，放弃")

@app.on_event("startup")
async def startup():
    asyncio.create_task(worker_loop())

if __name__ == "__main__":
    import uvicorn
    logger.info("启动审核监督中间层...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
