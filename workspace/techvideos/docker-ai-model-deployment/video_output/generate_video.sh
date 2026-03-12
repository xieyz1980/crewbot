#!/bin/bash
# ============================================
# Docker AI模型部署教程 - 视频生成脚本
# ============================================

set -e

OUTPUT_DIR="/workspace/projects/workspace/techvideos/docker-ai-model-deployment/video_output"
AUDIO_DIR="$OUTPUT_DIR/audio"
FRAMES_DIR="$OUTPUT_DIR/frames"

mkdir -p "$FRAMES_DIR"

echo "=== 生成视频帧 ==="

# 1. 开场标题 (5秒)
ffmpeg -f lavfi -i "color=c=0x1a1a2e:s=1920x1080:d=5" \
  -vf "
    drawtext=text='Docker部署开源AI模型':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=80:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-50,
    drawtext=text='+ NVIDIA GPU加速推理':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=50:fontcolor=0x00d4ff:x=(w-text_w)/2:y=(h-text_h)/2+50,
    drawtext=text='完整实战教程':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=40:fontcolor=0xaaaaaa:x=(w-text_w)/2:y=(h-text_h)/2+120
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/01_title.mp4"

# 2. 环境准备标题 (3秒)
ffmpeg -f lavfi -i "color=c=0x16213e:s=1920x1080:d=3" \
  -vf "
    drawtext=text='第一部分':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=40:fontcolor=0x00d4ff:x=100:y=100,
    drawtext=text='环境准备与GPU配置':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=60:fontcolor=white:x=100:y=160
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/02_section1.mp4"

# 3. NVIDIA命令演示 (10秒)
ffmpeg -f lavfi -i "color=c=0x0f0f0f:s=1920x1080:d=10" \
  -vf "
    drawtext=text='nvidia-smi':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=30:fontcolor=0x00ff00:x=100:y=100,
    drawtext=text='检查NVIDIA显卡驱动':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=24:fontcolor=0xaaaaaa:x=100:y=150,
    drawtext=text='+-----------------------------------------------------------------------------+':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=200,
    drawtext=text='| NVIDIA-SMI 535.104.05    Driver Version: 535.104.05    CUDA Version: 12.2     |':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=225,
    drawtext=text='|-------------------------------+----------------------+----------------------+':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=250,
    drawtext=text='| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=275,
    drawtext=text='| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=300,
    drawtext=text='|   0  RTX 3060       Off       | 00000000:01:00.0  On |                  N/A |':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y:325,
    drawtext=text='|  0%   45C    P8    15W / 170W |    512MiB / 12288MiB |      0%      Default |':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y:350,
    drawtext=text='+-----------------------------------------------------------------------------+':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y:400
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/03_nvidia_smi.mp4"

# 4. Docker配置标题 (3秒)
ffmpeg -f lavfi -i "color=c=0x16213e:s=1920x1080:d=3" \
  -vf "
    drawtext=text='第二部分':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=40:fontcolor=0x00d4ff:x=100:y=100,
    drawtext=text='Docker配置与镜像构建':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=60:fontcolor=white:x=100:y=160
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/04_section2.mp4"

# 5. Dockerfile展示 (12秒)
ffmpeg -f lavfi -i "color=c=0x1e1e1e:s=1920x1080:d=12" \
  -vf "
    drawtext=text='Dockerfile':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=32:fontcolor=0xffd700:x=80:y=60,
    drawtext=text='# 使用NVIDIA CUDA基础镜像':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=0x608b4e:x=80:y=120,
    drawtext=text='FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=155,
    drawtext=text='WORKDIR /app':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=190,
    drawtext=text='# 安装Python和依赖':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=0x608b4e:x=80:y=235,
    drawtext=text='RUN apt-get update && apt-get install -y python3 python3-pip':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=270,
    drawtext=text='# 安装AI库':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=0x608b4e:x=80:y=315,
    drawtext=text='RUN pip3 install torch transformers accelerate bitsandbytes flask':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=350,
    drawtext=text='COPY app.py /app/':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=395,
    drawtext=text='EXPOSE 5000':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=430,
    drawtext=text='CMD [\"python3\", \"app.py\"]':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=465
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/05_dockerfile.mp4"

# 6. docker-compose展示 (10秒)
ffmpeg -f lavfi -i "color=c=0x1e1e1e:s=1920x1080:d=10" \
  -vf "
    drawtext=text='docker-compose.yml':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=32:fontcolor=0xffd700:x=80:y=60,
    drawtext=text='services:':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=0x569cd6:x=80:y=110,
    drawtext=text='  llama2-api:':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=145,
    drawtext=text='    build: .':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=180,
    drawtext=text='    runtime: nvidia  # 启用GPU':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=0xff6b6b:x=80:y=215,
    drawtext=text='    environment:':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=250,
    drawtext=text='      - NVIDIA_VISIBLE_DEVICES=all':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=285,
    drawtext=text='      - MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=320,
    drawtext=text='    ports:':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=355,
    drawtext=text='      - \"5000:5000\"':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=390,
    drawtext=text='    deploy:':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=425,
    drawtext=text='      resources:':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=460,
    drawtext=text='        reservations:':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=495,
    drawtext=text='          devices: [{driver: nvidia, count: all, capabilities: [gpu]}]':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=530
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/06_compose.mp4"

