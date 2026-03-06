"""
One API Router - CrewBot 自研模型路由系统

核心功能：
- 多模型统一接入（GPT-4/Claude/DeepSeek等）
- 智能路由选择（根据任务类型/成本/质量）
- 负载均衡
- 故障自动转移
- 成本优化

文档: docs/architecture/one-api-router.md
"""

import os
import yaml
import json
import time
import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, AsyncGenerator, Union, Callable
from enum import Enum
from collections import defaultdict
import random

logger = logging.getLogger(__name__)


# ============== 数据模型 ==============

class TaskType(Enum):
    """任务类型枚举"""
    CODE = "code"          # 代码生成/分析
    WRITE = "writing"      # 创意写作  
    ANALYSIS = "analysis"  # 数据分析
    CHAT = "chat"          # 日常对话
    VISION = "vision"      # 图像理解
    RESEARCH = "research"  # 深度研究
    SUMMARY = "summary"    # 摘要总结
    GENERAL = "general"    # 通用任务


class RoutingStrategy(Enum):
    """路由策略"""
    AUTO = "auto"          # 自动选择
    QUALITY = "quality"    # 优先质量
    COST = "cost"          # 优先成本
    SPEED = "speed"        # 优先速度
    BALANCED = "balanced"  # 平衡模式


@dataclass
class Message:
    """标准消息格式"""
    role: str  # system, user, assistant, tool
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None


@dataclass
class ChatRequest:
    """聊天请求"""
    messages: List[Message]
    model: Optional[str] = None
    task_type: Optional[TaskType] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    budget_limit: Optional[float] = None  # USD
    quality_threshold: Optional[float] = None  # 0-1
    timeout: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatResponse:
    """标准响应格式"""
    content: str
    model: str
    provider: str
    usage: Dict[str, int]  # prompt_tokens, completion_tokens, total_tokens
    cost_usd: float
    latency_ms: float
    finish_reason: str
    raw_response: Optional[Dict] = None


@dataclass
class ModelProfile:
    """模型画像"""
    id: str
    provider: str
    display_name: str
    context_length: int
    capabilities: List[str]  # code, vision, function_calling, etc.
    pricing_prompt: float    # per 1K tokens
    pricing_completion: float  # per 1K tokens
    quality_score: float = 0.8    # 质量评分 0-1
    speed_score: float = 0.8      # 速度评分 0-1
    reliability: float = 0.99     # 可靠性 0-1


@dataclass
class ProviderConfig:
    """提供商配置"""
    name: str
    api_keys: List[str]
    base_url: Optional[str] = None
    weight: int = 1
    priority: int = 1
    timeout: float = 60.0
    max_retries: int = 3
    rpm_limit: int = 60
    tpm_limit: int = 10000
    enabled: bool = True


@dataclass
class RoutingRule:
    """路由规则"""
    name: str
    condition: Dict[str, Any]  # 触发条件
    action: Dict[str, Any]     # 执行动作
    priority: int = 0


@dataclass
class RouterMetrics:
    """路由指标"""
    total_requests: int = 0
    success_count: int = 0
    failure_count: int = 0
    fallback_count: int = 0
    total_cost_usd: float = 0.0
    latency_sum_ms: float = 0.0
    requests_by_model: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    requests_by_provider: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    cost_by_model: Dict[str, float] = field(default_factory=lambda: defaultdict(float))
    errors_by_provider: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    @property
    def avg_latency_ms(self) -> float:
        if self.total_requests == 0:
            return 0
        return self.latency_sum_ms / self.total_requests
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 1.0
        return self.success_count / self.total_requests


# ============== Provider Adapter 基类 ==============

