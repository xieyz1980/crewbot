# CrewBot 架构设计文档

> **轻量级多Agent协作平台 - 技术架构详细设计**
> 
> 版本：v1.0  
> 日期：2026-03-05  
> 状态：设计中

---

## 1. 架构设计原则

### 1.1 轻量级优先
- **资源占用**：个人版可在2核4G机器上运行
- **启动速度**：冷启动<10秒
- **安装复杂度**：一键安装，5分钟上手

### 1.2 模块化设计
- **核心最小化**：只包含必需功能
- **插件化扩展**：功能通过插件实现
- **按需加载**：不用的模块不占用资源

### 1.3 云原生友好
- **容器化**：Docker/Kubernetes原生支持
- **无状态设计**：便于水平扩展
- **配置即代码**：GitOps友好

### 1.4 多端适配
- **云端**：完整功能
- **边缘**：轻量功能
- **端侧**：核心功能

---

## 2. 总体架构

### 2.1 架构全景图

```
┌─────────────────────────────────────────────────────────────┐
│                        User Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Web UI     │  │   CLI Tool   │  │  Mobile App  │      │
│  │  (React)     │  │   (Python)   │  │  (Flutter)   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                     API Gateway                             │
│              (FastAPI / REST + WebSocket)                   │
└────────────────────────────┼────────────────────────────────┘
                             │
    ┌────────────────────────┼────────────────────────┐
    │                        │                        │
┌───▼─────┐         ┌───────▼────────┐      ┌───────▼──────┐
│  Core   │         │   Agent Hub    │      │   One API    │
│ Engine  │         │                │      │   Router     │
│         │         │ • Agent Store  │      │                │
│ • Task  │         │ • Agent Registry│     │ • Model       │
│   Mgmt  │         │ • Skill System │      │   Selector    │
│ • Flow  │         │                │      │ • Cost        │
│   Ctrl  │         │                │      │   Optimizer   │
│ • State │         │                │      │                │
│   Store │         │                │      │                │
└────┬────┘         └───────┬────────┘      └───────┬────────┘
     │                      │                       │
     └──────────────────────┼───────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────────┐
│                      Agent Runtime                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Agent    │  │   Agent    │  │   Agent    │           │
│  │   #1       │  │   #2       │  │   #N       │           │
│  │  (Sandbox) │  │  (Sandbox) │  │  (Sandbox) │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└────────────────────────────────────────────────────────────┘
```

### 2.2 核心组件说明

#### 2.2.1 Core Engine（编排引擎）
**职责**：任务调度、流程控制、状态管理

**关键模块**：
- **Task Manager**：任务分解与分配
- **Flow Controller**：工作流执行引擎
- **State Manager**：状态持久化
- **Event Bus**：事件总线（Agent间通信）

**技术选型**：
- Python 3.11+
- AsyncIO（异步处理）
- Redis（状态缓存）
- SQLite/PostgreSQL（持久化）

#### 2.2.2 Agent Hub（Agent管理中心）
**职责**：Agent注册、发现、管理

**关键模块**：
- **Agent Store**：官方Agent仓库
- **Agent Registry**：第三方Agent注册
- **Skill System**：技能定义与组合
- **Permission Manager**：权限控制

**Agent定义标准**：
```yaml
agent:
  name: "writer"
  version: "1.0.0"
  description: "写作助手Agent"
  author: "crewbot-team"
  
  skills:
    - name: "write_article"
      description: "撰写文章"
      input: 
        topic: string
        length: int
      output:
        article: string
      
  config:
    model: "gpt-4"
    temperature: 0.7
    max_tokens: 4000
    
  resources:
    memory: "512MB"
    timeout: 300
```

#### 2.2.3 One API Router（智能路由层）
**职责**：模型选择、负载均衡、成本控制

**核心算法**：

**1. 任务分类器**
```python
class TaskClassifier:
    def classify(self, task: Task) -> TaskType:
        # 基于任务内容智能分类
        if self.contains_code_keywords(task.content):
            return TaskType.CODING
        elif self.contains_creative_keywords(task.content):
            return TaskType.WRITING
        elif self.contains_analytical_keywords(task.content):
            return TaskType.ANALYSIS
        else:
            return TaskType.GENERAL
```

