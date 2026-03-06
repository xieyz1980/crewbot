"""
One API Router - 智能模型路由
负责任务分类、模型选择、成本优化
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE = "azure"
    LOCAL = "local"


@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    provider: ModelProvider
    context_length: int
    input_price_per_1k: float  # 美元
    output_price_per_1k: float  # 美元
    supports_function_calling: bool = False
    supports_vision: bool = False
    priority: int = 1  # 优先级，越小越优先
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """估算成本"""
        input_cost = (input_tokens / 1000) * self.input_price_per_1k
        output_cost = (output_tokens / 1000) * self.output_price_per_1k
        return input_cost + output_cost


# 预定义的模型配置
DEFAULT_MODELS = {
    # OpenAI Models
    "gpt-4": ModelConfig(
        name="gpt-4",
        provider=ModelProvider.OPENAI,
        context_length=8192,
        input_price_per_1k=0.03,
        output_price_per_1k=0.06,
        supports_function_calling=True,
        priority=1,
    ),
    "gpt-4-turbo": ModelConfig(
        name="gpt-4-turbo",
        provider=ModelProvider.OPENAI,
        context_length=128000,
        input_price_per_1k=0.01,
        output_price_per_1k=0.03,
        supports_function_calling=True,
        priority=1,
    ),
    "gpt-3.5-turbo": ModelConfig(
        name="gpt-3.5-turbo",
        provider=ModelProvider.OPENAI,
        context_length=16385,
        input_price_per_1k=0.0005,
        output_price_per_1k=0.0015,
        supports_function_calling=True,
        priority=3,
    ),
    
    # Anthropic Models
    "claude-3-opus": ModelConfig(
        name="claude-3-opus-20240229",
        provider=ModelProvider.ANTHROPIC,
        context_length=200000,
        input_price_per_1k=0.015,
        output_price_per_1k=0.075,
        supports_vision=True,
        priority=1,
    ),
    "claude-3-sonnet": ModelConfig(
        name="claude-3-sonnet-20240229",
        provider=ModelProvider.ANTHROPIC,
        context_length=200000,
        input_price_per_1k=0.003,
        output_price_per_1k=0.015,
        supports_vision=True,
        priority=2,
    ),
    "claude-3-haiku": ModelConfig(
        name="claude-3-haiku-20240307",
        provider=ModelProvider.ANTHROPIC,
        context_length=200000,
        input_price_per_1k=0.00025,
        output_price_per_1k=0.00125,
        priority=4,
    ),
    
    # Google Models
    "gemini-pro": ModelConfig(
        name="gemini-pro",
        provider=ModelProvider.GOOGLE,
        context_length=32768,
        input_price_per_1k=0.0005,
        output_price_per_1k=0.0015,
        priority=2,
    ),
}


class TaskClassifier:
    """任务分类器"""
    
    # 关键词映射
    KEYWORDS = {
        "coding": [
            "code", "programming", "python", "javascript", "java", "c++",
            "function", "class", "api", "debug", "error", "bug", "compile",
            "代码", "编程", "函数", "调试", "错误", "算法"
        ],
        "writing": [
            "write", "article", "blog", "essay", "content", "story",
            "creative", "draft", "edit", "proofread", "copy",
            "写作", "文章", "博客", "内容", "创意", "编辑"
        ],
        "analysis": [
            "analyze", "analysis", "data", "statistics", "chart", "graph",
            "report", "summary", "insights", "trends",
            "分析", "数据", "统计", "图表", "报告", "洞察"
        ],
        "research": [
            "research", "search", "find", "investigate", "explore",
            "文献", "研究", "调查", "搜索", "查找"
        ],
    }
    
    @classmethod
    def classify(cls, content: str) -> str:
        """根据内容分类任务类型"""
        content_lower = content.lower()
        scores = {}
        
        for task_type, keywords in cls.KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            scores[task_type] = score
        
        # 返回得分最高的类型，如果都为0则返回general
        if max(scores.values()) == 0:
            return "general"
        
        return max(scores, key=scores.get)


class ModelRouter:
    """
    One API Router - 智能模型路由
    
    核心功能：
    1. 任务分类
    2. 模型选择（基于成本、质量、延迟）
    3. 故障转移
    4. 成本优化
    """
    
    def __init__(self):
        self.models: Dict[str, ModelConfig] = DEFAULT_MODELS.copy()
        self.model_availability: Dict[str, bool] = {name: True for name in self.models}
        self.selection_strategy = "balanced"  # balanced, quality, cost
        logger.info("ModelRouter initialized")
    
    def add_model(self, config: ModelConfig) -> None:
        """添加自定义模型"""
        self.models[config.name] = config
        self.model_availability[config.name] = True
        logger.info(f"Model added: {config.name}")
    
    def set_model_availability(self, model_name: str, available: bool) -> None:
        """设置模型可用性"""
        if model_name in self.model_availability:
            self.model_availability[model_name] = available
            logger.info(f"Model {model_name} availability set to {available}")
    
    def get_available_models(self) -> List[str]:
        """获取可用模型列表"""
        return [name for name, available in self.model_availability.items() if available]
    
    def select_model(self, 
                    task_content: str,
                    task_type: Optional[str] = None,
                    budget: Optional[float] = None,
                    require_vision: bool = False,
                    require_functions: bool = False,
                    preferred_provider: Optional[str] = None) -> Optional[ModelConfig]:
        """
        智能选择模型
        
        Args:
            task_content: 任务内容描述
            task_type: 任务类型（可选，自动分类）
            budget: 预算限制（可选）
            require_vision: 是否需要视觉能力
            require_functions: 是否需要函数调用
            preferred_provider: 优先的提供商
        
        Returns:
            选中的模型配置
        """
        # 1. 任务分类
        if not task_type:
            task_type = TaskClassifier.classify(task_content)
        
        logger.info(f"Task classified as: {task_type}")
        
        # 2. 模型选择策略
        candidates = self._get_candidates(
            require_vision=require_vision,
            require_functions=require_functions,
            preferred_provider=preferred_provider
        )
        
        if not candidates:
            logger.warning("No available models match requirements")
            return None
        
        # 3. 根据任务类型排序
        ranked_models = self._rank_models_for_task(candidates, task_type, budget)
        
        # 4. 选择最佳模型
        selected = ranked_models[0] if ranked_models else None
        
        if selected:
            estimated_cost = selected.estimate_cost(1000, 500)  # 估算1000输入,500输出
            logger.info(f"Selected model: {selected.name} (est. cost: ${estimated_cost:.4f})")
        
        return selected
    
    def _get_candidates(self,
                       require_vision: bool = False,
                       require_functions: bool = False,
                       preferred_provider: Optional[str] = None) -> List[ModelConfig]:
        """获取候选模型"""
        candidates = []
        
        for name, config in self.models.items():
            # 检查可用性
            if not self.model_availability.get(name, False):
                continue
            
            # 检查视觉能力
            if require_vision and not config.supports_vision:
                continue
            
            # 检查函数调用能力
            if require_functions and not config.supports_function_calling:
                continue
            
            # 检查提供商偏好
            if preferred_provider and config.provider.value != preferred_provider:
                continue
            
            candidates.append(config)
        
        return candidates
    
    def _rank_models_for_task(self, 
                             candidates: List[ModelConfig],
                             task_type: str,
                             budget: Optional[float] = None) -> List[ModelConfig]:
        """为任务排序模型"""
        
        # 任务类型到模型的映射
        task_model_preferences = {
            "coding": ["gpt-4", "gpt-4-turbo", "claude-3-opus", "claude-3-sonnet"],
            "writing": ["claude-3-opus", "gpt-4", "claude-3-sonnet", "gpt-4-turbo"],
            "analysis": ["gpt-4", "claude-3-opus", "claude-3-sonnet", "gemini-pro"],
            "research": ["claude-3-opus", "gpt-4-turbo", "claude-3-sonnet"],
            "general": ["claude-3-sonnet", "gpt-4-turbo", "gemini-pro", "gpt-3.5-turbo"],
        }
        
        preferences = task_model_preferences.get(task_type, task_model_preferences["general"])
        
        # 按偏好排序
        def sort_key(config: ModelConfig) -> tuple:
            # 优先按任务偏好排序
            try:
                preference_score = preferences.index(config.name)
            except ValueError:
                preference_score = len(preferences)
            
            # 如果设置了预算，考虑成本
            if budget:
                estimated_cost = config.estimate_cost(1000, 500)
                if estimated_cost > budget:
                    return (1000, 0)  # 超出预算，排最后
                cost_score = estimated_cost
            else:
                cost_score = 0
            
            return (preference_score, cost_score)
        
        ranked = sorted(candidates, key=sort_key)
        return ranked
    
    def get_fallback_model(self, primary_model: ModelConfig) -> Optional[ModelConfig]:
        """获取备选模型（故障转移）"""
        # 同提供商的其他模型
        same_provider = [
            m for m in self.models.values()
            if m.provider == primary_model.provider 
            and m.name != primary_model.name
            and self.model_availability.get(m.name, False)
        ]
        
        if same_provider:
            return same_provider[0]
        
        # 其他可用模型
        all_available = [
            m for m in self.models.values()
            if m.name != primary_model.name
            and self.model_availability.get(m.name, False)
        ]
        
        return all_available[0] if all_available else None
    
    def estimate_task_cost(self, 
                          task_content: str,
                          estimated_input_tokens: int = 1000,
                          estimated_output_tokens: int = 500) -> Dict[str, float]:
        """估算任务成本"""
        task_type = TaskClassifier.classify(task_content)
        selected = self.select_model(task_content, task_type)
        
        if not selected:
            return {"error": "No suitable model found"}
        
        cost = selected.estimate_cost(estimated_input_tokens, estimated_output_tokens)
        
        return {
            "model": selected.name,
            "task_type": task_type,
            "estimated_input_tokens": estimated_input_tokens,
            "estimated_output_tokens": estimated_output_tokens,
            "estimated_cost_usd": cost,
            "provider": selected.provider.value,
        }
    
    def get_model_info(self) -> List[Dict]:
        """获取所有模型信息"""
        return [
            {
                "name": config.name,
                "provider": config.provider.value,
                "context_length": config.context_length,
                "input_price": config.input_price_per_1k,
                "output_price": config.output_price_per_1k,
                "supports_vision": config.supports_vision,
                "supports_functions": config.supports_function_calling,
                "available": self.model_availability.get(name, True),
            }
            for name, config in self.models.items()
        ]


# 全局路由器实例
router = ModelRouter()
