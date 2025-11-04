#!/bin/bash

echo "🚀 非遗之光 - Ubuntu 24 一键部署"
echo "================================"

# 更新系统并安装Python
echo "📦 安装Python环境..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# 创建虚拟环境
echo "🔧 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt
pip install gunicorn

# 初始化数据库
echo "🗄️ 初始化数据库..."
python init_data.py

echo ""
echo "✅ 部署完成！"
echo "🚀 启动命令: ./start.sh"
echo "🔗 访问地址: http://您的服务器IP:5000"