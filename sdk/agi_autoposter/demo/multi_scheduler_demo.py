#!/usr/bin/env python3
"""
分身调度演示 - multi_scheduler_demo.py

展示核心能力：
  1. 同一个大模型 API 被包装成多个「无状态调度分身」
  2. 所有分身同时向中间层提交任务
  3. 分身之间不通信、不共享状态、互不感知
  4. 中间层统一排队、执行、返回结果

运行前提：
  中间层已启动（python middleware.py）
"""

import asyncio
import httpx
import random
from datetime import datetime

MIDDLEWARE_URL = "http://localhost:8000"

NUM_SCHEDULERS = 5
TASKS_PER_SCHEDULER = 3


class SchedulerClone:
    def __init__(self, clone_id: int, client: httpx.AsyncClient):
        self.clone_id = clone_id
        self.client = client
        self.task_ids = []

    async def run(self):
        print(f"[分身#{self.clone_id}] 开始工作")
        
        platforms = ["douyin", "facebook", "tiktok", "x", "instagram"]
        
        for i in range(TASKS_PER_SCHEDULER):
            platform = random.choice(platforms)
            txt_id = self.clone_id * 10 + i
            img_id = random.randint(1, 10)
            
            resp = await self.client.post(
                f"{MIDDLEWARE_URL}/api/tasks",
                json={"platform": platform, "txt_id": txt_id, "img_id": img_id}
            )
            result = resp.json()
            self.task_ids.append(result["task_id"])
            print(f"[分身#{self.clone_id}] 发送任务: {result['task_id']} -> {platform}")
            
            await asyncio.sleep(0.3)
        
        print(f"[分身#{self.clone_id}] 完成，共发送 {len(self.task_ids)} 个任务")


async def run_multi_scheduler_demo():
    print("=" * 60)
    print("  分身调度演示")
    print("=" * 60)
    print(f"\n启动 {NUM_SCHEDULERS} 个调度分身，每个发送 {TASKS_PER_SCHEDULER} 个任务")
    print("分身之间不通信、不共享状态、互不感知\n")
    
    async with httpx.AsyncClient() as client:
        clones = [SchedulerClone(i + 1, client) for i in range(NUM_SCHEDULERS)]
        
        await asyncio.gather(*[c.run() for c in clones])
        
        all_task_ids = []
        for c in clones:
            all_task_ids.extend(c.task_ids)
        
        print(f"\n[等待接收] 等待 {len(all_task_ids)} 个任务执行完成...")
        await asyncio.sleep(len(all_task_ids) * 3 + 10)
        
        print("\n[接收结果]")
        print("-" * 60)
        for task_id in all_task_ids:
            resp = await client.get(f"{MIDDLEWARE_URL}/api/tasks/{task_id}")
            status = resp.json()
            icon = "✓" if status["status"] == "success" else "✗"
            result = status.get("result") or "N/A"
            if isinstance(result, dict):
                result = str(result)
            print(f"  {icon} {task_id}: {status['status']:10} | {str(result)[:60]}")
        
        print("-" * 60)
        print("[分身调度演示] 完成")


async def main():
    await run_multi_scheduler_demo()

if __name__ == "__main__":
    asyncio.run(main())
