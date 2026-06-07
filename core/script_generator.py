import anthropic
import json
from datetime import datetime
from typing import List, Dict
import os
from config.settings import CLAUDE_API_KEY, CLAUDE_MODEL, SCRIPT_OUTPUT_DIR, SCRIPT_CATEGORIES

class ScriptGenerator:
    """AI脚本生成引擎"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or CLAUDE_API_KEY
        if not self.api_key:
            raise ValueError("Claude API Key not found. Please set CLAUDE_API_KEY in .env")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = CLAUDE_MODEL
    
    def generate_cn_scripts(self, category: str, count: int = 5) -> List[Dict]:
        """
        生成中文脚本
        
        参数:
            category: 脚本分类 (knowledge/lifestyle/comedy/tutorial/drama)
            count: 生成数量
        
        返回:
            脚本列表
        """
        category_desc = SCRIPT_CATEGORIES.get(category, '知识科普')
        
        prompt = f"""你是一个专业的短视频编导。请为{category_desc}类短视频生成{count}个原创脚本。

要求：
1. 每个脚本600-800字
2. 内容原创，不涉及版权
3. 适合15-60秒视频（快节奏）
4. 包含3-5个关键转折点
5. 结尾有悬念或反转（吸引观众）
6. 风格自然、贴近日常
7. 输出为JSON格式

输出格式示例：
{{
    "scripts": [
        {{
            "title": "视频标题",
            "content": "脚本正文...",
            "duration": 30,
            "category": "{category}",
            "tags": ["tag1", "tag2"],
            "keyframes": ["镜头1", "镜头2"]
        }}
    ]
}}
"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            
            # 尝试解析JSON
            try:
                result = json.loads(response_text)
                scripts = result.get('scripts', [])
                print(f"✓ 成功生成{len(scripts)}个{category}脚本")
                return scripts
            except json.JSONDecodeError:
                # 尝试提取JSON
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    scripts = result.get('scripts', [])
                    print(f"✓ 成功生成{len(scripts)}个{category}脚本")
                    return scripts
                else:
                    print(f"✗ 无法解析脚本JSON")
                    return []
        
        except Exception as e:
            print(f"✗ 脚本生成失败: {str(e)}")
            return []
    
    def translate_to_english(self, cn_script: str) -> str:
        """
        将中文脚本翻译为英文
        
        参数:
            cn_script: 中文脚本
        
        返回:
            英文脚本
        """
        prompt = f"""请将以下中文短视频脚本翻译为英文。

要求：
1. 保持原意
2. 节奏感相似（音节长度相近）
3. 适合英文配音
4. 保留所有情感和表现力

中文脚本：
{cn_script}

请只返回翻译后的英文脚本，无需其他说明。"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
        except Exception as e:
            print(f"✗ 英文翻译失败: {str(e)}")
            return ""
    
    def translate_to_japanese(self, cn_script: str) -> str:
        """
        将中文脚本翻译为日文
        
        参数:
            cn_script: 中文脚本
        
        返回:
            日文脚本
        """
        prompt = f"""請以下の中国語短動画スクリプトを日本語に翻訳してください。

要件：
1. 原意を保持する
2. リズムが似ている（音節の長さが近い）
3. 日本語の音声に適している
4. すべての感情と表現力を保持する

中国語スクリプト：
{cn_script}

翻訳後の日本語スクリプトのみを返してください。説明は不要です。"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
        except Exception as e:
            print(f"✗ 日文翻译失败: {str(e)}")
            return ""
    
    def save_script(self, script: Dict, language: str = 'cn') -> str:
        """
        保存脚本到文件
        
        参数:
            script: 脚本字典
            language: 语言代码
        
        返回:
            保存路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{script['title']}_{language}_{timestamp}.json"
        filepath = os.path.join(SCRIPT_OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 脚本已保存: {filepath}")
        return filepath
