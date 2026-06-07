import os
from typing import Optional
from config.settings import ELEVENLABS_API_KEY, GOOGLE_APPLICATION_CREDENTIALS

class TTSEngine:
    """文本转语音引擎"""
    
    def __init__(self):
        self.elevenlabs_api_key = ELEVENLABS_API_KEY
        self.google_credentials = GOOGLE_APPLICATION_CREDENTIALS
        
        # 初始化Google TTS
        if self.google_credentials and os.path.exists(self.google_credentials):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.google_credentials
            try:
                from google.cloud import texttospeech
                self.google_client = texttospeech.TextToSpeechClient()
                self.google_available = True
            except Exception as e:
                print(f"⚠ Google TTS初始化失败: {str(e)}")
                self.google_available = False
        else:
            self.google_available = False
            print(f"⚠ Google凭证文件未找到")
    
    def generate_cn_audio(self, text: str, output_path: str, voice: str = "zh-CN-Neural2-A") -> Optional[str]:
        """
        使用Google TTS生成中文配音
        
        参数:
            text: 要转换的中文文本
            output_path: 输出文件路径
            voice: 声音选择 (zh-CN-Neural2-A 或 zh-CN-Neural2-B)
        
        返回:
            输出文件路径，失败返回None
        """
        if not self.google_available:
            print("✗ Google TTS不可用")
            return None
        
        try:
            from google.cloud import texttospeech
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice_obj = texttospeech.VoiceSelectionParams(
                language_code="zh-CN",
                name=voice,
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0
            )
            
            response = self.google_client.synthesize_speech(
                input=synthesis_input,
                voice=voice_obj,
                audio_config=audio_config
            )
            
            # 保存音频
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            
            print(f"✓ 中文配音已生成: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"✗ 中文配音生成失败: {str(e)}")
            return None
    
    def generate_en_audio(self, text: str, output_path: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> Optional[str]:
        """
        使用ElevenLabs生成英文配音
        
        参数:
            text: 要转换的英文文本
            output_path: 输出文件路径
            voice_id: ElevenLabs voice ID
        
        返回:
            输出文件路径，失败返回None
        """
        if not self.elevenlabs_api_key:
            print("✗ ElevenLabs API Key未配置")
            return None
        
        try:
            from elevenlabs import generate, Voice, VoiceSettings
            
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=voice_id,
                    settings=VoiceSettings(stability=0.71, similarity_boost=0.75)
                ),
                api_key=self.elevenlabs_api_key,
                model="eleven_monolingual_v1"
            )
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(audio)
            
            print(f"✓ 英文配音已生成: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"✗ 英文配音生成失败: {str(e)}")
            return None
    
    def generate_ja_audio(self, text: str, output_path: str) -> Optional[str]:
        """
        使用Google TTS生成日文配音
        
        参数:
            text: 要转换的日文文本
            output_path: 输出文件路径
        
        返回:
            输出文件路径，失败返回None
        """
        if not self.google_available:
            print("✗ Google TTS不可用")
            return None
        
        try:
            from google.cloud import texttospeech
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice_obj = texttospeech.VoiceSelectionParams(
                language_code="ja-JP",
                name="ja-JP-Neural2-B",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0
            )
            
            response = self.google_client.synthesize_speech(
                input=synthesis_input,
                voice=voice_obj,
                audio_config=audio_config
            )
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            
            print(f"✓ 日文配音已生成: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"✗ 日文配音生成失败: {str(e)}")
            return None
