# AI Video Factory - 自动化短视频生成系统

## 项目简介

这是一个完全自动化的AI短视频生成系统，可以:
- 自动生成原创视频脚本（中英日三语言）
- 自动配音和视频合成
- 自动上传到国内外多个视频平台
- 实现自动化广告变现

## 核心特性

✅ **完全自动化** - 脚本生成→配音→视频合成→自动上传
✅ **多语言支持** - 中文、英文、日文
✅ **多平台矩阵** - 国内5个+国外8个账号
✅ **法律合规** - 原创内容，零版权风险
✅ **低运营成本** - 月运营成本<¥2000
✅ **快速变现** - 2-3个月开始产生收入

## 项目结构

```
ai-video-factory/
├── config/                  # 配置文件
│   ├── __init__.py
│   ├── settings.py         # API密钥和全局配置
│   ├── accounts.json       # 账号管理
│   └── platforms.json      # 平台配置
├── core/                   # 核心模块
│   ├── __init__.py
│   ├── script_generator.py # 脚本生成
│   ├── tts_engine.py       # 配音引擎
│   ├── subtitle_generator.py # 字幕生成
│   ├── video_composer.py   # 视频合成
│   └── image_processor.py  # 图片处理
├── uploaders/              # 上传模块
│   ├── __init__.py
│   ├── youtube.py          # YouTube上传
│   ├── douyin.py           # 抖音上传
│   ├── xiaohongshu.py      # 小红书（手动）
│   ├── bilibili.py         # B站上传
│   ├── tiktok.py           # TikTok上传
│   └── instagram.py        # Instagram上传
├── utils/                  # 工具函数
│   ├── __init__.py
│   ├── logger.py           # 日志管理
│   ├── db_manager.py       # 数据库操作
│   ├── api_client.py       # API调用
│   └── scheduler.py        # 定时任务
├── tasks/                  # 定时任务
│   ├── __init__.py
│   ├── generate_scripts.py # 脚本生成任务
│   ├── compose_videos.py   # 视频合成任务
│   └── auto_upload.py      # 自动上传任务
├── data/                   # 数据目录
│   ├── scripts/            # 保存脚本
│   ├── videos/             # 生成的视频
│   └── uploads_log.db      # 上传记录
├── .env.example            # 环境变量模板
├── requirements.txt        # Python依赖
├── main.py                 # 主程序入口
└── setup.sh                # 快速设置脚本
```

## 快速开始

### 前置要求

- Python 3.9+
- FFmpeg 4.0+
- 有效的Claude API密钥
- 国外平台访问工具（VPN）

### 安装步骤

```bash
# 1. Clone仓库
git clone https://github.com/gfliu2335/lifedev.git
cd lifedev

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入API密钥

# 5. 初始化数据库
python main.py --init

# 6. 测试系统
python main.py --test
```

## 使用指南

### 生成脚本

```bash
python main.py --generate-scripts --category knowledge --count 5
```

### 生成视频

```bash
python main.py --compose-videos --script-id 1 --languages cn,en,ja
```

### 上传视频

```bash
python main.py --upload --platform youtube --video-id 1
```

### 启动自动化

```bash
python main.py --start-scheduler
```

## 变现方案

### 国内平台

| 平台 | 粉丝要求 | 单价 | 预期收入 |
|------|---------|------|--------|
| 抖音创作者基金 | 10w粉 | ¥10-50/1000播放 | ¥5000-20000/月 |
| 小红书品牌广告 | 有流量即可 | ¥500-5000/条 | ¥2000-10000/月 |
| B站创作激励 | 1000粉 | ¥5-20/1000播放 | ¥1000-5000/月 |

### 国外平台

| 平台 | 粉丝要求 | 单价 | 预期收入 |
|------|---------|------|--------|
| YouTube Partner | 1000订阅 | ¥5-30/1000展示 | ¥5000-30000/月 |
| TikTok Creator Fund | 10k粉 | ¥0.02-0.04/1000播放 | ¥1000-5000/月 |

## 成本预算

### 初期投入

| 项目 | 金额 |
|------|------|
| Claude API额度 | ¥2000（您已有） |
| ElevenLabs配音 | ¥1000-2000 |
| 服务器/函数 | ¥500 |
| VPN | ¥200 |
| 其他工具 | ¥500 |
| **总计** | **¥4200-5200** |

### 月度成本

| 项目 | 金额 |
|------|------|
| ElevenLabs | ¥1000-1500 |
| 服务器 | ¥500 |
| VPN | ¥20 |
| 存储 | ¥100 |
| **总计** | **¥1620-2120/月** |

## 开发周期

- 第1周：环境搭建+账号注册
- 第2周：核心模块开发
- 第3周：上传模块+自动化
- 第4周：测试和优化
- 第5-6周：持续运营数据收集
- 第7-8周：变现启动

## 文档

- [详细部署指南](./docs/deployment.md)
- [API配置教程](./docs/api-setup.md)
- [账号注册指南](./docs/account-setup.md)
- [常见问题解决](./docs/faq.md)

## 许可证

MIT

## 联系方式

如有问题，请提Issue或联系作者。
