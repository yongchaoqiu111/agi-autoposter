import asyncio
import sys
from agi_autoposter.demo import run_demo

def main():
    print("=" * 60)
    print("  AGI AutoPoster Demo - 三层结构体组合架构")
    print("=" * 60)
    print()
    
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n\n演示已手动中断，感谢使用！")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n演示运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