**2. 模型选择器**
```python
class ModelSelector:
    def select(self, task_type: TaskType, budget: float) -> ModelConfig:
        strategies = {
            TaskType.CODING: [
                ModelConfig("gpt-4", priority=1),
                ModelConfig("claude-3-opus", priority=2),
                ModelConfig("gpt-3.5-turbo", priority=3),
            ],
            TaskType.WRITING: [
                ModelConfig("claude-3-opus", priority=1),
                ModelConfig("gpt-4", priority=2),
            ],
            TaskType.ANALYSIS: [
                ModelConfig("gpt-4", priority=1),
                ModelConfig("claude-3-sonnet", priority=2),
            ]
        }
        
        # 根据预算选择最优模型
        for config in strategies[task_type]:
            if self.estimate_cost(config) <= budget:
                return config
        
        # 预算不足，选择最便宜的
        return ModelConfig("gpt-3.5-turbo")
```

**3. 成本优化器**
```python
class CostOptimizer:
    def optimize(self, requests: List[Request]) -> ExecutionPlan:
        # 批量处理，降低API调用次数
        # 缓存相似请求结果
        # 使用轻量模型做初步筛选
        pass
```

**支持的模型提供商**：
- OpenAI（GPT-4/GPT-3.5）
- Anthropic（Claude-3系列）
- Google（Gemini）
- 本地模型（Ollama/LM Studio）
- Azure OpenAI
- 阿里云（通义千问）

#### 2.2.4 Agent Runtime（Agent运行环境）
**职责**：Agent执行、资源隔离、安全管理

**沙箱设计**：
```python
class AgentSandbox:
    def __init__(self, agent_config: AgentConfig):
        self.container = self.create_container()
        self.resource_limits = agent_config.resources
        self.permissions = agent_config.permissions
    
    def execute(self, task: Task) -> Result:
        # 在隔离环境中执行Agent
        with self.resource_monitor():
            result = self.agent.run(task)
            return result
    
    def cleanup(self):
        # 清理资源
        self.container.stop()
```

**安全机制**：
- 容器隔离（Docker/runc）
- 网络隔离（禁止外网访问）
- 文件系统隔离（只读挂载）
- 资源限制（CPU/内存/时间）

---

## 3. 数据流设计

### 3.1 典型任务执行流程

```
用户请求
    │
    ▼
┌──────────────┐
│  API Gateway │  ← 认证、限流、日志
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Task Parser │  ← 解析用户意图
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Flow Planner │  ← 规划执行流程
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Scheduler   │  ← 调度Agent执行
└──────┬───────┘
       │
       ├──→ Agent A (并行)
       ├──→ Agent B (并行)
       └──→ Agent C (依赖A)
       │
       ▼
┌──────────────┐
│   Merger     │  ← 合并结果
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Response   │  ← 返回给用户
└──────────────┘
```

### 3.2 状态管理

**状态机设计**：
```python
class TaskState(Enum):
    PENDING = "pending"      # 等待执行
    SCHEDULING = "scheduling" # 调度中
    RUNNING = "running"      # 执行中
    WAITING = "waiting"      # 等待依赖
    COMPLETED = "completed"  # 完成
    FAILED = "failed"        # 失败
    RETRYING = "retrying"    # 重试中

class TaskStateMachine:
    transitions = {
        TaskState.PENDING: [TaskState.SCHEDULING],
        TaskState.SCHEDULING: [TaskState.RUNNING, TaskState.FAILED],
        TaskState.RUNNING: [TaskState.COMPLETED, TaskState.FAILED, TaskState.WAITING],
        TaskState.WAITING: [TaskState.RUNNING, TaskState.FAILED],
        TaskState.FAILED: [TaskState.RETRYING],
        TaskState.RETRYING: [TaskState.RUNNING],
    }
```

---

## 4. 部署架构

### 4.1 单机部署（个人版）

