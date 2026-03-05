# 🤖 CrewBot

> **轻量级多Agent协作平台**  
> 一键部署 · 智能路由 · 多端支持

[![GitHub stars](https://img.shields.io/github/stars/xieyz1980/crewbot?style=social)](https://github.com/xieyz1980/crewbot)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

---

## 🎯 愿景

让每个人都能拥有专属的AI团队。

就像一艘船上的船员们各司其职、协作配合，CrewBot让多个AI Agent协同工作，共同完成复杂任务。

---

## ✨ 核心特性

### 🚀 一键部署
```bash
# 企业版一键安装
curl -fsSL https://crewbot.ai/install.sh | bash -s -- --edition enterprise

# 个人版一键安装
curl -fsSL https://crewbot.ai/install.sh | bash -s -- --edition personal

# 树莓派版一键安装
curl -fsSL https://crewbot.ai/install.sh | bash -s -- --edition edge
```

### 🎨 可视化配置
- Web UI界面，零代码配置
- 模块化选择：需要哪些Agent能力，勾选即可
- 实时预览：配置即时生效，所见即所得

### 🧠 智能模型路由 (One API)
```python
# 自动选择最优模型，为用户节省Token成本
task = "写一段Python代码"
model = crewbot.select_model(task)
# → 选择 GPT-4-mini (代码任务，轻量模型足够)

task = "分析复杂架构设计"
model = crewbot.select_model(task)
# → 选择 Claude-3-Opus (复杂推理，需要强模型)
```

### 📱 多端支持
| 平台 | 支持情况 | 性能要求 |
|------|---------|---------|
| 云服务器 | ✅ 完整功能 | 4核8G+ |
| 个人电脑 | ✅ 标准功能 | 2核4G+ |
| 手机/平板 | ✅ 轻量模式 |  ARM芯片 |
| 树莓派 | ✅ 边缘模式 | 4B (4GB) |
| 车载系统 | 🔄 开发中 | 车规级芯片 |

### 🏢 企业级特性
- **团队协作**：多用户、多角色、权限管理
- **审计日志**：全程可追溯
- **SSO集成**：企业微信、钉钉、飞书
- **私有化部署**：数据不出域

### 🏠 个人版特性
- **即开即用**：5分钟搭建个人AI助理团队
- **低资源占用**：树莓派也能流畅运行
- **隐私优先**：本地运行，数据不上云

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                        CrewBot                              │
│                    (编排调度中心)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────┐    ┌─────▼──────┐   ┌─────▼──────┐
│ Agent  │    │   Agent    │   │   Agent    │
│ 写作   │    │   编程     │   │   分析     │
└───┬────┘    └─────┬──────┘   └─────┬──────┘
    │               │                │
    └───────────────┼────────────────┘
                    │
         ┌──────────▼──────────┐
         │    One API 路由层    │
         │   (智能模型选择)     │
         └──────────┬──────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───▼───┐    ┌─────▼─────┐   ┌────▼────┐
│ GPT-4 │    │ Claude-3  │   │ 本地模型 │
│  系列 │    │   系列    │   │ llama3  │
└───────┘    └───────────┘   └─────────┘
```

---

## 🚦 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/xieyz1980/crewbot.git
cd crewbot

# 一键安装
./install.sh
```

### 2. 配置

```bash
# 启动Web配置界面
crewbot config --ui

# 或命令行配置
crewbot config --set model.gpt4.enabled=true
```

### 3. 运行

```bash
# 启动CrewBot
crewbot start

# 查看状态
crewbot status

# 查看日志
crewbot logs
```

### 4. 使用

```python
from crewbot import Crew, Agent

# 创建你的AI团队
writer = Agent(name="写手", skills=["writing", "editing"])
coder = Agent(name="程序员", skills=["coding", "debugging"])
analyst = Agent(name="分析师", skills=["research", "analysis"])

# 组建Crew
crew = Crew(agents=[writer, coder, analyst])

# 分配任务
result = crew.execute("帮我写一篇关于AI基础设施的技术文章")
```

---

## 📚 使用场景

### 场景1: 企业研发团队 👔
```
项目经理Jim: 任务分解Agent
产品经理Dora: 需求分析Agent
程序员James: 代码开发Agent  
测试Eddy: 质量保障Agent
文档Jason: 技术写作Agent

协作流程: Jim分解 → Dora分析 → James开发 → Eddy测试 → Jason文档
效果: 开发周期缩短50%，代码质量提升
```

### 场景2: 个人AI助理 🏠
```
日程Agent: 管理时间和任务
写作Agent: 协助内容创作
研究Agent: 收集资料和信息
学习Agent: 总结和复习

一天的工作:
09:00 日程Agent提醒今日任务
10:00 写作Agent协助写书
14:00 研究Agent收集行业动态
20:00 学习Agent总结今日收获
```

### 场景3: 边缘设备部署 📱
```
树莓派 + CrewBot = 家庭智能中枢
- 语音助手
- 家居控制
- 本地知识库
- 隐私保护

无需联网，完全本地运行
```

---

## 🗺️ 路线图

### Phase 1: MVP (2026 Q1) ✅ 当前
- [ ] 核心Agent框架
- [ ] One API智能路由
- [ ] 一键安装脚本
- [ ] Web UI配置界面
- [ ] 基础文档和示例

### Phase 2: 企业版 (2026 Q2)
- [ ] 团队协作功能
- [ ] SSO集成
- [ ] 审计日志
- [ ] 私有化部署方案
- [ ] 企业SLA支持

### Phase 3: 边缘版 (2026 Q3)
- [ ] 端侧优化
- [ ] 模型量化
- [ ] 离线运行
- [ ] 手机APP
- [ ] 车载系统集成

### Phase 4: 生态 (2026 Q4)
- [ ] Agent市场
- [ ] 插件系统
- [ ] 社区贡献
- [ ] 企业认证

---

## 💡 核心设计理念

### 1. 简单至上
> "如果一个工具需要看30页文档才能用，那它不够好。"

- 5分钟上手
- 零代码配置
- 一键部署

### 2. 智能路由
> "用大模型做小事是浪费，用小模型做大事是灾难。"

- 自动选择最优模型
- 为用户节省Token成本
- 平衡质量与成本

### 3. 随处可用
> "AI能力应该像空气一样，随处可得。"

- 云端、本地、边缘，处处可用
- 手机、电脑、树莓派，设备不限
- 在线、离线、弱网，场景全覆盖

### 4. 隐私优先
> "数据是用户的，不是平台的。"

- 本地运行，数据不出域
- 端到端加密
- 用户完全控制

---

## 🤝 与OpenClaw的关系

CrewBot是对OpenClaw的**轻量级重构和优化**：

| 特性 | OpenClaw | CrewBot |
|------|----------|---------|
| 架构 | 完整但复杂 | 轻量且模块化 |
| 配置 | YAML文件 | Web UI + 一键脚本 |
| 部署 | 需要专业知识 | 一键安装 |
| 模型 | 单一模型 | One API智能路由 |
| 硬件 | 服务器级 | 从云端到树莓派 |
| 定位 | 企业级平台 | 全民可用工具 |

**致敬**：CrewBot建立在OpenClaw的优秀设计之上，感谢OpenClaw团队的开源贡献。

---

## 📖 相关资源

- 📚 **《智算基石》**: AI基础设施技术专著（谢友泽著，2026年出版）
  - 第10章深度分析了CrewBot的技术架构
  - 包含多Agent协作的理论与实践

- 🎓 **技术博客**: [LinkedIn - 谢友泽](https://linkedin.com/in/youze-xie-ai)
  - 分享AI架构和Agent技术

- 💬 **社区讨论**: [GitHub Discussions](../../discussions)
  - 使用问题、功能建议、技术交流

---

## 🛠️ 技术栈

- **核心**: Python 3.9+
- **编排**: 自研轻量级调度器
- **通信**: gRPC / HTTP2
- **存储**: SQLite (轻量) / PostgreSQL (企业)
- **前端**: React + TypeScript
- **部署**: Docker / Kubernetes / 裸机

---
## 🤝 贡献指南

我们欢迎各种形式的贡献：

- 🐛 提交Bug报告
- 💡 提出功能建议
- 📝 改进文档
- 🔧 提交代码PR
- 📢 帮助推广项目

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - 开源多Agent平台，CrewBot的技术灵感来源
- [OpenAI](https://openai.com/) / [Anthropic](https://anthropic.com/) - 提供强大的AI模型
- 《智算基石》读者 - 你们的反馈让CrewBot更好

---

## 📮 联系我们

- 📧 Email: crewbot@example.com
- 💬 Discord: [CrewBot社区](https://discord.gg/crewbot)
- 🐦 Twitter: [@CrewBotAI](https://twitter.com/crewbotai)

---

<p align="center">
  <strong>让AI协作像呼吸一样自然</strong><br>
  Made with ❤️ by CrewBot Team
</p>
