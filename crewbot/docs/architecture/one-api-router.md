# One API Router 架构设计文档

## 概述

One API Router 是 CrewBot 的自研模型路由系统，旨在提供比 OpenRouter 更灵活、更可控的多模型接入方案。

## 目标

1. **多模型统一接入**: 支持 GPT-4/Claude/DeepSeek/Gemini 等主流模型
2. **智能路由选择**: 根据任务类型、成本、质量自动选择最优模型
3. **负载均衡**: 在多个 API Key/Endpoint 间分配请求
4. **故障自动转移**: 单点故障时自动切换备用模型
5. **成本优化**: 实时监控和优化 API 成本

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│                     (CrewBot Agents)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    One API Router                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Router    │  │  Load       │  │    Cost Optimizer   │  │
│  │   Engine    │──│  Balancer   │──│    & Monitor        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Task      │  │  Circuit    │  │    Fallback         │  │
│  │   Router    │  │  Breaker    │  │    Manager          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Provider Adapters                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐  │
│  │  OpenAI  │ │ Anthropic│ │ DeepSeek │ │   OpenRouter   │  │
│  │  Adapter │ │  Adapter │ │  Adapter │ │   (Fallback)   │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 核心模块

### 1. Router Engine (路由引擎)

负责接收请求并决定路由策略。

```python
class RouterEngine:
    def route(self, request: Request) -> RouteDecision:
        # 1. 任务分类
        task_type = self.classifier.classify(request.content)
        
        # 2. 获取候选模型
        candidates = self.get_candidates(
            task_type=task_type,
            requirements=request.requirements
        )
        
        # 3. 评分排序
        scored = self.score_models(candidates, request)
        
        # 4. 返回最优选择
        return RouteDecision(
            primary=scored[0],
            fallbacks=scored[1:3]
        )
```

### 2. Task Classifier (任务分类器)

自动识别任务类型以选择合适模型。

```python
class TaskType(Enum):
    CODE = "code"          # 代码生成/分析
    WRITE = "writing"      # 创意写作
    ANALYSIS = "analysis"  # 数据分析
    CHAT = "chat"          # 日常对话
    VISION = "vision"      # 图像理解
    RESEARCH = "research"  # 深度研究
    SUMMARY = "summary"    # 摘要总结
```

### 3. Load Balancer (负载均衡)

在多个 API Key 间分配请求。

```python
class LoadBalancer:
    """支持多种负载均衡策略"""
    
    STRATEGIES = {
        "round_robin": RoundRobinStrategy,
        "weighted": WeightedStrategy,
        "least_conn": LeastConnectionStrategy,
        "adaptive": AdaptiveStrategy,  # 基于延迟和成功率
    }
```

### 4. Circuit Breaker (熔断器)

防止故障扩散。

```python
class CircuitBreaker:
    """熔断器状态"""
    
    class State(Enum):
        CLOSED = "closed"      # 正常
        OPEN = "open"          # 熔断
        HALF_OPEN = "half_open"  # 探测
    
    def call(self, func):
        if self.state == State.OPEN:
            raise CircuitBreakerOpen()
        
        try:
            result = func()
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise
```

### 5. Cost Optimizer (成本优化)

实时监控和优化成本。

```python
class CostOptimizer:
    """成本优化策略"""
    
    def optimize(self, request: Request, budget: Budget) -> ModelChoice:
        # 1. 检查预算限制
        if budget.remaining < budget.threshold:
            return self.select_cheapest(request)
        
        # 2. 根据任务价值选择
        value_score = self.assess_value(request)
        
        if value_score > 0.8:
            return self.select_best_quality(request)
        elif value_score < 0.3:
            return self.select_cheapest(request)
        else:
            return self.select_balanced(request)
```

## 数据模型

### ProviderConfig (提供商配置)

```python
@dataclass
class ProviderConfig:
    name: str                      # openai, anthropic, etc.
    api_keys: List[str]           # 多Key轮询
    base_url: Optional[str]       # 自定义Endpoint
    weight: int = 1               # 权重
    priority: int = 1             # 优先级
    rate_limit: RateLimitConfig   # 速率限制
    timeout: float = 60.0         # 超时时间
    retry_policy: RetryPolicy     # 重试策略
```

