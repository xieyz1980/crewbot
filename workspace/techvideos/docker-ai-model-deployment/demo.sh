#!/bin/bash
# ============================================
# Docker AI模型部署 - 视频录制演示脚本
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Docker AI模型部署 - 演示脚本${NC}"
echo -e "${BLUE}============================================${NC}"

# 函数：等待用户按键
wait_for_key() {
    echo ""
    echo -e "${YELLOW}按 Enter 键继续...${NC}"
    read
    echo ""
}

# 步骤1: 检查环境
echo -e "${GREEN}步骤 1: 检查环境${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
echo "检查NVIDIA显卡..."
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
echo ""
echo "检查Docker版本..."
docker --version
echo ""
echo "检查Docker Compose版本..."
docker-compose --version
wait_for_key

# 步骤2: 验证Docker GPU支持
echo -e "${GREEN}步骤 2: 验证Docker GPU支持${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
echo "运行测试容器..."
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi || {
    echo -e "${RED}错误: Docker无法访问GPU${NC}"
    echo "请检查NVIDIA Container Toolkit是否安装"
    exit 1
}
wait_for_key

# 步骤3: 显示项目结构
echo -e "${GREEN}步骤 3: 项目结构${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
tree -L 2 -I '__pycache__|*.pyc|models'
wait_for_key

# 步骤4: 显示Dockerfile内容
echo -e "${GREEN}步骤 4: Dockerfile 配置${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
cat Dockerfile
echo ""
wait_for_key

# 步骤5: 显示docker-compose配置
echo -e "${GREEN}步骤 5: Docker Compose 配置${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
cat docker-compose.yml
echo ""
wait_for_key

# 步骤6: 构建镜像
echo -e "${GREEN}步骤 6: 构建Docker镜像${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
docker-compose build
echo ""
echo -e "${GREEN}镜像构建完成！${NC}"
wait_for_key

# 步骤7: 启动服务
echo -e "${GREEN}步骤 7: 启动服务${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
docker-compose up -d
echo ""
echo "等待服务启动..."
sleep 10
echo -e "${GREEN}服务已启动${NC}"
wait_for_key

# 步骤8: 查看日志
echo -e "${GREEN}步骤 8: 查看服务日志${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
docker-compose logs --tail=50
echo ""
echo -e "${YELLOW}日志显示中... 按 Ctrl+C 退出日志查看${NC}"
wait_for_key

# 步骤9: 测试API
echo -e "${GREEN}步骤 9: 测试API接口${NC}"
echo -e "${BLUE}----------------------------------------${NC}"

echo "测试健康检查..."
curl -s http://localhost:5000/health | python3 -m json.tool

echo ""
echo "测试模型信息..."
curl -s http://localhost:5000/info | python3 -m json.tool

echo ""
echo "测试文本生成..."
curl -s -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "什么是Docker？用中文解释：", "max_length": 200}' | python3 -m json.tool

wait_for_key

# 步骤10: 监控GPU
echo -e "${GREEN}步骤 10: GPU监控${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
echo "运行 nvidia-smi (按 Ctrl+C 停止)..."
nvidia-smi -l 1 || true
wait_for_key

# 步骤11: 清理
echo -e "${GREEN}步骤 11: 清理资源${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
echo "停止服务..."
docker-compose down
echo ""
echo -e "${GREEN}演示完成！${NC}"
echo ""
echo "其他命令:"
echo "  查看所有容器: docker ps -a"
echo "  查看镜像: docker images"
echo "  清理未使用资源: docker system prune"
