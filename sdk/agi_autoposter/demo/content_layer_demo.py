#!/usr/bin/env python3
"""
内容层独立演示 - content_layer_demo.py

展示：
  1. 内容层如何独立生成/管理内容（文案 + 图片）
  2. 大模型如何通过调度层选择已有内容（只选 ID，不编内容）
  3. 调度层只调用执行层，不碰内容数据库

运行方式：
  python content_layer_demo.py
"""

import asyncio
import httpx
import random
from datetime import datetime

MIDDLEWARE_URL = "http://localhost:8000"

class ContentLibrary:
    def __init__(self):
        self.contents = [
            {"id": 1, "title": "AI产品推广", "txt": "全新AI工具上线...", "img": [101, 102, 103]},
            {"id": 2, "title": "天气预报", "txt": "今日晴天...", "img": [201, 202]},
            {"id": 3, "title": "美食推荐", "txt": "这家餐厅超好吃...", "img": [301, 302, 303, 304]},
            {"id": 4, "title": "健身教程", "txt": "每天30分钟...", "img": [401, 402]},
            {"id": 5, "title": "旅行攻略", "txt": "周末去哪儿...", "img": [501, 502, 503]},
        ]
    
    def get_content(self, content_id: int):
        for c in self.contents:
            if c["id"] == content_id:
                return c
        return None
    
    def get_all_ids(self):
        return [c["id"] for c in self.contents]
    
    def random_select(self, count=3):
        selected = random.sample(self.contents, min(count, len(self.contents)))
        return [{"content_id": c["id"], "title": c["title"], "txt_id": c["id"], "img_id": random.choice(c["img"])} for c in selected]

content_lib = ContentLibrary()

async def submit_task(client: httpx.AsyncClient, content_id: int, img_id: int, platform: str):
    resp = await client.post(f"{MIDDLEWARE_URL}/api/tasks", json={
        "platform": platform,
        "txt_id": content_id,
        "img_id": img_id
    })
    return resp.json()

async def run_content_layer_demo():
    print("=" * 60)
    print("  内容层独立演示")
    print("=" * 60)
    
    print("\n[内容层] 当前内容库:")
    for c in content_lib.contents:
        print(f"  ID={c['id']} | {c['title']} | 图片: {c['img']}")
    
    print("\n[调度层] 大模型从内容层选择内容:")
    selected = content_lib.random_select(count=3)
    for s in selected:
        content = content_lib.get_content(s["content_id"])
        print(f"  选择: content_id={s['content_id']} ({s['title']}) -> img_id={s['img_id']}")
        print(f"    文案: {content['txt'][:30]}...")
    
    print("\n[调度层] 发送指令到中间层:")
    platforms = ["douyin", "facebook", "tiktok"]
    submitted = []
    
    async with httpx.AsyncClient() as client:
        for i, s in enumerate(selected):
            platform = platforms[i % len(platforms)]
            result = await submit_task(client, s["content_id"], s["img_id"], platform)
            print(f"  已发送: {result['task_id']} -> {platform} (content_id={s['content_id']}, img_id={s['img_id']})")
            submitted.append(result["task_id"])
        
        print("\n[调度层] 等待执行结果...")
        await asyncio.sleep(15)
        
        print("\n[接收结果]")
        print("-" * 60)
        for task_id in submitted:
            resp = await client.get(f"{MIDDLEWARE_URL}/api/tasks/{task_id}")
            status = resp.json()
            icon = "✓" if status["status"] == "success" else "✗"
            result = status.get("result") or "N/A"
            if isinstance(result, dict):
                result = str(result)
            print(f"  {icon} {task_id}: {status['status']:10} | {str(result)[:60]}")
        
        print("-" * 60)
        print("[内容层演示] 完成")
        print("\n关键：大模型只选择了已有的 content_id，没有编造内容。")


async def main():
    await run_content_layer_demo()

if __name__ == "__main__":
    asyncio.run(main())
