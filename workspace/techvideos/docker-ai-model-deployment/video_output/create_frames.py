#!/usr/bin/env python3
"""
生成视频帧 - 使用Python简化ffmpeg调用
"""

import subprocess
import os

FRAMES_DIR = "/workspace/projects/workspace/techvideos/docker-ai-model-deployment/video_output/frames"

def run_ffmpeg(cmd):
    """运行ffmpeg命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def create_simple_frame(filename, bg_color, duration, texts):
    """创建带文字的简单帧"""
    vf_parts = []
    for text, fontfile, fontsize, color, x, y in texts:
        # 转义特殊字符
        text_escaped = text.replace("'", "'\\''")
        vf_parts.append(f"drawtext=text='{text_escaped}':fontfile={fontfile}:fontsize={fontsize}:fontcolor={color}:x={x}:y={y}")
    
    vf_filter = ",".join(vf_parts)
    
    cmd = f"""ffmpeg -f lavfi -i "color=c={bg_color}:s=1920x1080:d={duration}" -vf "{vf_filter}" -pix_fmt yuv420p -y {FRAMES_DIR}/{filename}"""
    return run_ffmpeg(cmd)

# 创建剩余帧
font_mono = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
font_sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# 4. Docker配置标题
print("Creating 04_section2.mp4...")
create_simple_frame("04_section2.mp4", "0x16213e", 3, [
    ("Docker Config", font_sans, 40, "0x00d4ff", 100, 100),
    ("and Build", font_bold, 60, "white", 100, 160),
])

# 5. Dockerfile展示
print("Creating 05_dockerfile.mp4...")
create_simple_frame("05_dockerfile.mp4", "0x1e1e1e", 12, [
    ("Dockerfile", font_bold, 32, "0xffd700", 80, 60),
    ("FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04", font_mono, 22, "white", 80, 120),
    ("WORKDIR /app", font_mono, 22, "white", 80, 160),
    ("RUN apt-get update && apt-get install -y python3", font_mono, 22, "white", 80, 200),
    ("RUN pip3 install torch transformers bitsandbytes flask", font_mono, 22, "white", 80, 240),
    ("COPY app.py /app/", font_mono, 22, "white", 80, 280),
    ("EXPOSE 5000", font_mono, 22, "white", 80, 320),
    ("CMD python3 app.py", font_mono, 22, "white", 80, 360),
])

# 6. docker-compose展示
print("Creating 06_compose.mp4...")
create_simple_frame("06_compose.mp4", "0x1e1e1e", 10, [
    ("docker-compose.yml", font_bold, 32, "0xffd700", 80, 60),
    ("services:", font_mono, 22, "0x569cd6", 80, 110),
    ("llama2-api:", font_mono, 22, "white", 80, 150),
    ("build: .", font_mono, 22, "white", 80, 190),
    ("runtime: nvidia (GPU Enable)", font_mono, 22, "0xff6b6b", 80, 230),
    ("NVIDIA_VISIBLE_DEVICES: all", font_mono, 22, "white", 80, 270),
    ("ports: 5000:5000", font_mono, 22, "white", 80, 310),
    ("devices: driver nvidia, capabilities gpu", font_mono, 22, "white", 80, 350),
])

# 7. 部署演示
print("Creating 07_deploy.mp4...")
create_simple_frame("07_deploy.mp4", "0x0f0f0f", 10, [
    ("docker-compose up --build -d", font_mono, 28, "0x00ff00", 100, 100),
    ("Building llama2-api", font_mono, 20, "0xaaaaaa", 100, 150),
    ("[+] Building 15.2s (8/8) FINISHED", font_mono, 20, "0x00ff00", 100, 180),
    ("=> transferring dockerfile: 496B", font_mono, 18, "0xaaaaaa", 100, 210),
    ("=> FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04", font_mono, 18, "0xaaaaaa", 100, 235),
    ("=> RUN pip3 install torch transformers...", font_mono, 18, "0xaaaaaa", 100, 260),
    ("=> exporting to image", font_mono, 18, "0x00ff00", 100, 285),
    ("[+] Running 1/1", font_mono, 20, "0x00ff00", 100, 330),
    ("Container llama2-gpu Started", font_mono, 20, "0x00ff00", 100, 360),
])

# 8. API测试
print("Creating 08_api_test.mp4...")
create_simple_frame("08_api_test.mp4", "0x0f0f0f", 12, [
    ("curl http://localhost:5000/health", font_mono, 24, "0x00ff00", 80, 80),
    ("{", font_mono, 22, "white", 80, 120),
    ('"status": "ok",', font_mono, 22, "0xffd700", 80, 155),
    ('"gpu_available": true,', font_mono, 22, "0x00ff00", 80, 190),
    ('"gpu_name": "NVIDIA GeForce RTX 3060"', font_mono, 22, "white", 80, 225),
    ("}", font_mono, 22, "white", 80, 260),
    ("POST /generate", font_mono, 20, "0x00ff00", 80, 320),
    ('"prompt": "What is Docker?"', font_mono, 20, "white", 80, 355),
    ('"generated": "Docker is a containerization platform"', font_mono, 20, "0x00ff00", 80, 390),
])

# 9. GPU监控
print("Creating 09_gpu_monitor.mp4...")
create_simple_frame("09_gpu_monitor.mp4", "0x0f0f0f", 8, [
    ("watch -n 1 nvidia-smi", font_mono, 24, "0x00ff00", 100, 100),
    ("GPU 0: RTX 3060", font_mono, 20, "0x00aa00", 100, 150),
    ("Processes: python3 app.py", font_mono, 18, "0x00aa00", 100, 180),
    ("GPU Memory: 6144MiB / 12288MiB", font_mono, 18, "0xff6b6b", 100, 210),
    ("GPU Util: 85%", font_mono, 18, "0x00ff00", 100, 240),
    ("GPU Inference Running!", font_sans, 32, "0x00ff00", 100, 300),
    ("VRAM Usage: ~6GB", font_sans, 24, "0xaaaaaa", 100, 350),
    ("10-20x faster than CPU", font_sans, 24, "0xaaaaaa", 100, 390),
])

# 10. 结尾总结
print("Creating 10_summary.mp4...")
create_simple_frame("10_summary.mp4", "0x1a1a2e", 8, [
    ("Summary", font_bold, 60, "0x00d4ff", 700, 100),
    ("Install NVIDIA Container Toolkit", font_sans, 36, "white", 500, 220),
    ("Write Dockerfile for AI Model", font_sans, 36, "white", 500, 280),
    ("Configure GPU Access", font_sans, 36, "white", 500, 340),
    ("Test Inference API", font_sans, 36, "white", 500, 400),
    ("Monitor GPU Performance", font_sans, 36, "white", 500, 460),
    ("Code on GitHub", font_sans, 28, "0xffd700", 750, 580),
])

print("\nAll frames created!")