# 7. 部署演示 (10秒)
ffmpeg -f lavfi -i "color=c=0x0f0f0f:s=1920x1080:d=10" \
  -vf "
    drawtext=text='$ docker-compose up --build -d':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=28:fontcolor=0x00ff00:x=100:y=100,
    drawtext=text='Building llama2-api':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=20:fontcolor=0xaaaaaa:x=100:y=150,
    drawtext=text='[+] Building 15.2s (8/8) FINISHED':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=20:fontcolor=0x00ff00:x=100:y=180,
    drawtext=text=' => => transferring dockerfile: 496B':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0xaaaaaa:x=100:y=210,
    drawtext=text=' => => transferring context: 2.34kB':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0xaaaaaa:x=100:y=235,
    drawtext=text=' => [1/5] FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0xaaaaaa:x=100:y=260,
    drawtext=text=' => [2/5] RUN apt-get update && apt-get install -y python3':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0xaaaaaa:x=100:y=285,
    drawtext=text=' => [3/5] RUN pip3 install torch transformers...':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0xaaaaaa:x=100:y=310,
    drawtext=text=' => [4/5] COPY app.py /app/':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0xaaaaaa:x=100:y=335,
    drawtext=text=' => exporting to image':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00ff00:x=100:y=360,
    drawtext=text=' => => naming to docker.io/library/docker-ai-model':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00ff00:x=100:y=385,
    drawtext=text='[+] Running 1/1':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=20:fontcolor=0x00ff00:x=100:y=430,
    drawtext=text=' ✔ Container llama2-gpu  Started':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=20:fontcolor=0x00ff00:x=100:y=460
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/07_deploy.mp4"

# 8. API测试 (12秒)
ffmpeg -f lavfi -i "color=c=0x0f0f0f:s=1920x1080:d=12" \
  -vf "
    drawtext=text='$ curl http://localhost:5000/health':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=24:fontcolor=0x00ff00:x=80:y=80,
    drawtext=text='{':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=120,
    drawtext=text='  \"status\": \"ok\",':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=0xffd700:x=80:y=155,
    drawtext=text='  \"gpu_available\": true,':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=0x00ff00:x=80:y=190,
    drawtext=text='  \"gpu_name\": \"NVIDIA GeForce RTX 3060\"':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=225,
    drawtext=text='}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=260,
    drawtext=text='$ curl -X POST http://localhost:5000/generate -H \"Content-Type: application/json\"':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=20:fontcolor=0x00ff00:x=80:y=320,
    drawtext=text='  -d \'{\"prompt\": \"什么是Docker？\", \"max_length\": 200}\'':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=20:fontcolor=0x00ff00:x=80:y=350,
    drawtext=text='{':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=400,
    drawtext=text='  \"prompt\": \"什么是Docker？\",':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=20:fontcolor=white:x=80:y=435,
    drawtext=text='  \"generated\": \"Docker是一个开源的容器化平台...\",':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=20:fontcolor=0x00ff00:x=80:y=470,
    drawtext=text='  \"model\": \"TinyLlama/TinyLlama-1.1B-Chat-v1.0\"':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=20:fontcolor=white:x=80:y=505,
    drawtext=text='}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=22:fontcolor=white:x=80:y=540
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/08_api_test.mp4"

# 9. GPU监控 (8秒)
ffmpeg -f lavfi -i "color=c=0x0f0f0f:s=1920x1080:d=8" \
  -vf "
    drawtext=text='$ watch -n 1 nvidia-smi':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=24:fontcolor=0x00ff00:x=100:y=100,
    drawtext=text='+-----------------------------------------------------------------------------+':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=150,
    drawtext=text='| Processes:                                                                  |':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=175,
    drawtext=text='|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=200,
    drawtext=text='|        ID   ID                                                   Usage      |':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=225,
    drawtext=text='|=============================================================================|':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=250,
    drawtext=text='|    0   N/A  N/A    123456      C   python3 app.py                 6144MiB |':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0xff6b6b:x=100:y=275,
    drawtext=text='+-----------------------------------------------------------------------------+':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=0x00aa00:x=100:y=300,
    drawtext=text='':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontsize=18:fontcolor=white:x=100:y=340,
    drawtext=text='👆 GPU推理正在进行中！':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=32:fontcolor=0x00ff00:x=100:y=380,
    drawtext=text='显存占用约 6GB，推理速度比CPU快 10-20倍':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=24:fontcolor=0xaaaaaa:x=100:y=430
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/09_gpu_monitor.mp4"

# 10. 结尾总结 (8秒)
ffmpeg -f lavfi -i "color=c=0x1a1a2e:s=1920x1080:d=8" \
  -vf "
    drawtext=text='教程总结':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=60:fontcolor=0x00d4ff:x=(w-text_w)/2:y=150,
    drawtext=text='✅ 安装NVIDIA Container Toolkit':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=36:fontcolor=white:x=(w-text_w)/2:y=280,
    drawtext=text='✅ 编写Dockerfile部署AI模型':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=36:fontcolor=white:x=(w-text_w)/2:y=340,
    drawtext=text='✅ 配置GPU访问权限':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=36:fontcolor=white:x=(w-text_w)/2:y=400,
    drawtext=text='✅ 测试推理API':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=36:fontcolor=white:x=(w-text_w)/2:y=460,
    drawtext=text='✅ 监控GPU性能':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=36:fontcolor=white:x=(w-text_w)/2:y=520,
    drawtext=text='代码已上传到GitHub，链接见视频描述':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=28:fontcolor=0xffd700:x=(w-text_w)/2:y=620
  " \
  -pix_fmt yuv420p -y "$FRAMES_DIR/10_summary.mp4"

echo "=== 视频帧生成完成 ==="
ls -la "$FRAMES_DIR/"
