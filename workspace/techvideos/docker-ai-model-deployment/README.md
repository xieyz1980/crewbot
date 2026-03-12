# Docker部署开源AI模型 + NVIDIA GPU推理

🚀 使用Docker和NVIDIA GPU快速部署开源大语言模型

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA-GPU-76B900?style=flat&logo=nvidia&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)

## 📋 目录

- [功能特性](#功能特性)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [使用说明](#使用说明)
- [API文档](#api文档)
- [模型推荐](#模型推荐)
- [故障排除](#故障排除)

---

## ✨ 功能特性

- ✅ **GPU加速**: 自动检测并使用NVIDIA显卡进行推理
- ✅ **模型量化**: 4bit量化技术，大幅降低显存需求
- ✅ **REST API**: 提供简单易用的HTTP API接口
- ✅ **批量推理**: 支持批量文本生成，提高效率
- ✅ **模型热切换**: 通过环境变量切换不同模型
- ✅ **自动缓存**: 模型文件自动缓存，避免重复下载

---

## 🖥️ 环境要求

### 硬件要求

| 配置项 | 最低要求 | 推荐配置 |
|--------|----------|----------|
| GPU | NVIDIA GTX 1060 (6GB) | RTX 3060 (12GB) 或更高 |
| 内存 | 8GB | 16GB+ |
| 硬盘 | 10GB 可用空间 | 50GB+ SSD |

### 软件要求

- **操作系统**: Linux (Ubuntu 20.04+), Windows 10/11 + WSL2
- **Docker**: 20.10+ 且已安装 Docker Compose
- **NVIDIA驱动**: 450.80.02+ (推荐最新版)
- **NVIDIA Container Toolkit**: 必须安装

---

## 🚀 快速开始

### 1. 安装NVIDIA Container Toolkit

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 验证安装
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

> **Windows用户**: 确保已安装 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install) 和 [NVIDIA驱动 for WSL](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)

### 2. 克隆项目

```bash
git clone <your-repo-url>
cd docker-ai-model-deployment
```

### 3. 配置环境变量

```bash
# 创建环境变量文件
cp .env.example .env

# 编辑 .env 文件
nano .env
```

`.env` 文件示例:
```
# 模型选择 (HuggingFace模型名称)
MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0

# HuggingFace Token (可选，公开模型不需要)
# 从 https://huggingface.co/settings/tokens 获取
HF_TOKEN=your_token_here
```

### 4. 启动服务

```bash
# 构建并启动
docker-compose up --build -d

# 查看日志
docker-compose logs -f
```

首次启动会下载模型文件（约2-4GB），请耐心等待。

### 5. 测试服务

```bash
# 安装测试脚本依赖
pip install requests

# 运行测试
python test_api.py
```

---

## 📖 使用说明

### 启动服务

```bash
# 前台运行（查看实时日志）
docker-compose up

# 后台运行
docker-compose up -d

# 重新构建后启动
docker-compose up --build -d
```

### 停止服务

```bash
# 停止
docker-compose down

# 停止并删除卷（会删除模型缓存）
docker-compose down -v
```

### 切换模型

编辑 `.env` 文件，修改 `MODEL_NAME` 后重启:

```bash
# 修改 MODEL_NAME 后
docker-compose down
docker-compose up -d
```

---

## 📚 API文档

### 基础信息

- **基础URL**: `http://localhost:5000`
- **Content-Type**: `application/json`

### 接口列表

#### 1. 健康检查
```http
GET /health
```

**响应示例**:
```json
{
  "status": "ok",
  "gpu_available": true,
  "gpu_name": "NVIDIA GeForce RTX 3060",
  "cuda_version": "11.8"
}
```

#### 2. 模型信息
```http
GET /info
```

**响应示例**:
```json
{
  "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  "gpu_available": true,
  "gpu_name": "NVIDIA GeForce RTX 3060",
  "gpu_memory_gb": 12.0,
  "model_loaded": true
}
```

#### 3. 文本生成
```http
POST /generate
Content-Type: application/json

{
  "prompt": "什么是Docker？",
  "max_length": 200,
  "temperature": 0.7,
  "top_p": 0.9
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| prompt | string | 是 | - | 输入提示词 |
| max_length | integer | 否 | 512 | 最大生成长度 |
| temperature | float | 否 | 0.7 | 温度参数 (0-1) |
| top_p | float | 否 | 0.9 | Top-p采样 |

**响应示例**:
```json
{
  "prompt": "什么是Docker？",
  "generated": "Docker是一个开源的容器化平台...",
  "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  "parameters": {
    "max_length": 200,
    "temperature": 0.7,
    "top_p": 0.9
  }
}
```

#### 4. 批量生成
```http
POST /generate_batch
Content-Type: application/json

{
  "prompts": ["问题1", "问题2", "问题3"],
  "max_length": 200,
  "temperature": 0.7
}
```

---

## 🤖 模型推荐

### 入门级 (4-8GB显存)

| 模型 | 参数量 | 显存需求 | 特点 |
|------|--------|----------|------|
| TinyLlama-1.1B | 1.1B | ~2GB | 轻量快速，适合测试 |
| Qwen2-0.5B | 0.5B | ~1GB | 中文支持好 |
| Phi-2 | 2.7B | ~4GB | 微软出品，推理能力强 |

### 进阶级 (8-16GB显存)

| 模型 | 参数量 | 显存需求 | 特点 |
|------|--------|----------|------|
| Llama-2-7B | 7B | ~8GB | Meta开源，通用能力强 |
| Mistral-7B | 7B | ~8GB | 法国Mistral，性能优秀 |
| Qwen2-7B | 7B | ~8GB | 阿里出品，中文优秀 |

### 专业级 (16GB+显存)

| 模型 | 参数量 | 显存需求 | 特点 |
|------|--------|----------|------|
| Llama-2-13B | 13B | ~16GB | 更强的推理能力 |
| Mixtral-8x7B | 47B (MoE) | ~24GB | 专家混合模型 |

---

## 🔧 故障排除

### 1. GPU不可用

**症状**: `/health` 返回 `gpu_available: false`

**解决**:
```bash
# 检查驱动
nvidia-smi

# 检查Docker GPU支持
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# 重启Docker
sudo systemctl restart docker
```

### 2. 显存不足 (OOM)

**症状**: 服务启动时崩溃或生成时出错

**解决**:
- 使用更小的模型 (如 TinyLlama-1.1B)
- 减小 `max_length` 参数
- 确保 `load_in_4bit=True` 已启用

### 3. 模型下载失败

**症状**: 启动时卡在下载步骤

**解决**:
```bash
# 检查网络连接
ping huggingface.co

# 设置镜像（国内用户）
export HF_ENDPOINT=https://hf-mirror.com

# 手动下载模型后挂载
```

### 4. 端口冲突

**症状**: `bind: address already in use`

**解决**:
```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "5001:5000"  # 改为5001
```

---

## 📹 视频教程

本项目的详细视频教程已上传到B站/YouTube:

- [B站: Docker部署AI模型完整教程](your-bilibili-link)
- [YouTube: Deploy AI Models with Docker](your-youtube-link)

---

## 📝 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)
- [Docker](https://www.docker.com/)

---

## 📮 反馈

如有问题或建议，欢迎提交 Issue 或 Pull Request！
