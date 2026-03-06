"""
Anthropic Claude API Client for CrewBot
Provides integration with Anthropic Claude models
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, AsyncGenerator, Union
from dataclasses import dataclass
from enum import Enum
import asyncio

# Configure logging
logger = logging.getLogger(__name__)


class ClaudeModel(str, Enum):
    """Supported Anthropic Claude models"""
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"
    CLAUDE_3_5_HAIKU = "claude-3-5-haiku-20241022"


@dataclass
class AnthropicConfig:
    """Configuration for Anthropic client"""
    api_key: str
    base_url: Optional[str] = None
    default_model: ClaudeModel = ClaudeModel.CLAUDE_3_5_SONNET
    timeout: float = 60.0
    max_retries: int = 3
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: Optional[float] = None
    top_k: Optional[int] = None


@dataclass
class ClaudeMessage:
    """Claude message structure"""
    role: str  # user, assistant
    content: Union[str, List[Dict]]  # Can be string or content blocks


@dataclass
class ClaudeResponse:
    """Standardized Claude response"""
    content: str
    model: str
    usage: Dict[str, int]
    stop_reason: str
    raw_response: Optional[Dict] = None


class AnthropicError(Exception):
    """Base exception for Anthropic client errors"""
    pass


class AnthropicAPIError(AnthropicError):
    """API-specific errors"""
    def __init__(self, message: str, status_code: int = None, error_type: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_type = error_type


class AnthropicRateLimitError(AnthropicAPIError):
    """Rate limit exceeded"""
    pass


class AnthropicAuthenticationError(AnthropicAPIError):
    """Authentication failed"""
    pass


class AnthropicClient:
    """
    Anthropic Claude API Client with full error handling and retry support
    """
    
    def __init__(self, config: Optional[AnthropicConfig] = None):
        """
        Initialize Anthropic client
        
        Args:
            config: Anthropic configuration. If None, uses environment variables
        """
        self.config = config or self._create_config_from_env()
        self._client = None
        self._initialize_client()
        logger.info(f"Anthropic client initialized with model: {self.config.default_model}")
    
    def _create_config_from_env(self) -> AnthropicConfig:
        """Create config from environment variables"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise AnthropicError("ANTHROPIC_API_KEY environment variable not set")
        
        model_str = os.getenv("ANTHROPIC_DEFAULT_MODEL", "claude-3-5-sonnet-20241022")
        
        return AnthropicConfig(
            api_key=api_key,
            base_url=os.getenv("ANTHROPIC_BASE_URL"),
            default_model=ClaudeModel(model_str),
            timeout=float(os.getenv("ANTHROPIC_TIMEOUT", "60.0")),
            max_retries=int(os.getenv("ANTHROPIC_MAX_RETRIES", "3")),
            temperature=float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("ANTHROPIC_MAX_TOKENS", "4096")),
            top_p=float(os.getenv("ANTHROPIC_TOP_P")) if os.getenv("ANTHROPIC_TOP_P") else None,
            top_k=int(os.getenv("ANTHROPIC_TOP_K")) if os.getenv("ANTHROPIC_TOP_K") else None
        )
    
    def _initialize_client(self):
        """Initialize the Anthropic client"""
        try:
            from anthropic import AsyncAnthropic
            
            client_kwargs = {
                "api_key": self.config.api_key,
                "timeout": self.config.timeout,
                "max_retries": self.config.max_retries
            }
            
            if self.config.base_url:
                client_kwargs["base_url"] = self.config.base_url
            
            self._client = AsyncAnthropic(**client_kwargs)
            logger.debug("Anthropic async client initialized successfully")
            
        except ImportError:
            logger.error("anthropic package not installed. Run: pip install anthropic")
            raise AnthropicError("anthropic package not installed")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            raise AnthropicError(f"Client initialization failed: {e}")
    
    async def chat(
        self,
        messages: List[ClaudeMessage],
        model: Optional[ClaudeModel] = None,
        system: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Union[ClaudeResponse, AsyncGenerator[str, None]]:
        """
        Send chat completion request to Claude
        
        Args:
            messages: List of messages
            model: Model to use (defaults to config.default_model)
            system: System prompt (Claude-specific)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            tools: Optional tools for function calling
            **kwargs: Additional parameters
            
        Returns:
            ClaudeResponse or AsyncGenerator for streaming
        """
        model = model or self.config.default_model
        temperature = temperature if temperature is not None else self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens
        
        # Convert messages to Anthropic format
        message_dicts = []
        for msg in messages:
            if isinstance(msg.content, str):
                message_dicts.append({
                    "role": msg.role,
                    "content": msg.content
                })
            else:
                message_dicts.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        request_params = {
            "model": model.value,
            "messages": message_dicts,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        if system:
            request_params["system"] = system
        
        if self.config.top_p is not None:
            request_params["top_p"] = self.config.top_p
        
        if self.config.top_k is not None:
            request_params["top_k"] = self.config.top_k
        
        if tools:
            request_params["tools"] = tools
        
        logger.debug(f"Sending Claude request: model={model}, messages={len(messages)}")
        
        try:
            if stream:
                return self._stream_chat(request_params)
            else:
                return await self._complete_chat(request_params)
                
        except Exception as e:
            self._handle_error(e)
    
    async def _complete_chat(self, params: Dict) -> ClaudeResponse:
        """Non-streaming chat completion"""
        try:
            response = await self._client.messages.create(**params)
            
            # Extract text content from response
            content_text = ""
            for block in response.content:
                if block.type == "text":
                    content_text += block.text
            
            return ClaudeResponse(
                content=content_text,
                model=response.model,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                },
                stop_reason=response.stop_reason or "end_turn",
                raw_response={
                    "id": response.id,
                    "type": response.type,
                    "role": response.role,
                    "content": [{"type": c.type, "text": c.text if hasattr(c, 'text') else ''} 
                               for c in response.content],
                    "model": response.model,
                    "stop_reason": response.stop_reason,
                    "stop_sequence": response.stop_sequence,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens
                    }
                }
            )
            
        except Exception as e:
            logger.error(f"Claude chat completion failed: {e}")
            raise
    
    async def _stream_chat(self, params: Dict) -> AsyncGenerator[str, None]:
        """Streaming chat completion"""
        params["stream"] = True
        
        try:
            async with self._client.messages.stream(**params) as stream:
                async for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            logger.error(f"Claude streaming chat failed: {e}")
            raise
    
    async def simple_chat(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Simple one-turn chat with Claude
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt (Claude-specific)
            
        Returns:
            Assistant's response text
        """
        messages = [ClaudeMessage(role="user", content=prompt)]
        
        response = await self.chat(
            messages=messages,
            system=system_prompt
        )
        return response.content
    
    async def chat_with_history(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Chat with conversation history
        
        Args:
            messages: List of {role, content} dictionaries
            system_prompt: Optional system prompt
            
        Returns:
            Assistant's response text
        """
        claude_messages = [
            ClaudeMessage(role=msg["role"], content=msg["content"])
            for msg in messages
        ]
        
        response = await self.chat(
            messages=claude_messages,
            system=system_prompt
        )
        return response.content
    
    async def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using Anthropic's tokenizer
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Token count
        """
        try:
            # Use the client's beta token counting if available
            # Fallback to approximate count
            import tiktoken
            encoder = tiktoken.get_encoding("cl100k_base")  # Claude uses similar tokenizer
            return len(encoder.encode(text))
        except ImportError:
            # Rough approximation: ~4 characters per token
            return len(text) // 4
        except Exception as e:
            logger.warning(f"Token counting failed: {e}")
            return len(text) // 4
    
    def _handle_error(self, error: Exception):
        """Handle and classify API errors"""
        error_str = str(error).lower()
        
        # Rate limit errors
        if "rate limit" in error_str or "429" in error_str:
            logger.warning("Anthropic rate limit exceeded")
            raise AnthropicRateLimitError(
                "Rate limit exceeded. Please try again later.",
                status_code=429,
                error_type="rate_limit"
            )
        
        # Authentication errors
        if "authentication" in error_str or "401" in error_str or "api key" in error_str:
            logger.error("Anthropic authentication failed")
            raise AnthropicAuthenticationError(
                "Authentication failed. Please check your API key.",
                status_code=401,
                error_type="authentication"
            )
        
        # Context length errors
        if "context" in error_str or "token" in error_str or "too long" in error_str:
            logger.error("Context length exceeded")
            raise AnthropicAPIError(
                "Input too long. Please reduce the message length.",
                status_code=400,
                error_type="context_length"
            )
        
        # Overloaded
        if "overloaded" in error_str or "529" in error_str:
            logger.warning("Anthropic API overloaded")
            raise AnthropicAPIError(
                "Service temporarily overloaded. Please try again later.",
                status_code=529,
                error_type="overloaded"
            )
        
        # Re-raise as generic API error
        logger.error(f"Anthropic API error: {error}")
        raise AnthropicAPIError(str(error), error_type="api_error")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check API connectivity and return status
        
        Returns:
            Health status dictionary
        """
        try:
            # Simple request to verify connectivity
            response = await self._client.messages.create(
                model="claude-3-haiku-20240307",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=10
            )
            
            return {
                "status": "healthy",
                "provider": "anthropic",
                "model": response.model,
                "latency_ms": None,
                "error": None
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "provider": "anthropic",
                "model": None,
                "latency_ms": None,
                "error": str(e)
            }
    
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about available models
        
        Returns:
            Model information dictionary
        """
        return {
            "current_model": self.config.default_model.value,
            "available_models": [m.value for m in ClaudeModel],
            "max_tokens_default": self.config.max_tokens,
            "supports_vision": True,
            "supports_tools": True,
            "supports_streaming": True
        }


# Convenience function for quick usage
def create_anthropic_client(
    api_key: Optional[str] = None,
    model: str = "claude-3-5-sonnet-20241022",
    **kwargs
) -> AnthropicClient:
    """
    Create Anthropic client with simple parameters
    
    Args:
        api_key: API key (defaults to env var)
        model: Model name
        **kwargs: Additional config options
        
    Returns:
        Configured AnthropicClient
    """
    if api_key:
        config = AnthropicConfig(
            api_key=api_key,
            default_model=ClaudeModel(model),
            **kwargs
        )
        return AnthropicClient(config)
    
    return AnthropicClient()