### ModelProfile (模型画像)

```python
@dataclass
class ModelProfile:
    id: str                       # 模型ID
    provider: str                 # 所属提供商
    capabilities: List[str]       # 能力列表
    context_length: int           # 上下文长度
    pricing: PricingInfo          # 价格信息
    latency_stats: LatencyStats   # 延迟统计
    quality_score: float          # 质量评分(0-1)
    reliability: float            # 可靠性评分(0-1)
```

### RoutingRule (路由规则)

```python
@dataclass  
class RoutingRule:
    name: str                     # 规则名称
    condition: RuleCondition      # 触发条件
    action: RuleAction            # 执行动作
    priority: int = 0             # 优先级
```

## 路由策略

### 1. 基于任务的智能路由

```python
TASK_ROUTING = {
    TaskType.CODE: {
        "primary": ["claude-3.5-sonnet", "gpt-4o"],
        "fallback": ["deepseek-coder", "gpt-4o-mini"],
    },
    TaskType.WRITE: {
        "primary": ["claude-3.5-sonnet", "claude-3-opus"],
        "fallback": ["gpt-4o", "gpt-4o-mini"],
    },
    TaskType.CHAT: {
        "primary": ["gpt-4o-mini", "claude-3.5-haiku"],
        "fallback": ["gemini-flash", "deepseek-chat"],
    },
    TaskType.VISION: {
        "primary": ["gpt-4o", "claude-3.5-sonnet"],
        "fallback": ["gemini-pro"],
    },
}
```

### 2. 基于成本的动态路由

```python
def route_by_budget(request: Request, budget: Budget):
    """根据预算动态选择"""
    
    cost_tiers = {
        "high": ["claude-3-opus", "gpt-4-turbo"],
        "medium": ["claude-3.5-sonnet", "gpt-4o"],
        "low": ["gpt-4o-mini", "claude-3.5-haiku"],
        "minimal": ["deepseek-chat", "gemini-flash"],
    }
    
    if budget.per_request > 0.01:
        tier = "high"
    elif budget.per_request > 0.005:
        tier = "medium"
    elif budget.per_request > 0.001:
        tier = "low"
    else:
        tier = "minimal"
    
    return select_from_tier(tier, request.task_type)
```

### 3. 基于质量的自适应路由

```python
def route_by_quality(request: Request, min_quality: float):
    """根据质量要求选择"""
    
    quality_scores = {
        "claude-3-opus": 0.95,
        "gpt-4o": 0.93,
        "claude-3.5-sonnet": 0.91,
        "gpt-4o-mini": 0.85,
        "deepseek-chat": 0.82,
    }
    
    candidates = [
        m for m, score in quality_scores.items()
        if score >= min_quality
    ]
    
    return select_cheapest(candidates)
```

## API 设计

### 初始化

```python
from crewbot.router.one_api import OneAPIRouter

router = OneAPIRouter(
    config_path="config/router.yaml",
    # 或程序化配置
    providers=[
        ProviderConfig(name="openai", api_keys=["sk-..."]),
        ProviderConfig(name="anthropic", api_keys=["sk-ant-..."]),
    ]
)
```

### 基本使用

```python
# 简单使用（自动路由）
response = await router.chat(
    messages=[{"role": "user", "content": "Hello!"}],
    strategy="auto"  # auto, quality, cost, speed
)

# 指定模型
response = await router.chat(
    messages=[...],
    model="claude-3.5-sonnet"
)

# 指定任务类型（更智能的路由）
response = await router.chat(
    messages=[...],
    task_type="code",
    budget_limit=0.005  # 单请求预算限制
)
```

### 流式响应

```python
async for chunk in router.stream_chat(messages=[...]):
    print(chunk, end="")
```

### 批量请求

```python
# 批量路由，自动并行和负载均衡
responses = await router.batch_chat([
    {"messages": [...], "task_type": "code"},
    {"messages": [...], "task_type": "chat"},
    {"messages": [...], "task_type": "analysis"},
])
```

