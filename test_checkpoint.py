#!/usr/bin/env python3
"""
Test script for checkpoint functionality.
This script creates a small sample novel to test the checkpoint and progress features.
"""

import os
import sys
import time

def create_test_novel():
    """Create a small test novel for checkpoint testing."""
    test_content = """第1章 测试开始
这是第一章的内容，用来测试断点续传功能。这里有足够的文字来生成一个有意义的摘要。
故事讲述了一个测试程序的冒险旅程，充满了各种挑战和惊喜。

第2章 功能验证
第二章继续我们的测试旅程。这里我们验证了各种功能，包括进度条显示和阶段性保存。
测试过程中遇到了许多有趣的问题，但都被一一解决了。

第3章 断点重启
第三章专门测试断点重启功能。当程序被中断时，能够从上次停止的地方继续处理。
这是一个非常重要的功能，特别是对于长篇小说的处理。

第4章 进度显示
第四章测试tqdm进度条的显示效果。用户可以清楚地看到处理进度和剩余时间。
这大大提升了用户体验，让等待变得不那么焦虑。

第5章 最终测试
最后一章进行综合测试，确保所有功能都能正常工作。
测试完成后，我们将有一个完整的小说摘要生成系统。
"""
    
    # Create test novel
    os.makedirs("novels", exist_ok=True)
    test_file = "novels/test_checkpoint.txt"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"✅ Created test novel: {test_file}")
    return test_file

def run_checkpoint_test():
    """Run checkpoint functionality test."""
    print("=" * 60)
    print("📋 CHECKPOINT FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Create test novel
    test_file = create_test_novel()
    
    print(f"\n📖 Test novel created with 5 chapters")
    print(f"📄 File: {test_file}")
    
    print(f"\n🚀 To test checkpoint functionality:")
    print(f"1. Run: python main.py {test_file}")
    print(f"2. Wait for a few chapters to process")
    print(f"3. Press Ctrl+C to interrupt")
    print(f"4. Check the checkpoints/ directory for saved progress")
    print(f"5. Run the same command again to resume from checkpoint")
    print(f"6. Use --no-resume to start fresh: python main.py {test_file} --no-resume")
    
    print(f"\n📁 Expected files after interruption:")
    print(f"   checkpoints/test_checkpoint_checkpoint.json  # Checkpoint data")
    print(f"   checkpoints/test_checkpoint_progress.md      # Intermediate results")
    
    print(f"\n🔧 Features to test:")
    print(f"   ✅ tqdm progress bar display")
    print(f"   ✅ Automatic checkpoint saving after each chapter")
    print(f"   ✅ Interrupt handling (Ctrl+C)")
    print(f"   ✅ Resume from checkpoint")
    print(f"   ✅ Intermediate progress file generation")
    print(f"   ✅ Final cleanup of checkpoint files")
    
    # Check if LMStudio is running
    try:
        import requests
        response = requests.get("http://localhost:1234/v1/models", timeout=3)
        if response.status_code == 200:
            print(f"\n✅ LMStudio server is ready - you can run the test now!")
            print(f"🚀 Run: python main.py {test_file}")
        else:
            print(f"\n⚠️ LMStudio server not fully ready")
    except:
        print(f"\n⚠️ LMStudio server not running - start it first")
    
    return test_file

if __name__ == "__main__":
    run_checkpoint_test() 