class ProviderAdapter(ABC):
    """提供商适配器基类"""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.name = config.name
        self._key_index = 0  # 轮询计数器
    
    @property
    def current_api_key(self) -> str:
        """获取当前API Key（轮询）"""
        key = self.config.api_keys[self._key_index % len(self.config.api_keys)]
        self._key_index += 1
        return key
    
    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """发送聊天请求"""
        pass
    
    @abstractmethod
    async def stream_chat(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        """流式聊天"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        pass
    
    def estimate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """估算成本"""
        profile = MODEL_PROFILES.get(model)
        if not profile:
            return 0.0
        return (input_tokens / 1000) * profile.pricing_prompt + \
               (output_tokens / 1000) * profile.pricing_completion


# ============== 预定义模型配置 ==============

MODEL_PROFILES: Dict[str, ModelProfile] = {
    # OpenAI
    "gpt-4o": ModelProfile(
        id="gpt-4o",
        provider="openai",
        display_name="GPT-4o",
        context_length=128000,
        capabilities=["vision", "function_calling", "json_mode"],
        pricing_prompt=0.0025,
        pricing_completion=0.01,
        quality_score=0.93,
        speed_score=0.85,
    ),
    "gpt-4o-mini": ModelProfile(
        id="gpt-4o-mini",
        provider="openai",
        display_name="GPT-4o Mini",
        context_length=128000,
        capabilities=["vision", "function_calling", "json_mode"],
        pricing_prompt=0.00015,
        pricing_completion=0.0006,
        quality_score=0.85,
        speed_score=0.95,
    ),
    "gpt-4-turbo": ModelProfile(
        id="gpt-4-turbo",
        provider="openai",
        display_name="GPT-4 Turbo",
        context_length=128000,
        capabilities=["vision", "function_calling", "json_mode"],
        pricing_prompt=0.01,
        pricing_completion=0.03,
        quality_score=0.94,
        speed_score=0.80,
    ),
    
    # Anthropic
    "claude-3-5-sonnet": ModelProfile(
        id="claude-3-5-sonnet",
        provider="anthropic",
        display_name="Claude 3.5 Sonnet",
        context_length=200000,
        capabilities=["vision", "function_calling"],
        pricing_prompt=0.003,
        pricing_completion=0.015,
        quality_score=0.91,
        speed_score=0.85,
    ),
    "claude-3-5-haiku": ModelProfile(
        id="claude-3-5-haiku",
        provider="anthropic",
        display_name="Claude 3.5 Haiku",
        context_length=200000,
        capabilities=["vision"],
        pricing_prompt=0.00025,
        pricing_completion=0.00125,
        quality_score=0.83,
        speed_score=0.95,
    ),
    "claude-3-opus": ModelProfile(
        id="claude-3-opus",
        provider="anthropic",
        display_name="Claude 3 Opus",
        context_length=200000,
        capabilities=["vision", "function_calling"],
        pricing_prompt=0.015,
        pricing_completion=0.075,
        quality_score=0.95,
        speed_score=0.75,
    ),
    
    # DeepSeek
    "deepseek-chat": ModelProfile(
        id="deepseek-chat",
        provider="deepseek",
        display_name="DeepSeek Chat",
        context_length=64000,
        capabilities=["function_calling"],
        pricing_prompt=0.00014,
        pricing_completion=0.00028,
        quality_score=0.82,
        speed_score=0.88,
    ),
    "deepseek-coder": ModelProfile(
        id="deepseek-coder",
        provider="deepseek",
        display_name="DeepSeek Coder",
        context_length=64000,
        capabilities=["code", "function_calling"],
        pricing_prompt=0.00014,
        pricing_completion=0.00028,
        quality_score=0.88,
        speed_score=0.88,
    ),
    
    # Google
    "gemini-1.5-pro": ModelProfile(
        id="gemini-1.5-pro",
        provider="google",
        display_name="Gemini 1.5 Pro",
        context_length=2000000,
        capabilities=["vision", "function_calling", "json_mode"],
        pricing_prompt=0.00125,
        pricing_completion=0.005,
        quality_score=0.90,
        speed_score=0.82,
    ),
    "gemini-1.5-flash": ModelProfile(
        id="gemini-1.5-flash",
        provider="google",
        display_name="Gemini 1.5 Flash",
        context_length=1000000,
        capabilities=["vision", "function_calling", "json_mode"],
        pricing_prompt=0.000075,
        pricing_completion=0.0003,
        quality_score=0.84,
        speed_score=0.92,
    ),
}

# 任务类型到推荐模型的映射
TASK_MODEL_MAPPING = {
    TaskType.CODE: ["claude-3-5-sonnet", "gpt-4o", "deepseek-coder", "gpt-4o-mini"],
    TaskType.WRITE: ["claude-3-5-sonnet", "claude-3-opus", "gpt-4o", "gpt-4o-mini"],
    TaskType.ANALYSIS: ["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro", "deepseek-chat"],
    TaskType.CHAT: ["gpt-4o-mini", "claude-3-5-haiku", "gemini-1.5-flash", "deepseek-chat"],
    TaskType.VISION: ["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro"],
    TaskType.RESEARCH: ["claude-3-opus", "gpt-4-turbo", "claude-3-5-sonnet"],
    TaskType.SUMMARY: ["gpt-4o-mini", "claude-3-5-haiku", "gemini-1.5-flash"],
    TaskType.GENERAL: ["gpt-4o-mini", "claude-3-5-sonnet", "deepseek-chat"],
}


# ============== 任务分类器 ==============

class TaskClassifier:
    """简单的任务分类器"""
    
    KEYWORDS = {
        TaskType.CODE: [
            "code", "programming", "python", "javascript", "java", "function",
            "class", "api", "debug", "error", "bug", "algorithm", "编程",
            "代码", "函数", "调试", "算法", "class", "def ", "import ",
        ],
        TaskType.WRITE: [
            "write", "article", "blog", "essay", "content", "story",
            "creative", "draft", "edit", "proofread", "写作", "文章",
            "博客", "创意", "故事", "文案", "邮件", "email",
        ],
        TaskType.ANALYSIS: [
            "analyze", "analysis", "data", "statistics", "chart", "graph",
            "report", "summary", "insights", "trends", "分析", "数据",
            "统计", "图表", "报告", "趋势", "metric", "dashboard",
        ],
        TaskType.VISION: [
            "image", "picture", "photo", "diagram", "chart", "analyze image",
            "看图", "图片", "图像", "照片", "图表", "describe what you see",
        ],
        TaskType.RESEARCH: [
            "research", "investigate", "explore", "study", "survey",
            "文献", "研究", "调查", "探索", "论文", "paper", "academic",
        ],
        TaskType.SUMMARY: [
            "summarize", "summary", "tl;dr", "key points", "abstract",
            "总结", "摘要", "要点", "概括", "精简", "brief",
        ],
    }
    
    @classmethod
    def classify(cls, content: str) -> TaskType:
        """根据内容分类任务类型"""
        content_lower = content.lower()
        scores = defaultdict(int)
        
        for task_type, keywords in cls.KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    scores[task_type] += 1
        
        if not scores:
            return TaskType.GENERAL
        
        return max(scores, key=scores.get)


# ============== 熔断器 ==============

class CircuitState(Enum):
    CLOSED = "closed"       # 正常
    OPEN = "open"          # 熔断
    HALF_OPEN = "half_open"  # 半开探测


class CircuitBreaker:
    """熔断器 - 防止故障扩散"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0
        self.half_open_calls = 0
    
    def can_execute(self) -> bool:
        """检查是否可以执行"""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                logger.info("Circuit breaker entering half-open state")
                return True
            return False
        
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls < self.half_open_max_calls:
                self.half_open_calls += 1
                return True
            return False
        
        return True
    
    def record_success(self):
        """记录成功"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_max_calls:
                self._reset()
                logger.info("Circuit breaker closed (recovered)")
        else:
            self.failure_count = max(0, self.failure_count - 1)
    
    def record_failure(self):
        """记录失败"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            logger.warning("Circuit breaker opened (half-open failure)")
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker opened ({self.failure_count} failures)")
    
    def _reset(self):
        """重置状态"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.half_open_calls = 0


# ============== One API Router 主类 ==============

class OneAPIRouter:
    """
    One API Router - 智能模型路由系统
    
    Usage:
        router = OneAPIRouter()
        
        # 简单使用（自动路由）
        response = await router.chat(messages=[...])
        
        # 指定策略
        response = await router.chat(
            messages=[...],
            strategy=RoutingStrategy.QUALITY
        )
        
        # 指定任务类型
        response = await router.chat(
            messages=[...],
            task_type=TaskType.CODE
        )
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        providers: Optional[List[ProviderConfig]] = None,
        default_strategy: RoutingStrategy = RoutingStrategy.BALANCED,
        enable_fallback: bool = True,
        metrics_enabled: bool = True
    ):
        self.default_strategy = default_strategy
        self.enable_fallback = enable_fallback
        self.metrics_enabled = metrics_enabled
        
        # 组件初始化
        self.adapters: Dict[str, ProviderAdapter] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.metrics = RouterMetrics()
        
        # 加载配置
        if config_path:
            self._load_config(config_path)
        elif providers:
            for config in providers:
                self._register_provider(config)
        else:
            # 从环境变量自动配置
            self._auto_configure()
        
        logger.info(f"OneAPIRouter initialized with {len(self.adapters)} providers")
    
    def _load_config(self, path: str):
        """从YAML加载配置"""
        with open(path) as f:
            config = yaml.safe_load(f)
        
        for provider_data in config.get("providers", []):
            provider_config = ProviderConfig(**provider_data)
            self._register_provider(provider_config)
    
    def _register_provider(self, config: ProviderConfig):
        """注册提供商适配器"""
        # 这里简化处理，实际应该根据provider name加载对应的Adapter类
        # 先创建占位，后续实现具体Adapter
        self.adapters[config.name] = None  # Placeholder
        self.circuit_breakers[config.name] = CircuitBreaker()
        logger.info(f"Registered provider: {config.name}")
    
    def _auto_configure(self):
        """从环境变量自动配置"""
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            self._register_provider(ProviderConfig(
                name="openai",
                api_keys=[os.getenv("OPENAI_API_KEY")],
                base_url=os.getenv("OPENAI_BASE_URL")
            ))
        
        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            self._register_provider(ProviderConfig(
                name="anthropic",
                api_keys=[os.getenv("ANTHROPIC_API_KEY")]
            ))
        
        # DeepSeek
        if os.getenv("DEEPSEEK_API_KEY"):
            self._register_provider(ProviderConfig(
                name="deepseek",
                api_keys=[os.getenv("DEEPSEEK_API_KEY")],
                base_url="https://api.deepseek.com"
            ))
    
    async def chat(
        self,
        messages: List[Union[Message, Dict]],
        strategy: RoutingStrategy = RoutingStrategy.AUTO,
        task_type: Optional[TaskType] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> ChatResponse:
        """
        发送聊天请求（智能路由）
        
        Args:
            messages: 消息列表
            strategy: 路由策略
            task_type: 任务类型（可选，自动检测）
            model: 指定模型（可选）
            **kwargs: 额外参数
        
        Returns:
            ChatResponse
        """
        # 标准化消息格式
        normalized_messages = [
            Message(**m) if isinstance(m, dict) else m
            for m in messages
        ]
        
        # 创建请求对象
        request = ChatRequest(
            messages=normalized_messages,
            model=model,
            task_type=task_type,
            **kwargs
        )
        
        # 自动检测任务类型
        if not request.task_type:
            content = " ".join([m.content for m in normalized_messages if m.role == "user"])
            request.task_type = TaskClassifier.classify(content)
            logger.debug(f"Auto-classified task as: {request.task_type.value}")
        
        # 路由选择
        if model:
            # 指定模型
            selected_model = model
        else:
            # 智能路由
            selected_model = self._select_model(request, strategy)
        
        request.model = selected_model
        
        # 执行请求
        start_time = time.time()
        
        try:
            response = await self._execute_with_fallback(request)
            
            # 更新指标
            if self.metrics_enabled:
                self._update_metrics(request, response, time.time() - start_time)
            
            return response
            
        except Exception as e:
            logger.error(f"Chat failed after all retries: {e}")
            raise
    
    async def stream_chat(
        self,
        messages: List[Union[Message, Dict]],
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """流式聊天"""
        # 简化实现：先使用非流式，后续扩展
        response = await self.chat(messages, **kwargs)
        
        # 模拟流式输出
        words = response.content.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.01)
    
    def _select_model(
        self,
        request: ChatRequest,
        strategy: RoutingStrategy
    ) -> str:
        """选择模型"""
        task_models = TASK_MODEL_MAPPING.get(request.task_type, TASK_MODEL_MAPPING[TaskType.GENERAL])
        
        # 根据策略选择
        if strategy == RoutingStrategy.QUALITY or request.quality_threshold:
            # 优先质量
            candidates = [m for m in task_models if MODEL_PROFILES[m].quality_score >= 0.9]
            return candidates[0] if candidates else task_models[0]
        
        elif strategy == RoutingStrategy.COST or request.budget_limit:
            # 优先成本
            sorted_models = sorted(
                task_models,
                key=lambda m: MODEL_PROFILES[m].pricing_prompt + MODEL_PROFILES[m].pricing_completion
            )
            # 在预算内选质量最高的
            for model in sorted_models:
                profile = MODEL_PROFILES[model]
                avg_cost = (profile.pricing_prompt + profile.pricing_completion) / 2
                if avg_cost <= (request.budget_limit or 0.01):
                    return model
            return sorted_models[0]
        
        elif strategy == RoutingStrategy.SPEED:
            # 优先速度
            sorted_models = sorted(
                task_models,
                key=lambda m: MODEL_PROFILES[m].speed_score,
                reverse=True
            )
            return sorted_models[0]
        
        else:  # AUTO or BALANCED
            # 平衡模式：质量+成本的综合考虑
            def balance_score(model: str) -> float:
                profile = MODEL_PROFILES[model]
                quality = profile.quality_score
                cost_efficiency = 1.0 / (profile.pricing_prompt + profile.pricing_completion + 0.001)
                return quality * 0.6 + cost_efficiency * 0.4
            
            sorted_models = sorted(task_models, key=balance_score, reverse=True)
            return sorted_models[0]
    
    async def _execute_with_fallback(self, request: ChatRequest) -> ChatResponse:
        """执行请求，带故障转移"""
        model = request.model
        profile = MODEL_PROFILES.get(model)
        
        if not profile:
            raise ValueError(f"Unknown model: {model}")
        
        provider = profile.provider
        adapter = self.adapters.get(provider)
        
        if not adapter:
            # 降级到OpenRouter或其他可用提供商
            logger.warning(f"Provider {provider} not available, trying fallback")
            return await self._fallback_execute(request)
        
        # 检查熔断器
        circuit = self.circuit_breakers.get(provider)
        if circuit and not circuit.can_execute():
            logger.warning(f"Circuit breaker open for {provider}, using fallback")
            return await self._fallback_execute(request)
        
        # 执行请求
        try:
            # 这里简化处理，实际应该调用adapter.chat
            # 当前是骨架代码
            raise NotImplementedError("Provider adapters not yet implemented")
            
        except Exception as e:
            logger.error(f"Request failed for {provider}: {e}")
            if circuit:
                circuit.record_failure()
            
            if self.enable_fallback:
                return await self._fallback_execute(request)
            raise
    
    async def _fallback_execute(self, request: ChatRequest) -> ChatResponse:
        """降级执行"""
        # 这里可以使用OpenRouter作为兜底
        # 或者选择其他可用模型
        logger.info("Executing fallback strategy")
        self.metrics.fallback_count += 1
        
        # TODO: 实现OpenRouter兜底逻辑
        raise NotImplementedError("Fallback to OpenRouter not yet implemented")
    
    def _update_metrics(
        self,
        request: ChatRequest,
        response: ChatResponse,
        latency: float
    ):
        """更新指标"""
        self.metrics.total_requests += 1
        self.metrics.success_count += 1
        self.metrics.latency_sum_ms += latency * 1000
        self.metrics.total_cost_usd += response.cost_usd
        self.metrics.requests_by_model[response.model] += 1
        self.metrics.requests_by_provider[response.provider] += 1
        self.metrics.cost_by_model[response.model] += response.cost_usd
    
    async def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        results = {
            "overall": "healthy",
            "providers": {},
            "metrics": {
                "total_requests": self.metrics.total_requests,
                "success_rate": self.metrics.success_rate,
                "avg_latency_ms": self.metrics.avg_latency_ms,
            }
        }
        
        for name, adapter in self.adapters.items():
            circuit = self.circuit_breakers.get(name)
            results["providers"][name] = {
                "circuit_state": circuit.state.value if circuit else "unknown",
                "available": circuit.can_execute() if circuit else False,
            }
        
        return results
    
    def get_metrics(self) -> RouterMetrics:
        """获取指标"""
        return self.metrics
    
    def estimate_cost(
        self,
        model: str,
        input_tokens: int = 1000,
        output_tokens: int = 500
    ) -> float:
        """估算请求成本"""
        profile = MODEL_PROFILES.get(model)
        if not profile:
            return 0.0
        
        return (input_tokens / 1000) * profile.pricing_prompt + \
               (output_tokens / 1000) * profile.pricing_completion
    
    def get_available_models(
        self,
        task_type: Optional[TaskType] = None,
        capability: Optional[str] = None
    ) -> List[ModelProfile]:
        """获取可用模型列表"""
        models = list(MODEL_PROFILES.values())
        
        if task_type:
            model_ids = TASK_MODEL_MAPPING.get(task_type, [])
            models = [m for m in models if m.id in model_ids]
        
        if capability:
            models = [m for m in models if capability in m.capabilities]
        
        return models


# ============== 便捷函数 ==============

def create_router(
    config_path: Optional[str] = None,
    strategy: str = "balanced"
) -> OneAPIRouter:
    """
    快速创建路由器
    
    Args:
        config_path: 配置文件路径
        strategy: 默认策略 (auto, quality, cost, speed, balanced)
    
    Returns:
        OneAPIRouter 实例
    """
    strategy_enum = RoutingStrategy(strategy)
    return OneAPIRouter(
        config_path=config_path,
        default_strategy=strategy_enum
    )


# ============== 测试 ==============

if __name__ == "__main__":
    async def demo():
        print("🚀 One API Router Demo\n")
        
        # 创建路由器
        router = OneAPIRouter()
        
        # 健康检查
        print("📡 Health Check:")
        health = await router.health_check()
        print(f"   Overall: {health['overall']}")
        for provider, status in health['providers'].items():
            print(f"   - {provider}: {status['circuit_state']}")
        print()
        
        # 模型选择测试
        print("🎯 Model Selection:")
        test_cases = [
            ("Write a Python function to calculate fibonacci", TaskType.CODE),
            ("Write a blog post about AI", TaskType.WRITE),
            ("What's the weather?", TaskType.CHAT),
        ]
        
        for content, expected_type in test_cases:
            classified = TaskClassifier.classify(content)
            selected = router._select_model(
                ChatRequest(messages=[], task_type=classified),
                RoutingStrategy.BALANCED
            )
            print(f"   Content: {content[:40]}...")
            print(f"   Classified: {classified.value}, Selected: {selected}\n")
        
        # 成本估算
        print("💰 Cost Estimation (1000 in / 500 out):")
        for model_id in ["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet", "deepseek-chat"]:
            cost = router.estimate_cost(model_id, 1000, 500)
            print(f"   {model_id}: ${cost:.5f}")
        
        print("\n✅ Demo completed!")
    
    asyncio.run(demo())