## 监控与指标

### 收集的指标

```python
@dataclass
class RouterMetrics:
    # 请求指标
    total_requests: int
    requests_by_model: Dict[str, int]
    requests_by_provider: Dict[str, int]
    
    # 延迟指标
    latency_p50: float
    latency_p95: float
    latency_p99: float
    
    # 成本指标
    total_cost_usd: float
    cost_by_model: Dict[str, float]
    cost_by_provider: Dict[str, float]
    
    # 质量指标
    success_rate: float
    error_rate_by_provider: Dict[str, float]
    fallback_rate: float
```

### 健康检查

```python
health = await router.health_check()
# {
#     "overall": "healthy",
#     "providers": {
#         "openai": {"status": "healthy", "latency": 120},
#         "anthropic": {"status": "healthy", "latency": 150},
#         "deepseek": {"status": "degraded", "latency": 800},
#     }
# }
```

## 配置示例

### YAML 配置

```yaml
# config/router.yaml

providers:
  openai:
    api_keys:
      - "${OPENAI_API_KEY_1}"
      - "${OPENAI_API_KEY_2}"
    weight: 2
    priority: 1
    rate_limit:
      rpm: 500
      tpm: 100000
    
  anthropic:
    api_keys:
      - "${ANTHROPIC_API_KEY}"
    weight: 1
    priority: 1
    rate_limit:
      rpm: 100
      
  deepseek:
    api_keys:
      - "${DEEPSEEK_API_KEY}"
    base_url: "https://api.deepseek.com"
    weight: 1
    priority: 2

routing:
  default_strategy: "balanced"
  
  rules:
    - name: "code_tasks"
      condition:
        task_type: "code"
      action:
        primary: ["claude-3.5-sonnet", "gpt-4o"]
        fallback: ["deepseek-coder"]
        
    - name: "low_budget"
      condition:
        budget_limit: "< 0.001"
      action:
        models: ["gpt-4o-mini", "deepseek-chat"]

  fallback:
    max_retries: 3
    retry_delay: 1.0
    backup_provider: "openrouter"

monitoring:
  enabled: true
  export_interval: 60
  prometheus_port: 9090
```

## 实现计划

### Phase 1: 基础框架 (本周)

- [ ] RouterEngine 核心实现
- [ ] ProviderAdapter 基类
- [ ] OpenAI Adapter
- [ ] Anthropic Adapter
- [ ] 基础路由策略

### Phase 2: 高级功能 (下周)

- [ ] 负载均衡器
- [ ] 熔断器
- [ ] 成本监控
- [ ] 任务分类器
- [ ] DeepSeek/Gemini Adapters

### Phase 3: 优化与完善 (第三周)

- [ ] 自适应路由学习
- [ ] 性能优化
- [ ] 完整测试覆盖
- [ ] 文档完善
- [ ] OpenRouter 作为兜底

## 与现有系统集成

```python
# 在 crewbot/agent/framework.py 中使用

from crewbot.router.one_api import OneAPIRouter

class Agent:
    def __init__(self):
        self.llm_router = OneAPIRouter()
    
    async def process(self, task: Task) -> Response:
        # 自动选择最佳模型
        response = await self.llm_router.chat(
            messages=task.to_messages(),
            task_type=task.type,
            context=task.context
        )
        return Response(content=response.content)
```

## 性能目标

- **路由决策延迟**: < 1ms
- **故障转移时间**: < 3s
- **支持并发**: 1000+ req/s
- **内存占用**: < 100MB
- **配置热更新**: 零停机

## 总结

One API Router 提供了企业级的多模型路由能力：

1. **智能**: 基于任务类型自动选择最佳模型
2. **可靠**: 熔断器 + 自动故障转移
3. **经济**: 实时成本监控和优化
4. **灵活**: 丰富的配置选项和扩展点
5. **可观测**: 完整的监控和指标

这是从 OpenRouter 快速集成到自研可控方案的重要演进。
