"""
CrewBot Providers - 模型接入层

提供多种模型接入方式：
- OpenRouter: 统一多模型接入（推荐）
- OpenAI: 原生OpenAI API
- Anthropic: 原生Anthropic API
"""

from .openrouter_client import (
    OpenRouterClient,
    OpenRouterConfig,
    OpenRouterModel,
    Message,
    ChatResponse,
    ModelInfo,
    ModelSelector,
    create_openrouter_client,
    OpenRouterError,
    OpenRouterAPIError,
    OpenRouterRateLimitError,
)

__all__ = [
    # OpenRouter (主推)
    "OpenRouterClient",
    "OpenRouterConfig", 
    "OpenRouterModel",
    "Message",
    "ChatResponse",
    "ModelInfo",
    "ModelSelector",
    "create_openrouter_client",
    "OpenRouterError",
    "OpenRouterAPIError",
    "OpenRouterRateLimitError",
]

# Provider version
__version__ = "0.1.0"
