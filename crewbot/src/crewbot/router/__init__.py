# One API Router

"""
One API Router - 智能模型路由层
统一接口管理多个AI模型，自动选择最优模型
"""

import os
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import random

logger = logging.getLogger(__name__)


class ModelProvider(Enum):
    """模型提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    DEEPSEEK = "deepseek"
    QIANWEN = "qianwen"  # 阿里通义千问
    LOCAL = "local"


@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    provider: ModelProvider
    model_id: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    cost_per_1k_tokens: float = 0.0
    max_tokens: int = 4096
    temperature: float = 0.7
    priority: int = 1  # 优先级，数字越小优先级越高
    enabled: bool = True
    
    def __post_init__(self):
        # 从环境变量读取API密钥
        if not self.api_key:
            env_map = {
                ModelProvider.OPENAI: "OPENAI_API_KEY",
                ModelProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
                ModelProvider.DEEPSEEK: "DEEPSEEK_API_KEY",
                ModelProvider.QIANWEN: "QIANWEN_API_KEY",
            }
            env_var = env_map.get(self.provider)
            if env_var:
                self.api_key = os.getenv(env_var)


class TaskType(Enum):
    """任务类型"""
    CREATIVE_WRITING = "creative_writing"  # 创意写作
    TECHNICAL_WRITING = "technical_writing"  # 技术写作
    CODE_GENERATION = "code_generation"  # 代码生成
    CODE_REVIEW = "code_review"  # 代码审查
    DATA_ANALYSIS = "data_analysis"  # 数据分析
    GENERAL_CHAT = "general_chat"  # 一般对话
    TRANSLATION = "translation"  # 翻译
    SUMMARIZATION = "summarization"  # 摘要


class ModelRouter:
    """
    智能模型路由器
    
    功能：
    1. 统一管理多个模型
    2. 根据任务类型智能选择模型
    3. 成本优化
    4. 故障自动切换
    """
    
    def __init__(self):
        self.models: Dict[str, ModelConfig] = {}
        self.default_model: Optional[str] = None
        
        # 任务类型到模型偏好映射
        self.task_preferences: Dict[TaskType, List[str]] = {
            TaskType.CREATIVE_WRITING: ["claude-3-opus", "gpt-4", "claude-3-sonnet"],
            TaskType.TECHNICAL_WRITING: ["claude-3-opus", "gpt-4", "qianwen-max"],
            TaskType.CODE_GENERATION: ["gpt-4", "claude-3-opus", "deepseek-coder"],
            TaskType.CODE_REVIEW: ["claude-3-sonnet", "gpt-4", "qianwen-max"],
            TaskType.DATA_ANALYSIS: ["gpt-4", "claude-3-sonnet", "qianwen-max"],
            TaskType.GENERAL_CHAT: ["gpt-3.5-turbo", "claude-3-haiku", "qianwen-turbo"],
            TaskType.TRANSLATION: ["qianwen-max", "gpt-4", "claude-3-sonnet"],
            TaskType.SUMMARIZATION: ["gpt-3.5-turbo", "claude-3-haiku", "qianwen-turbo"],
        }
        
        self._init_default_models()
    
    def _init_default_models(self):
        """初始化默认模型配置"""
        default_models = [
            ModelConfig(
                name="gpt-4",
                provider=ModelProvider.OPENAI,
                model_id="gpt-4",
                cost_per_1k_tokens=0.03,
                max_tokens=8192,
                priority=1
            ),
            ModelConfig(
                name="gpt-3.5-turbo",
                provider=ModelProvider.OPENAI,
                model_id="gpt-3.5-turbo",
                cost_per_1k_tokens=0.002,
                max_tokens=4096,
                priority=2
            ),
            ModelConfig(
                name="claude-3-opus",
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3-opus-20240229",
                cost_per_1k_tokens=0.015,
                max_tokens=200000,
                priority=1
            ),
            ModelConfig(
                name="claude-3-sonnet",
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3-sonnet-20240229",
                cost_per_1k_tokens=0.003,
                max_tokens=200000,
                priority=2
            ),
            ModelConfig(
                name="deepseek-chat",
                provider=ModelProvider.DEEPSEEK,
                model_id="deepseek-chat",
                cost_per_1k_tokens=0.00014,
                max_tokens=4096,
                priority=3
            ),
            ModelConfig(
                name="qianwen-max",
                provider=ModelProvider.QIANWEN,
                model_id="qwen-max",
                cost_per_1k_tokens=0.002,
                max_tokens=8192,
                priority=2
            ),
        ]
        
        for model in default_models:
            self.register_model(model)
        
        # 设置默认模型
        if "gpt-3.5-turbo" in self.models:
            self.default_model = "gpt-3.5-turbo"
    
    def register_model(self, config: ModelConfig):
        """注册模型"""
        self.models[config.name] = config
        logger.info(f"注册模型: {config.name} ({config.provider.value})")
    
    def get_model(self, name: str) -> Optional[ModelConfig]:
        """获取模型配置"""
        return self.models.get(name)
    
    def list_models(self, enabled_only: bool = True) -> List[ModelConfig]:
        """列出所有模型"""
        models = list(self.models.values())
        if enabled_only:
            models = [m for m in models if m.enabled and m.api_key]
        return sorted(models, key=lambda x: x.priority)
    
    def classify_task(self, prompt: str) -> TaskType:
        """
        智能分类任务类型
        
        基于关键词和启发式规则
        """
        prompt_lower = prompt.lower()
        
        # 代码相关
        code_keywords = ["code", "程序", "代码", "function", "class", "def ", 
                        "编程", "bug", "debug", "error", "python", "javascript"]
        if any(kw in prompt_lower for kw in code_keywords):
            if any(kw in prompt_lower for kw in ["review", "审查", "检查", "优化"]):
                return TaskType.CODE_REVIEW
            return TaskType.CODE_GENERATION
        
        # 数据分析
        data_keywords = ["分析", "数据", "统计", "图表", "可视化", "dataframe",
                        "analyze", "data", "statistics", "chart"]
        if any(kw in prompt_lower for kw in data_keywords):
            return TaskType.DATA_ANALYSIS
        
        # 翻译
        translate_keywords = ["翻译", "translate", "英文", "中文", "english", "chinese"]
        if any(kw in prompt_lower for kw in translate_keywords):
            return TaskType.TRANSLATION
        
        # 摘要
        summary_keywords = ["总结", "摘要", "summarize", "summary", "概括"]
        if any(kw in prompt_lower for kw in summary_keywords):
            return TaskType.SUMMARIZATION
        
        # 创意写作
        creative_keywords = ["故事", "小说", "story", "poem", "诗", "创意", "creative"]
        if any(kw in prompt_lower for kw in creative_keywords):
            return TaskType.CREATIVE_WRITING
        
        # 技术写作
        tech_keywords = ["文档", "说明", "技术", "documentation", "technical", "guide"]
        if any(kw in prompt_lower for kw in tech_keywords):
            return TaskType.TECHNICAL_WRITING
        
        # 默认一般对话
        return TaskType.GENERAL_CHAT
    
    def select_model(self, 
                     prompt: str,
                     task_type: Optional[TaskType] = None,
                     budget: Optional[float] = None,
                     preferred_models: Optional[List[str]] = None) -> Tuple[str, ModelConfig]:
        """
        智能选择模型
        
        策略：
        1. 如果有指定任务类型，优先使用偏好模型
        2. 如果预算有限，选择成本最低的合适模型
        3. 如果有偏好模型，优先使用
        4. 否则使用默认模型
        
        Returns:
            (model_name, model_config)
        """
        # 获取任务类型
        if not task_type:
            task_type = self.classify_task(prompt)
        
        logger.info(f"任务类型: {task_type.value}")
        
        # 获取可用的模型列表
        available_models = self.list_models(enabled_only=True)
        
        if not available_models:
            raise ValueError("没有可用的模型，请先配置API密钥")
        
        # 如果有偏好模型列表，按优先级选择
        if preferred_models:
            for model_name in preferred_models:
                if model_name in self.models and self.models[model_name].enabled:
                    model = self.models[model_name]
                    if model.api_key:  # 确保有API密钥
                        return model_name, model
        
        # 根据任务类型获取偏好模型
        preferred = self.task_preferences.get(task_type, [])
        
        # 在偏好模型中选择
        candidates = []
        for model_name in preferred:
            if model_name in self.models:
                model = self.models[model_name]
                if model.enabled and model.api_key:
                    candidates.append((model_name, model))
        
        # 如果预算有限，选择成本最低的
        if budget is not None and candidates:
            # 估算token数量（简单估算：1个中文字符≈1.5个token）
            estimated_tokens = len(prompt) * 1.5 + 1000  # 加1000作为输出余量
            
            affordable = []
            for name, model in candidates:
                estimated_cost = (estimated_tokens / 1000) * model.cost_per_1k_tokens
                if estimated_cost <= budget:
                    affordable.append((name, model, estimated_cost))
            
            if affordable:
                # 在预算范围内选择优先级最高的
                affordable.sort(key=lambda x: x[1].priority)
                return affordable[0][0], affordable[0][1]
        
        # 返回优先级最高的候选
        if candidates:
            candidates.sort(key=lambda x: x[1].priority)
            return candidates[0]
        
        # 回退到默认模型
        if self.default_model and self.default_model in self.models:
            model = self.models[self.default_model]
            if model.enabled and model.api_key:
                return self.default_model, model
        
        # 最后回退到第一个可用模型
        first_available = available_models[0]
        return first_available.name, first_available
    
    def estimate_cost(self, prompt: str, model_name: str, 
                     output_tokens: int = 1000) -> float:
        """估算成本"""
        if model_name not in self.models:
            return 0.0
        
        model = self.models[model_name]
        input_tokens = len(prompt) * 1.5  # 粗略估算
        
        total_tokens = input_tokens + output_tokens
        cost = (total_tokens / 1000) * model.cost_per_1k_tokens
        
        return cost
    
    def get_model_info(self) -> List[Dict[str, Any]]:
        """获取所有模型信息"""
        info = []
        for name, config in self.models.items():
            info.append({
                "name": name,
                "provider": config.provider.value,
                "model_id": config.model_id,
                "cost_per_1k_tokens": config.cost_per_1k_tokens,
                "max_tokens": config.max_tokens,
                "enabled": config.enabled,
                "has_api_key": bool(config.api_key),
                "priority": config.priority
            })
        return sorted(info, key=lambda x: x["priority"])


# 全局路由器实例
_router: Optional[ModelRouter] = None

def get_router() -> ModelRouter:
    """获取全局路由器实例"""
    global _router
    if _router is None:
        _router = ModelRouter()
    return _router