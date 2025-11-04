#!/bin/bash

echo "🌟 启动非遗之光..."
echo "📍 访问地址: http://您的服务器IP:5000"
echo "🛑 停止服务: 按 Ctrl+C"
echo ""

source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 --workers 2 app:app