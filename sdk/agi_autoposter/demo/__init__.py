import asyncio
import sys
import os
import signal
from pathlib import Path

async def run_demo():
    print("=" * 60)
    print("  AGI AutoPoster - 三层架构完整演示")
    print("=" * 60)
    print()
    
    middleware_server = None
    
    try:
        from agi_autoposter.middleware import app
        import uvicorn
        
        print("[1/3] 启动审核监督中间层...")
        
        config = uvicorn.Config(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="warning",
            access_log=False
        )
        server = uvicorn.Server(config)
        
        asyncio.create_task(server.serve())
        
        await asyncio.sleep(2)
        
        if not server.started:
            print("  中间层启动中，请稍候...")
            await asyncio.sleep(3)
        
        print("  中间层已启动: http://127.0.0.1:8000")
        print()
        
        print("[2/3] 运行多分身调度演示...")
        from agi_autoposter.demo.multi_scheduler_demo import run_multi_scheduler_demo
        await run_multi_scheduler_demo()
        print()
        
        await asyncio.sleep(2)
        
        print("[3/3] 运行内容层演示...")
        from agi_autoposter.demo.content_layer_demo import run_content_layer_demo
        await run_content_layer_demo()
        print()
        
        print("=" * 60)
        print("  演示完成！")
        print("=" * 60)
        
    except OSError as e:
        if "address already in use" in str(e).lower() or "10048" in str(e):
            print(f"\n错误: 端口 8000 已被占用")
            print("请先关闭占用 8000 端口的程序，或修改中间层配置使用其他端口")
        else:
            print(f"\n错误: {e}")
    except Exception as e:
        print(f"\n演示运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if middleware_server:
            print("\n正在关闭中间层...")
            middleware_server.should_exit = True
            await asyncio.sleep(1)
            print("中间层已关闭")
