# CrewBot

> **轻量级多Agent协作平台**  
> 让每个人都能拥有专属的AI团队

---

## 🚀 5分钟快速开始

### 方式1：Docker一键部署（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/xieyz1980/crewbot.git
cd crewbot

# 2. 一键启动
docker-compose up -d

# 3. 访问 http://localhost:8080
# 默认账号：admin / crewbot123
```

### 方式2：本地安装

```bash
# 1. 克隆仓库
git clone https://github.com/xieyz1980/crewbot.git
cd crewbot

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python -m crewbot

# 4. 访问 http://localhost:8080
```

---

## 📖 使用指南

### 第一步：配置AI模型

1. 打开 Web UI (`http://localhost:8080`)
2. 点击"模型配置"
3. 添加你的API密钥（OpenAI/Claude等）
4. 点击"测试连接"验证

### 第二步：创建Agent

1. 点击"创建Agent"
2. 选择Agent类型（写作/编程/分析等）
3. 配置Agent参数
4. 点击"启动Agent"

### 第三步：开始协作

1. 在对话框输入任务
2. CrewBot自动分配Agent
3. 查看执行结果
4. 与Agent交互优化

---

## 🛠️ 高级配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `CREWBOT_PORT` | 服务端口 | 8080 |
| `CREWBOT_DB` | 数据库路径 | ./data/crewbot.db |
| `CREWBOT_LOG_LEVEL` | 日志级别 | INFO |

### 配置文件

编辑 `config.yaml`：

```yaml
server:
  port: 8080
  host: 0.0.0.0

models:
  openai:
    api_key: ${OPENAI_API_KEY}
  claude:
    api_key: ${CLAUDE_API_KEY}

agents:
  writer:
    model: gpt-4
    temperature: 0.7
  coder:
    model: claude-3-opus
    temperature: 0.2
```

---

## 📁 项目结构

```
crewbot/
├── src/crewbot/          # 核心代码
│   ├── core/            # 核心引擎
│   ├── agent/           # Agent框架
│   ├── router/          # One API Router
│   ├── web/             # Web UI
│   └── utils/           # 工具函数
├── tests/               # 测试用例
├── docs/                # 文档
├── scripts/             # 部署脚本
├── config.yaml          # 配置文件
├── requirements.txt     # 依赖
└── docker-compose.yml   # Docker部署
```

---

## 🧪 运行测试

```bash
# 安装测试依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/ -v

# 生成测试报告
pytest tests/ --cov=crewbot --cov-report=html
```

---

## 🤝 贡献指南

欢迎贡献代码！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

MIT License

---

**让AI协作像呼吸一样自然** 🐾
