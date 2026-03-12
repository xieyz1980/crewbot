# Docker部署开源AI模型 + NVIDIA显卡推理 视频教程

## 📹 视频信息

- **标题**: Docker部署开源AI模型并调用NVIDIA显卡进行推理 - 完整实战教程
- **时长**: 约15-20分钟
- **难度**: 初中级
- **目标观众**: 开发者、AI爱好者、DevOps工程师

---

## 🎬 视频脚本

### 开场 (0:00-0:30)

**[画面: 电脑桌面，打开终端]**

**旁白:**
> "大家好，欢迎来到本期的技术实战教程。今天我将带大家从零开始，学习如何在Docker中部署开源AI大模型，并配置NVIDIA显卡进行GPU加速推理。无论你是想本地部署LLM，还是搭建AI服务，这个教程都能帮到你。"

---

### 第一部分：环境准备 (0:30-3:00)

#### 1.1 检查NVIDIA显卡

**[画面: 终端输入命令]**

```bash
# 查看显卡信息
nvidia-smi
```

**旁白:**
> "首先，确保你的机器有NVIDIA显卡。运行nvidia-smi命令，如果看到显卡信息，说明驱动已安装。"

**[画面: 显示显卡信息输出]**

#### 1.2 安装NVIDIA Container Toolkit

**[画面: 终端逐行输入命令]**

```bash
# 添加NVIDIA仓库
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# 安装工具包
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 重启Docker服务
sudo systemctl restart docker
```

**旁白:**
> "要让Docker使用GPU，需要安装NVIDIA Container Toolkit。这是NVIDIA官方提供的工具，让容器可以访问宿主机的GPU资源。"

#### 1.3 验证GPU支持

**[画面: 终端运行测试命令]**

```bash
# 测试Docker GPU访问
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

**旁白:**
> "运行这个测试命令，如果在容器内也能看到显卡信息，说明配置成功了。"

---

### 第二部分：部署开源模型 (3:00-8:00)

#### 2.1 选择模型 - 以Llama 2为例

**[画面: 浏览器打开Hugging Face网站]**

**旁白:**
> "今天我们以Meta的Llama 2模型为例。这是一个开源的大语言模型，性能优秀，适合本地部署。你也可以选择其他模型，比如Mistral、Qwen等。"

#### 2.2 创建项目结构

**[画面: 终端创建文件夹]**

```bash
mkdir -p ~/ai-models/llama2-docker
cd ~/ai-models/llama2-docker
```

#### 2.3 编写Dockerfile

**[画面: 编辑器打开Dockerfile]**

```dockerfile
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
    flask

# 复制应用代码
COPY app.py /app/

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python3", "app.py"]
```

**旁白:**
> "这个Dockerfile基于NVIDIA的CUDA镜像，安装了PyTorch和相关的AI库。注意我们使用了bitsandbytes库来进行模型量化，这样可以在消费级显卡上运行大模型。"

#### 2.4 编写应用代码

**[画面: 编辑器打开app.py]**

```python
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

app = Flask(__name__)

# 全局变量存储模型和tokenizer
model = None
tokenizer = None

def load_model():
    """加载模型到GPU"""
    global model, tokenizer
    
    model_name = os.getenv('MODEL_NAME', 'meta-llama/Llama-2-7b-chat-hf')
    
    print(f"正在加载模型: {model_name}")
    
    # 加载tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # 加载模型到GPU，使用4bit量化节省显存
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map='auto',
        load_in_4bit=True
    )
    
    print("模型加载完成！")

@app.route('/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'gpu': torch.cuda.is_available()})

@app.route('/generate', methods=['POST'])
def generate():
    """文本生成接口"""
    data = request.json
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 512)
    temperature = data.get('temperature', 0.7)
    
    # 编码输入
    inputs = tokenizer(prompt, return_tensors='pt').to('cuda')
    
    # 生成文本
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # 解码输出
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return jsonify({
        'prompt': prompt,
        'generated': generated_text,
        'model': 'llama2-7b'
    })

if __name__ == '__main__':
    # 启动时加载模型
    load_model()
    
    # 启动Flask服务
    app.run(host='0.0.0.0', port=5000)
```

**旁白:**
> "这是我们的推理服务代码。使用Flask创建了一个简单的API服务，包含健康检查和文本生成两个接口。关键点是device_map='auto'和load_in_4bit，这让模型自动分配到GPU并使用4bit量化，7B模型只需要约8GB显存。"

#### 2.5 编写docker-compose配置

**[画面: 编辑器打开docker-compose.yml]**

```yaml
version: '3.8'

