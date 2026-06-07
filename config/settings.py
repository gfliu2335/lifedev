import os
from dotenv import load_dotenv
from pathlib import Path
import json

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# ============ API配置 ============
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_MODEL = "eleven_monolingual_v1"

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# ============ 视频配置 ============
VIDEO_RESOLUTION = (1080, 1920)  # 竖屏
VIDEO_FPS = 30
VIDEO_BITRATE = "5000k"
VIDEO_AUDIO_BITRATE = "128k"
VIDEO_CODEC = "libx264"
VIDEO_AUDIO_CODEC = "aac"

# ============ 路径配置 ============
VIDEO_OUTPUT_DIR = os.getenv("VIDEO_OUTPUT_DIR", str(BASE_DIR / "data" / "videos"))
SCRIPT_OUTPUT_DIR = os.getenv("SCRIPT_OUTPUT_DIR", str(BASE_DIR / "data" / "scripts"))
LOG_DIR = str(BASE_DIR / "logs")
DATA_DIR = str(BASE_DIR / "data")

# 创建必要的目录
for dir_path in [VIDEO_OUTPUT_DIR, SCRIPT_OUTPUT_DIR, LOG_DIR, DATA_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# ============ 数据库配置 ============
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/uploads_log.db")

# ============ 日志配置 ============
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# ============ 代理配置 ============
PROXY_URL = os.getenv("PROXY_URL")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")

def get_proxy():
    """获取代理配置"""
    if PROXY_URL:
        if PROXY_USERNAME and PROXY_PASSWORD:
            return f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_URL}"
        return f"http://{PROXY_URL}"
    return None

# ============ 系统配置 ============
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
TIMEOUT = 300  # 超时时间（秒）

# ============ 脚本生成配置 ============
SCRIPT_CATEGORIES = {
    'knowledge': '生活冷知识、科学知识、历史趣闻',
    'lifestyle': '日常生活技巧、家居收纳、穿搭建议',
    'comedy': '搞笑段子、网络段子改编、日常趣事',
    'tutorial': '技能教程、DIY手工、烹饪讲解',
    'drama': '虚拟故事、剧情讲述、悬疑短剧'
}

SCRIPT_LENGTH_RANGE = (600, 800)  # 字数范围
VIDEO_DURATION_RANGE = (15, 60)   # 视频时长范围（秒）

# ============ 语言配置 ============
SUPPORTED_LANGUAGES = ['cn', 'en', 'ja']

TTS_VOICES = {
    'cn': 'zh-CN-Neural2-A',
    'en': '21m00Tcm4TlvDq8ikWAM',  # ElevenLabs voice ID
    'ja': 'ja-JP-Neural2-B'
}

# ============ 平台配置 ============
PLATFORMS = {
    'douyin': {
        'name': '抖音',
        'type': 'video',
        'min_followers': 0,
        'supports_languages': ['cn'],
        'auto_upload': True
    },
    'xiaohongshu': {
        'name': '小红书',
        'type': 'content',
        'min_followers': 0,
        'supports_languages': ['cn'],
        'auto_upload': False  # 需要手动
    },
    'bilibili': {
        'name': 'B站',
        'type': 'video',
        'min_followers': 0,
        'supports_languages': ['cn'],
        'auto_upload': True
    },
    'youtube': {
        'name': 'YouTube',
        'type': 'video',
        'min_followers': 1000,
        'supports_languages': ['en'],
        'auto_upload': True
    },
    'tiktok': {
        'name': 'TikTok',
        'type': 'video',
        'min_followers': 0,
        'supports_languages': ['en'],
        'auto_upload': True
    },
    'instagram': {
        'name': 'Instagram',
        'type': 'content',
        'min_followers': 0,
        'supports_languages': ['en'],
        'auto_upload': True
    }
}

# ============ 发布计划 ============
PUBLISH_SCHEDULE = {
    'douyin': ['09:00', '14:00', '20:00'],      # 每天3次
    'youtube': ['10:00', '18:00'],              # 每天2次
    'tiktok': ['09:00', '15:00', '21:00'],      # 每天3次
    'bilibili': ['12:00', '19:00'],             # 每天2次
    'xiaohongshu': ['10:00', '15:00'],          # 每天2次
    'instagram': ['08:00', '17:00']             # 每天2次
}

# ============ 账号配置 ============
def load_accounts():
    """从.env加载账号配置"""
    accounts = {}
    
    douyin_accounts_str = os.getenv("DOUYIN_ACCOUNTS", "[]")
    youtube_accounts_str = os.getenv("YOUTUBE_ACCOUNTS", "[]")
    tiktok_accounts_str = os.getenv("TIKTOK_ACCOUNTS", "[]")
    
    try:
        accounts['douyin'] = json.loads(douyin_accounts_str)
        accounts['youtube'] = json.loads(youtube_accounts_str)
        accounts['tiktok'] = json.loads(tiktok_accounts_str)
    except json.JSONDecodeError:
        accounts = {'douyin': [], 'youtube': [], 'tiktok': []}
    
    return accounts

ACCOUNTS = load_accounts()

print(f"✓ 配置已加载")
print(f"  Claude API: {bool(CLAUDE_API_KEY)}")
print(f"  ElevenLabs API: {bool(ELEVENLABS_API_KEY)}")
print(f"  视频输出目录: {VIDEO_OUTPUT_DIR}")
