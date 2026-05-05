#!/usr/bin/env python3
"""
大模型调度层
只做两件事：
  1. 发指令 - 推送任务到中间层
  2. 等待接收 - 接收执行结果反馈
"""

import httpx
import asyncio

MIDDLEWARE_URL = "http://localhost:8000"

def generate_tasks():
    """生成发帖任务"""
    return [
        {"platform": "douyin", "txt_id": 1, "img_id": 3},
        {"platform": "douyin", "txt_id": 2, "img_id": 4},
        {"platform": "facebook", "txt_id": 3, "img_id": 5},
        {"platform": "tiktok", "txt_id": 4, "img_id": 1},
        {"platform": "x", "txt_id": 5, "img_id": 2},
        {"platform": "instagram", "txt_id": 6, "img_id": 3},
        {"platform": "facebook", "txt_id": 7, "img_id": 6},
    ]

async def main():
    print("=" * 50)
    print("  调度层 - 发指令 & 等待接收")
    print("=" * 50)
    
    tasks = generate_tasks()
    print(f"\n[发指令] 生成 {len(tasks)} 个任务")
    
    async with httpx.AsyncClient() as client:
        submitted = []
        for task in tasks:
            resp = await client.post(f"{MIDDLEWARE_URL}/api/tasks", json=task)
            result = resp.json()
            print(f"  已发送: {result['task_id']} -> {result['platform']}")
            submitted.append(result["task_id"])
            await asyncio.sleep(0.2)
        
        print(f"\n[等待接收] 等待执行结果...")
        await asyncio.sleep(40)
        
        print("\n[接收结果]")
        print("-" * 50)
        for task_id in submitted:
            resp = await client.get(f"{MIDDLEWARE_URL}/api/tasks/{task_id}")
            status = resp.json()
            icon = "✓" if status["status"] == "success" else "✗"
            result = status.get("result") or "N/A"
            if isinstance(result, dict):
                result = str(result)
            print(f"  {icon} {task_id}: {status['status']:10} | {str(result)[:60]}")
        
        print("-" * 50)
        print("[调度层] 本轮完成")

if __name__ == "__main__":
    asyncio.run(main())
