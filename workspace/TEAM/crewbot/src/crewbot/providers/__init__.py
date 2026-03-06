"""
LLM Providers for CrewBot
"""

from .openai_client import (
    OpenAIClient,
    OpenAIConfig,
    OpenAIModel,
    Message,
    ChatResponse,
    OpenAIError,
    OpenAIAPIError,
    OpenAIRateLimitError,
    OpenAIAuthenticationError,
    create_openai_client
)

from .anthropic_client import (
    AnthropicClient,
    AnthropicConfig,
    ClaudeModel,
    ClaudeMessage,
    ClaudeResponse,
    AnthropicError,
    AnthropicAPIError,
    AnthropicRateLimitError,
    AnthropicAuthenticationError,
    create_anthropic_client
)

__all__ = [
    # OpenAI
    "OpenAIClient",
    "OpenAIConfig", 
    "OpenAIModel",
    "Message",
    "ChatResponse",
    "OpenAIError",
    "OpenAIAPIError",
    "OpenAIRateLimitError",
    "OpenAIAuthenticationError",
    "create_openai_client",
    
    # Anthropic
    "AnthropicClient",
    "AnthropicConfig",
    "ClaudeModel",
    "ClaudeMessage",
    "ClaudeResponse",
    "AnthropicError",
    "AnthropicAPIError",
    "AnthropicRateLimitError",
    "AnthropicAuthenticationError",
    "create_anthropic_client",
]
