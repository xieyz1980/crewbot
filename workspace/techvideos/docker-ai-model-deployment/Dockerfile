# 使用NVIDIA CUDA基础镜像
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 设置工作目录
WORKDIR /app

# 安装Python和依赖
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 安装Python包
RUN pip3 install --no-cache-dir \
    torch \
    transformers \
    accelerate \
    bitsandbytes \
    flask \
    huggingface-hub

# 复制应用代码
COPY app.py /app/
COPY requirements.txt /app/

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python3", "app.py"]
