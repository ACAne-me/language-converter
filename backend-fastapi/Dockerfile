FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    curl \
    git \
    mecab \
    libmecab-dev \
    mecab-ipadic \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 确保unidic-lite被正确安装和初始化
RUN python -c "import unidic_lite; print('Unidic-lite initialized successfully')"

# 复制应用代码
COPY . .

# 设置环境变量以确保fugashi能找到正确的字典路径
ENV MECABRC=""
ENV MECAB_DICDIR="/usr/lib/x86_64-linux-gnu/mecab/dic/ipadic"

# 启动FastAPI服务器 - 添加详细日志
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
