# CrewBot 使用说明

> 🎯 **目标**：让不懂IT的用户5分钟上手CrewBot

---

## 📦 安装

### 方式1：Docker一键部署（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/xieyz1980/crewbot.git
cd crewbot

# 2. 一键启动
docker-compose up -d

# 3. 访问 http://localhost:8080
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
```

---

## ⚙️ 第一步：配置AI模型（2分钟）

### 1. 打开配置页面
打开浏览器，访问 `http://localhost:8080/models`

### 2. 添加API密钥
CrewBot支持多种AI模型，您需要配置至少一个：

| 模型 | 获取方式 | 费用 |
|------|---------|------|
| OpenAI GPT-4 | [OpenAI官网](https://platform.openai.com) | 按量付费 |
| Claude 3 | [Anthropic官网](https://anthropic.com) | 按量付费 |
| 阿里通义千问 | [阿里云](https://dashscope.aliyun.com) | 有免费额度 |
| DeepSeek | [DeepSeek官网](https://deepseek.com) | 有免费额度 |

### 3. 环境变量配置

在运行目录创建 `.env` 文件：

```bash
# OpenAI（可选）
OPENAI_API_KEY=sk-your-key-here

# Claude（可选）
ANTHROPIC_API_KEY=sk-ant-your-key-here

# 阿里通义千问（可选）
QIANWEN_API_KEY=sk-your-key-here

# DeepSeek（可选）
DEEPSEEK_API_KEY=sk-your-key-here
```

> 💡 **提示**：不需要配置所有模型，配1-2个即可开始使用

---

## 🚀 第二步：开始使用（3分钟）

### 1. 进入主页
访问 `http://localhost:8080`

### 2. 发送任务
在对话框输入您的需求，例如：

```
帮我写一篇关于人工智能的文章，800字左右，适合技术博客
```

### 3. 查看结果
CrewBot会：
- 🧠 自动分析任务类型
- 🤖 选择最适合的Agent
- 🎯 选择最优的AI模型
- ✨ 生成结果并展示

---

## 👥 内置Agent介绍

CrewBot内置了3个专业Agent：

### 1. ✍️ 写作Agent（Writer）
**擅长**：
- 撰写文章、报告、博客
- 文案创作
- 翻译润色
- 编辑校对

**使用示例**：
```
写一篇关于新能源汽车的市场分析报告
```

### 2. 💻 编程Agent（Coder）
**擅长**：
- 代码编写
- Bug调试
- 代码审查
- 技术文档

**使用示例**：
```
写一个Python函数，实现斐波那契数列
```

### 3. 📊 分析Agent（Analyst）
**擅长**：
- 数据分析
- 趋势洞察
- 生成图表建议
- 研究报告

**使用示例**：
```
分析2024年AI行业的发展趋势
```

---

## 💡 使用技巧

### 技巧1：明确任务类型

✅ **好的提示**：
```
写一篇技术博客，介绍Python异步编程，包含代码示例，面向初学者
```

❌ **模糊的提示**：
```
写代码
```

### 技巧2：提供上下文

✅ **好的提示**：
```
我在做一个电商网站，需要一个用户注册页面，包含手机号验证功能
```

### 技巧3：分步复杂任务

复杂任务可以分解：
1. 先让Agent写大纲
2. 再逐段完善
3. 最后整体润色

---

## 🔧 高级功能

### 1. Agent管理
访问 `http://localhost:8080/agents` 可以：
- 查看所有Agent
- 查看Agent详情
- 配置Agent参数

### 2. 任务管理
访问 `http://localhost:8080/tasks` 可以：
- 查看任务历史
- 查看执行状态
- 取消进行中的任务

### 3. 模型选择
CrewBot会**自动**选择最优模型，但您可以指定：

```
使用GPT-4写一篇关于量子计算的文章
```

---

## 💰 成本控制

### 查看预估费用
CrewBot会在每次回复后显示预估费用，例如：
```
模型: gpt-3.5-turbo | 费用估算: $0.0023
```

### 自动成本优化
CrewBot会自动：
- 简单任务使用便宜模型（GPT-3.5）
- 复杂任务使用强模型（GPT-4/Claude）
- 节省30-50%的费用

### 设置预算上限
在 `config.yaml` 中设置：
```yaml
budget:
  daily_limit: 10  # 每日预算上限$10
  alert_threshold: 0.8  # 80%时告警
```

---

## 🆘 常见问题

### Q1: 提示"没有可用的模型"
**原因**：没有配置API密钥
**解决**：按照"第一步：配置AI模型"配置至少一个API密钥

### Q2: 任务执行失败
**原因**：API密钥无效或模型服务异常
**解决**：
1. 检查API密钥是否正确
2. 检查网络连接
3. 查看日志 `docker logs crewbot`

### Q3: 如何更换模型？
**答**：CrewBot会自动选择，也可以在提示中指定：
```
使用Claude-3写一篇故事
```

### Q4: 支持中文吗？
**答**：完全支持！所有Agent都针对中文优化

### Q5: 数据安全吗？
**答**：
- 所有数据存储在本地
- API调用直接发送到模型提供商
- 不会上传到第三方服务器

---

## 📞 获取帮助

- 📧 邮箱：support@crewbot.ai
- 💬 Discord：[CrewBot社区](https://discord.gg/crewbot)
- 🐛 问题反馈：[GitHub Issues](https://github.com/xieyz1980/crewbot/issues)

---

## 🎉 开始您的AI协作之旅！

现在就去 `http://localhost:8080` 试试吧！

**让AI协作像呼吸一样自然** 🤖✨