```yaml
# docker-compose.yml
version: '3.8'

services:
  crewbot:
    image: crewbot/crewbot:latest
    ports:
      - "8080:8080"
    volumes:
      - ./data:/data
      - ./config:/config
    environment:
      - CREWBOT_MODE=personal
      - CREWBOT_DB_URL=sqlite:///data/crewbot.db
    depends_on:
      - redis
      
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

**资源需求**：
- CPU：2核
- 内存：4GB
- 存储：20GB
- 网络：可选（支持离线运行）

### 4.2 集群部署（企业版）

```yaml
# kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crewbot-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: crewbot-api
  template:
    metadata:
      labels:
        app: crewbot-api
    spec:
      containers:
      - name: api
        image: crewbot/crewbot:latest
        ports:
        - containerPort: 8080
        env:
        - name: CREWBOT_MODE
          value: "enterprise"
        - name: CREWBOT_DB_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

**资源需求**：
- CPU：8核+
- 内存：16GB+
- 存储：100GB+（SSD）
- 数据库：PostgreSQL集群
- 缓存：Redis集群

### 4.3 边缘部署（边缘版）

**树莓派4B部署**：
```bash
# 一键安装脚本
curl -fsSL https://crewbot.ai/install-edge.sh | bash
```

**优化策略**：
- 使用轻量级模型（Phi-2、Llama-2-7B）
- 模型量化（INT8/INT4）
- 减少功能模块（只保留核心Agent）
- 本地优先（优先使用本地模型）

---

## 5. API设计

### 5.1 REST API

**任务提交**
```http
POST /api/v1/tasks
Content-Type: application/json

{
  "name": "write_blog",
  "description": "写一篇关于AI基础设施的博客",
  "agents": ["writer", "researcher"],
  "input": {
    "topic": "AI基础设施",
    "length": 2000
  },
  "config": {
    "max_cost": 0.5,
    "timeout": 300
  }
}

Response:
{
  "task_id": "task_123456",
  "status": "pending",
  "created_at": "2026-03-05T10:00:00Z"
}
```

**查询任务状态**
```http
GET /api/v1/tasks/{task_id}

Response:
{
  "task_id": "task_123456",
  "status": "running",
  "progress": 60,
  "agents": [
    {"name": "researcher", "status": "completed"},
    {"name": "writer", "status": "running"}
  ],
  "created_at": "2026-03-05T10:00:00Z",
  "updated_at": "2026-03-05T10:05:00Z"
}
```

### 5.2 WebSocket API（实时通信）

```javascript
// 连接WebSocket
const ws = new WebSocket('wss://crewbot.ai/ws/tasks/task_123456');

// 接收实时更新
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
  // {
  //   "type": "agent_output",
  //   "agent": "writer",
  //   "content": "正在撰写文章大纲..."
  // }
};
```

---

## 6. 本周开发计划（3/6-3/9）

### Day 1（3/6）：基础架构搭建
- [ ] 项目脚手架搭建（FastAPI + SQLModel）
- [ ] Docker开发环境配置
- [ ] 基础API框架（/health, /version）
- [ ] 数据库模型设计

### Day 2（3/7）：Core Engine实现
- [ ] Task Manager基础功能
- [ ] 状态机实现
- [ ] 事件总线（Redis Pub/Sub）
- [ ] 简单工作流执行

### Day 3（3/8）：Agent框架
- [ ] Agent基类设计
- [ ] Agent注册/发现机制
- [ ] 沙箱环境（Docker）
- [ ] 示例Agent（Echo Agent）

### Day 4（3/9）：One API Router
- [ ] 模型配置管理
- [ ] 简单路由逻辑（轮询）
- [ ] 成本计算模块
- [ ] OpenAI/Claude集成

**本周目标**：完成MVP核心功能，可运行简单任务

---

## 7. 技术栈总结

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端框架** | FastAPI | Python异步Web框架 |
| **数据库** | SQLite/PostgreSQL | 轻量/企业级 |
| **缓存** | Redis | 状态缓存、消息队列 |
| **任务队列** | Celery + Redis | 异步任务处理 |
| **容器化** | Docker | 部署和隔离 |
| **前端** | React + TypeScript | Web UI |
| **移动端** | Flutter | 跨平台APP |
| **CLI** | Click (Python) | 命令行工具 |

---

*文档版本：v1.0*  
*最后更新：2026-03-05*  
*下次更新：3/6 开始实施*