services:
  llama2-api:
    build: .
    container_name: llama2-gpu
    runtime: nvidia  # 关键：启用NVIDIA运行时
    environment:
      - NVIDIA_VISIBLE_DEVICES=all  # 使用所有GPU
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
      - MODEL_NAME=meta-llama/Llama-2-7b-chat-hf
      - HF_TOKEN=${HF_TOKEN}  # HuggingFace token
    ports:
      - "5000:5000"
    volumes:
      - ./models:/root/.cache/huggingface  # 缓存模型文件
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped
```

**旁白:**
> "docker-compose.yml是部署配置的核心。runtime: nvidia是关键配置，让容器可以使用GPU。我们还挂载了模型缓存目录，这样重复启动时不需要重新下载模型。"

---

### 第三部分：构建和运行 (8:00-12:00)

#### 3.1 设置HuggingFace Token

**[画面: 终端设置环境变量]**

```bash
# 从HuggingFace获取token：https://huggingface.co/settings/tokens
export HF_TOKEN="your_token_here"
```

**旁白:**
> "Llama 2模型需要HuggingFace的访问token。先去官网申请，然后设置环境变量。"

#### 3.2 构建镜像

**[画面: 终端运行构建命令]**

```bash
docker-compose build
```

**旁白:**
> "现在构建Docker镜像。这个过程会下载基础镜像和安装Python依赖，可能需要几分钟。"

#### 3.3 启动服务

**[画面: 终端启动服务]**

```bash
docker-compose up -d
```

**旁白:**
> "使用docker-compose up -d在后台启动服务。第一次启动会下载模型文件，大约4GB，需要一些时间。"

#### 3.4 查看日志

**[画面: 终端查看日志]**

```bash
docker-compose logs -f
```

**旁白:**
> "通过日志可以看到模型下载和加载的进度。当看到'模型加载完成'时，服务就准备好了。"

---

### 第四部分：测试和验证 (12:00-16:00)

#### 4.1 健康检查

**[画面: 终端测试API]**

```bash
# 测试服务状态
curl http://localhost:5000/health
```

**[画面: 显示JSON响应]**

```json
{
  "status": "ok",
  "gpu": true
}
```

**旁白:**
> "首先测试健康检查接口，确认GPU可用。"

#### 4.2 文本生成测试

**[画面: 终端发送生成请求]**

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "解释什么是Docker，用中文回答：",
    "max_length": 200,
    "temperature": 0.7
  }'
```

**[画面: 显示生成的文本]**

**旁白:**
> "发送一个文本生成请求，让模型解释Docker的概念。temperature参数控制输出的随机性，值越低输出越确定。"

#### 4.3 监控GPU使用

**[画面: 新开终端，运行nvidia-smi]**

```bash
# 每隔1秒刷新
watch -n 1 nvidia-smi
```

**[画面: 显示GPU使用率和显存占用]**

**旁白:**
> "可以看到推理时GPU的利用率上升，显存占用约6-8GB。这证明模型确实在GPU上运行。"

#### 4.4 性能对比 (可选)

**[画面: 分屏显示CPU和GPU推理速度]**

**旁白:**
> "对比一下，同样的模型在CPU上可能需要几十秒才能生成，而在GPU上只需要1-2秒。"

---

### 第五部分：进阶和清理 (16:00-19:00)

#### 5.1 使用其他模型

**[画面: 编辑器修改docker-compose.yml]**

```yaml
environment:
  # 可以换成其他模型
  - MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
  # 或者国产模型
  # - MODEL_NAME=Qwen/Qwen-7B-Chat
```

**旁白:**
> "想换其他模型？只需要修改MODEL_NAME环境变量。支持HuggingFace上的任何兼容模型。"

#### 5.2 批量推理优化

**[画面: 展示优化后的代码片段]**

```python
# 批量处理提高效率
@app.route('/generate_batch', methods=['POST'])
def generate_batch():
    data = request.json
    prompts = data.get('prompts', [])
    
    # 批量编码
    inputs = tokenizer(prompts, return_tensors='pt', padding=True).to('cuda')
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    
    results = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return jsonify({'results': results})
```

**旁白:**
> "对于批量推理，可以把多个请求合并处理，效率更高。"

#### 5.3 清理资源

**[画面: 终端执行清理命令]**

```bash
# 停止服务
docker-compose down

# 删除镜像（可选）
docker rmi llama2-docker_llama2-api

# 查看磁盘使用
docker system df
```

**旁白:**
> "测试完成后，记得清理资源。docker-compose down停止服务，docker system df查看Docker磁盘使用情况。"

---

### 结尾 (19:00-20:00)

**[画面: 回到桌面，总结要点]**

**旁白:**
> "今天我们完成了：
> 1. 安装NVIDIA Container Toolkit
> 2. 编写Dockerfile部署AI模型
> 3. 配置GPU访问
> 4. 测试推理API
> 5. 监控GPU性能
>
> 所有代码都上传到GitHub了，链接在视频描述。有问题欢迎在评论区讨论。
> 如果你喜欢这个教程，请点赞订阅，我们下期再见！"

**[画面: 结束画面，显示GitHub链接和二维码]**

---

## 📦 配套文件清单

```
docker-ai-model-deployment/
├── Dockerfile              # Docker镜像构建文件
├── docker-compose.yml      # Docker Compose配置
├── app.py                  # Flask API服务代码
├── requirements.txt        # Python依赖列表
├── test_api.py            # API测试脚本
├── README.md              # 项目说明
└── VIDEO_SCRIPT.md        # 本视频脚本
```

---

## 🎯 学习要点总结

1. **NVIDIA Container Toolkit** - 让Docker容器访问GPU的关键工具
2. **CUDA基础镜像** - nvidia/cuda系列镜像自带GPU支持
3. **runtime: nvidia** - docker-compose中启用GPU的关键配置
4. **模型量化** - load_in_4bit=True大幅降低显存需求
5. **device_map='auto'** - 自动分配模型到可用GPU
6. **volume挂载** - 缓存模型文件避免重复下载

---

## 🔗 相关链接

- [NVIDIA Container Toolkit文档](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [Llama 2模型页面](https://huggingface.co/meta-llama)
- [Docker GPU文档](https://docs.docker.com/compose/gpu-support/)

---

*视频制作日期: 2026-03-12*
