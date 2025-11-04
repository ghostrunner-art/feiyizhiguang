# 非遗之光 - 中国非物质文化遗产宣传网站

## 项目简介

"非遗之光"是一个专门用于宣传中国非物质文化遗产的网站，集成了AI智能问答功能，让用户能够便捷地了解和探索中华文化瑰宝。

## 核心功能

### 🎭 非遗内容展示
- **分类展示**：按照官方10个类别展示非遗项目
  - 民间文学、传统音乐、传统舞蹈、传统戏剧、曲艺
  - 传统体育游艺杂技、传统美术、传统技艺、传统医药、民俗
- **搜索功能**：支持关键词搜索非遗项目
- **详情页面**：每个非遗项目都有详细的图文介绍

### 🤖 AI智能问答
- **专业知识库**：集成中国非物质文化遗产知识库
- **自然语言交互**：用户可通过自然语言提问
- **智能回退机制**：华为云AI不可用时自动使用本地知识库

## 技术架构

- **后端框架**：Python Flask
- **数据库**：SQLite
- **AI接口**：华为云大模型API（支持本地回退）
- **前端设计**：传统文化风格，响应式布局

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 初始化数据库
```bash
python init_data.py
```

### 3. 配置环境变量（可选）
复制 `.env.example` 为 `.env` 并配置华为云AI接口：
```bash
HUAWEI_AI_API_KEY=your_api_key_here
HUAWEI_AI_ENDPOINT=your_endpoint_here
```

### 4. 启动应用
```bash
python app.py
```

访问 http://127.0.0.1:5000 查看网站

## 页面导航

- **首页** (`/`)：网站介绍和分类导航
- **分类页面** (`/categories`)：所有非遗分类概览
- **分类详情** (`/category/<id>`)：特定分类的项目列表
- **项目详情** (`/item/<id>`)：单个非遗项目的详细信息
- **AI问答** (`/ai-chat`)：智能问答聊天界面

## API接口

- `GET /api/items` - 获取非遗项目列表
- `GET /api/item/<id>` - 获取项目详情
- `GET /api/knowledge` - 获取知识库内容
- `GET /api/search` - 全局搜索
- `POST /api/ai/chat` - AI问答接口

## 设计特色

- **传统美学**：采用中国传统色彩和视觉元素
- **古朴典雅**：避免现代科技感，突出文化底蕴
- **响应式设计**：支持各种设备访问
- **用户体验**：流畅的交互和优雅的动画效果

## 项目结构

```
feiyi/
├── app.py              # 主应用文件
├── huawei_ai.py        # AI接口模块
├── init_data.py        # 数据初始化脚本
├── requirements.txt    # 依赖包列表
├── .env.example        # 环境变量示例
├── instance/
│   └── feiyi.db       # SQLite数据库
└── templates/          # HTML模板
    ├── base.html
    ├── index.html
    ├── categories.html
    ├── category_detail.html
    ├── item_detail.html
    └── ai_chat.html
```

## 开发说明

本项目采用传统文化设计理念，注重：
- 色彩搭配：水墨、朱红、靛蓝等传统色系
- 视觉元素：书法、印章、传统纹样
- 布局设计：简洁留白，注重意境
- 用户体验：沉浸式浏览体验

## 许可证

本项目用于学习和展示目的，请遵守相关法律法规。