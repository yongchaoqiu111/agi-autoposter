#!/usr/bin/env python3
"""
全平台通用 EXE 改造模板
用法：
  双击打开 = 正常界面模式
  带参数启动 = 静默后台自动执行
  
示例：
  python worker.py --platform douyin --txtid 5 --imgid 3 --auto
  
输出标准格式（供中间层解析）：
  RESULT:success:url=https://xxx
  RESULT:fail:error=xxx
"""

import argparse
import sys
import time
import random

def gui_mode():
    """界面模式 - 保留原有功能"""
    print("=" * 50)
    print("  多平台发帖工具 - 界面版")
    print("=" * 50)
    print("\n请选择平台：")
    print("1. 抖音")
    print("2. Facebook")
    print("3. 快手")
    print("4. TikTok")
    print("5. X (Twitter)")
    print("6. Instagram")
    print("\n（此为演示模式，实际应显示 GUI 界面）")
    input("\n按回车键退出...")

def auto_mode(platform: str, txt_id: int, img_id: int):
    """静默自动模式 - 后台执行"""
    print(f"[{platform}] 开始执行自动发帖任务")
    print(f"  文案 ID: {txt_id}")
    print(f"  图片 ID: {img_id}")
    
    print(f"[{platform}] 加载文案 #{txt_id}...")
    time.sleep(0.5)
    
    print(f"[{platform}] 加载图片 #{img_id}...")
    time.sleep(0.5)
    
    print(f"[{platform}] 正在发布...")
    time.sleep(1)
    
    success = random.random() > 0.1
    
    if success:
        post_url = f"https://{platform}.com/post/{txt_id}_{img_id}_{int(time.time())}"
        print(f"[{platform}] 发布成功！")
        print(f"[{platform}] 帖子链接: {post_url}")
        print(f"\nRESULT:success:url={post_url}")
        return 0
    else:
        print(f"[{platform}] 发布失败：网络错误")
        print(f"\nRESULT:fail:error=network_error")
        return 1

def main():
    parser = argparse.ArgumentParser(description="多平台发帖工具")
    parser.add_argument("--platform", type=str, help="目标平台 (douyin/facebook/kuaishou/tiktok/x/instagram)")
    parser.add_argument("--txtid", type=int, help="文案 ID")
    parser.add_argument("--imgid", type=int, help="图片 ID")
    parser.add_argument("--auto", action="store_true", help="启用自动模式")
    
    args = parser.parse_args()
    
    if args.auto and args.platform and args.txtid and args.imgid:
        exit_code = auto_mode(args.platform, args.txtid, args.imgid)
        sys.exit(exit_code)
    else:
        gui_mode()

if __name__ == "__main__":
    main()
