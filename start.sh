#!/bin/bash

echo "=========================================="
echo "数据表格填充 Demo - 快速启动"
echo "=========================================="

# 检查Python环境
echo "1. 检查Python环境..."
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python未安装或不在PATH中"
    exit 1
fi

# 检查依赖
echo "2. 检查依赖..."
python -c "import streamlit, pandas, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  依赖未安装，正在安装..."
    pip install -r requirements.txt
fi

# 运行测试
echo "3. 运行功能测试..."
python test_app.py
if [ $? -ne 0 ]; then
    echo "❌ 测试失败，请检查代码"
    exit 1
fi

# 启动应用
echo "4. 启动Streamlit应用..."
echo "🌐 应用将在浏览器中打开: http://localhost:8501"
echo "📝 按 Ctrl+C 停止应用"
echo "=========================================="

streamlit run app.py --server.port 8501 