import os
from typing import Optional
from datetime import datetime
from config.settings import VIDEO_OUTPUT_DIR, VIDEO_RESOLUTION, VIDEO_FPS

class VideoComposer:
    """视频合成引擎"""
    
    def __init__(self, resolution: tuple = None):
        self.resolution = resolution or VIDEO_RESOLUTION
        self.width, self.height = self.resolution
        self.fps = VIDEO_FPS
    
    def compose_video(
        self,
        script: str,
        audio_path: str,
        output_path: str,
        bg_image: Optional[str] = None,
        subtitle: bool = True
    ) -> Optional[str]:
        """
        合成视频
        
        参数:
            script: 脚本文本
            audio_path: 配音文件路径
            output_path: 输出视频路径
            bg_image: 背景图片路径
            subtitle: 是否添加字幕
        
        返回:
            输出文件路径，失败返回None
        """
        try:
            from moviepy.editor import (
                ColorClip, ImageClip, TextClip, CompositeVideoClip,
                AudioFileClip
            )
            from PIL import Image, ImageDraw, ImageFont
            
            print(f"正在合成视频...")
            
            # 1. 准备背景
            if bg_image and os.path.exists(bg_image):
                bg = ImageClip(bg_image).set_duration(0)
                bg = bg.resize(height=self.height)
            else:
                # 使用深色背景
                bg = ColorClip(size=self.resolution, color=(20, 20, 20))
            
            # 2. 加载配音
            if not os.path.exists(audio_path):
                print(f"✗ 音频文件不存在: {audio_path}")
                return None
            
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # 3. 生成字幕
            if subtitle:
                subtitle_clip = self._generate_subtitle_clip(script, duration)
                video = CompositeVideoClip(
                    [bg.set_duration(duration), subtitle_clip],
                    size=self.resolution
                ).set_audio(audio)
            else:
                video = bg.set_duration(duration).set_audio(audio)
            
            # 4. 导出视频
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            print(f"  输出: {output_path}")
            print(f"  分辨率: {self.resolution}")
            print(f"  时长: {duration:.1f}秒")
            
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # 清理
            video.close()
            audio.close()
            
            print(f"✓ 视频合成完成: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"✗ 视频合成失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _generate_subtitle_clip(self, text: str, duration: float):
        """
        生成字幕视频片段
        
        参数:
            text: 字幕文本
            duration: 时长
        
        返回:
            字幕clip
        """
        try:
            from moviepy.editor import ImageClip
            from PIL import Image, ImageDraw, ImageFont
            
            # 创建带背景的字幕图片
            subtitle_img = Image.new('RGBA', self.resolution, (0, 0, 0, 180))
            draw = ImageDraw.Draw(subtitle_img)
            
            # 尝试使用系统字体
            try:
                font = ImageFont.truetype(
                    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                    40
                )
            except:
                try:
                    font = ImageFont.truetype("C:\\Windows\\Fonts\\msyh.ttc", 40)
                except:
                    font = ImageFont.load_default()
            
            # 文字换行处理
            lines = self._wrap_text(text, 30)
            y = 200
            
            for line in lines[:6]:  # 最多显示6行
                draw.text(
                    (40, y),
                    line,
                    fill=(255, 255, 255, 255),
                    font=font
                )
                y += 60
            
            # 保存临时图片
            subtitle_img_path = "/tmp/subtitle_temp.png"
            os.makedirs("/tmp", exist_ok=True)
            subtitle_img.save(subtitle_img_path)
            
            subtitle_clip = ImageClip(subtitle_img_path).set_duration(duration)
            return subtitle_clip
        
        except Exception as e:
            print(f"⚠ 字幕生成失败: {str(e)}")
            return None
    
    @staticmethod
    def _wrap_text(text: str, width: int) -> list:
        """
        文本换行处理
        
        参数:
            text: 文本
            width: 每行宽度（字符数）
        
        返回:
            换行后的文本行列表
        """
        lines = []
        for char_line in text.split('\n'):
            if len(char_line) <= width:
                lines.append(char_line)
            else:
                for i in range(0, len(char_line), width):
                    lines.append(char_line[i:i+width])
        return lines
