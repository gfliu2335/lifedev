#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI Video Factory - 主程序入口

自动化短视频生成和上传系统
"""

import argparse
import sys
from datetime import datetime
from core.script_generator import ScriptGenerator
from core.tts_engine import TTSEngine
from core.video_composer import VideoComposer
from utils.logger import setup_logger
from config.settings import VIDEO_OUTPUT_DIR
import os

logger = setup_logger(__name__)

class VideoFactory:
    """主工厂类"""
    
    def __init__(self):
        self.script_gen = None
        self.tts = None
        self.composer = None
        self._initialize()
    
    def _initialize(self):
        """初始化所有组件"""
        try:
            print("\n🚀 正在初始化AI Video Factory...")
            
            # 初始化脚本生成器
            print("  └─ 初始化脚本生成器...")
            self.script_gen = ScriptGenerator()
            print("    ✓ 脚本生成器就绪")
            
            # 初始化TTS引擎
            print("  └─ 初始化语音合成引擎...")
            self.tts = TTSEngine()
            print("    ✓ 语音合成引擎就绪")
            
            # 初始化视频合成器
            print("  └─ 初始化视频合成器...")
            self.composer = VideoComposer()
            print("    ✓ 视频合成器就绪")
            
            print("\n✅ 初始化完成！\n")
            return True
        
        except Exception as e:
            print(f"\n❌ 初始化失败: {str(e)}\n")
            return False
    
    def test_mode(self):
        """测试模式 - 完整流程演示"""
        print("\n" + "="*60)
        print("🧪 测试模式 - 完整流程演示")
        print("="*60 + "\n")
        
        # 1. 生成脚本
        print("[步骤1] 生成测试脚本...")
        scripts = self.script_gen.generate_cn_scripts(category='knowledge', count=1)
        
        if not scripts:
            print("❌ 脚本生成失败")
            return False
        
        script = scripts[0]
        print(f"✓ 脚本生成成功")
        print(f"  标题: {script['title']}")
        print(f"  字数: {len(script['content'])}")
        
        # 2. 翻译脚本
        print("\n[步骤2] 翻译脚本到英文和日文...")
        en_script = self.script_gen.translate_to_english(script['content'])
        ja_script = self.script_gen.translate_to_japanese(script['content'])
        
        if en_script:
            print(f"✓ 英文翻译成功 ({len(en_script)}字)")
        else:
            print(f"⚠ 英文翻译失败")
        
        if ja_script:
            print(f"✓ 日文翻译成功 ({len(ja_script)}字)")
        else:
            print(f"⚠ 日文翻译失败")
        
        # 3. 生成配音
        print("\n[步骤3] 生成配音...")
        
        # 中文配音
        cn_audio = f"/tmp/test_cn.mp3"
        if self.tts.generate_cn_audio(script['content'][:100], cn_audio):
            print(f"✓ 中文配音生成成功")
        else:
            print(f"⚠ 中文配音生成失败（可能是Google TTS未配置）")
        
        # 英文配音
        en_audio = f"/tmp/test_en.mp3"
        if en_script and self.tts.generate_en_audio(en_script[:100], en_audio):
            print(f"✓ 英文配音生成成功")
        else:
            print(f"⚠ 英文配音生成失败（可能是ElevenLabs未配置）")
        
        print("\n✅ 测试完成！")
        print("\n⚠️  提示:")
        print("  1. 如果Google TTS失败，请配置GOOGLE_APPLICATION_CREDENTIALS")
        print("  2. 如果ElevenLabs失败，请配置ELEVENLABS_API_KEY")
        print("  3. 完整的视频合成需要真实的音频文件\n")
        
        return True
    
    def generate_scripts(self, category: str = 'knowledge', count: int = 5):
        """生成脚本"""
        print(f"\n生成{count}个{category}类脚本...\n")
        
        scripts = self.script_gen.generate_cn_scripts(category, count)
        
        if scripts:
            print(f"\n✅ 成功生成{len(scripts)}个脚本\n")
            
            for i, script in enumerate(scripts, 1):
                print(f"脚本 #{i}")
                print(f"  标题: {script['title']}")
                print(f"  字数: {len(script['content'])}")
                print(f"  标签: {', '.join(script.get('tags', []))}")
                print()
        else:
            print("❌ 脚本生成失败\n")
    
    def compose_video(self, script_text: str, audio_path: str = None, output_name: str = "output"):
        """合成视频"""
        if not audio_path:
            print("❌ 需要提供音频文件路径\n")
            return
        
        output_path = os.path.join(VIDEO_OUTPUT_DIR, f"{output_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        
        result = self.composer.compose_video(
            script=script_text,
            audio_path=audio_path,
            output_path=output_path,
            subtitle=True
        )
        
        if result:
            print(f"\n✅ 视频生成成功: {result}\n")
        else:
            print(f"\n❌ 视频生成失败\n")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="AI Video Factory - 自动化短视频生成系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --test                    # 运行测试
  python main.py --generate-scripts        # 生成脚本
  python main.py --generate-scripts --category comedy --count 10
        """
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='运行完整系统测试'
    )
    
    parser.add_argument(
        '--generate-scripts',
        action='store_true',
        help='生成脚本'
    )
    
    parser.add_argument(
        '--category',
        default='knowledge',
        choices=['knowledge', 'lifestyle', 'comedy', 'tutorial', 'drama'],
        help='脚本分类'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=5,
        help='生成数量'
    )
    
    parser.add_argument(
        '--init',
        action='store_true',
        help='初始化系统'
    )
    
    args = parser.parse_args()
    
    # 创建工厂实例
    factory = VideoFactory()
    
    # 执行命令
    if args.init:
        print("✓ 系统已初始化")
    elif args.test:
        factory.test_mode()
    elif args.generate_scripts:
        factory.generate_scripts(category=args.category, count=args.count)
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
