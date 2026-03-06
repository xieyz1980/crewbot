"""
OpenAI API Client for CrewBot
Provides integration with OpenAI GPT models
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


class OpenAIModel(str, Enum):
    """Supported OpenAI models"""
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo-preview"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


@dataclass
class OpenAIConfig:
    """Configuration for OpenAI client"""
    api_key: str
    base_url: Optional[str] = None
    default_model: OpenAIModel = OpenAIModel.GPT_4O
    timeout: float = 60.0
    max_retries: int = 3
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    organization: Optional[str] = None


@dataclass
class Message:
    """Chat message structure"""
    role: str  # system, user, assistant, function
    content: str
    name: Optional[str] = None
    function_call: Optional[Dict] = None


@dataclass
class ChatResponse:
    """Standardized chat response"""
    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str
    raw_response: Optional[Dict] = None


class OpenAIError(Exception):
    """Base exception for OpenAI client errors"""
    pass


class OpenAIAPIError(OpenAIError):
    """API-specific errors"""
    def __init__(self, message: str, status_code: int = None, error_type: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_type = error_type


class OpenAIRateLimitError(OpenAIAPIError):
    """Rate limit exceeded"""
    pass


class OpenAIAuthenticationError(OpenAIAPIError):
    """Authentication failed"""
    pass


class OpenAIClient:
    """
    OpenAI API Client with full error handling and retry support
    """
    
    def __init__(self, config: Optional[OpenAIConfig] = None):
        """
        Initialize OpenAI client
        
        Args:
            config: OpenAI configuration. If None, uses environment variables
        """
        self.config = config or self._create_config_from_env()
        self._client = None
        self._initialize_client()
        logger.info(f"OpenAI client initialized with model: {self.config.default_model}")
    
    def _create_config_from_env(self) -> OpenAIConfig:
        """Create config from environment variables"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise OpenAIError("OPENAI_API_KEY environment variable not set")
        
        return OpenAIConfig(
            api_key=api_key,
            base_url=os.getenv("OPENAI_BASE_URL"),
            default_model=OpenAIModel(os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")),
            timeout=float(os.getenv("OPENAI_TIMEOUT", "60.0")),
            max_retries=int(os.getenv("OPENAI_MAX_RETRIES", "3")),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS")) if os.getenv("OPENAI_MAX_TOKENS") else None,
            organization=os.getenv("OPENAI_ORGANIZATION")
        )
    
    def _initialize_client(self):
        """Initialize the OpenAI client"""
        try:
            import openai
            
            client_kwargs = {
                "api_key": self.config.api_key,
                "timeout": self.config.timeout,
                "max_retries": self.config.max_retries
            }
            
            if self.config.base_url:
                client_kwargs["base_url"] = self.config.base_url
            
            if self.config.organization:
                client_kwargs["organization"] = self.config.organization
            
            self._client = openai.AsyncOpenAI(**client_kwargs)
            logger.debug("OpenAI async client initialized successfully")
            
        except ImportError:
            logger.error("openai package not installed. Run: pip install openai")
            raise OpenAIError("openai package not installed")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise OpenAIError(f"Client initialization failed: {e}")
    
    async def chat(
        self,
        messages: List[Message],
        model: Optional[OpenAIModel] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        **kwargs
    ) -> Union[ChatResponse, AsyncGenerator[str, None]]:
        """
        Send chat completion request
        
        Args:
            messages: List of messages
            model: Model to use (defaults to config.default_model)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            tools: Optional tools for function calling
            tool_choice: Tool choice configuration
            **kwargs: Additional parameters
            
        Returns:
            ChatResponse or AsyncGenerator for streaming
        """
        model = model or self.config.default_model
        temperature = temperature if temperature is not None else self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens
        
        # Convert Message objects to dict format
        message_dicts = [
            {"role": msg.role, "content": msg.content}
            + ({"name": msg.name} if msg.name else {})
            + ({"function_call": msg.function_call} if msg.function_call else {})
            for msg in messages
        ]
        
        request_params = {
            "model": model.value,
            "messages": message_dicts,
            "temperature": temperature,
            "stream": stream,
            **kwargs
        }
        
        if max_tokens:
            request_params["max_tokens"] = max_tokens
        
        if tools:
            request_params["tools"] = tools
        
        if tool_choice:
            request_params["tool_choice"] = tool_choice
        
        logger.debug(f"Sending chat request: model={model}, messages={len(messages)}")
        
        try:
            if stream:
                return self._stream_chat(request_params)
            else:
                return await self._complete_chat(request_params)
                
        except Exception as e:
            self._handle_error(e)
    
    async def _complete_chat(self, params: Dict) -> ChatResponse:
        """Non-streaming chat completion"""
        try:
            response = await self._client.chat.completions.create(**params)
            
            # Extract response data
            choice = response.choices[0]
            message = choice.message
            
            return ChatResponse(
                content=message.content or "",
                model=response.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                finish_reason=choice.finish_reason,
                raw_response=response.model_dump() if hasattr(response, 'model_dump') else None
            )
            
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise
    
    async def _stream_chat(self, params: Dict) -> AsyncGenerator[str, None]:
        """Streaming chat completion"""
        params["stream"] = True
        
        try:
            stream = await self._client.chat.completions.create(**params)
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Streaming chat failed: {e}")
            raise
    
    async def simple_chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Simple one-turn chat
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Assistant's response text
        """
        messages = []
        if system_prompt:
            messages.append(Message(role="system", content=system_prompt))
        messages.append(Message(role="user", content=prompt))
        
        response = await self.chat(messages)
        return response.content
    
    async def embed(self, text: Union[str, List[str]], model: str = "text-embedding-3-small") -> List[List[float]]:
        """
        Create embeddings for text
        
        Args:
            text: Text or list of texts to embed
            model: Embedding model to use
            
        Returns:
            List of embedding vectors
        """
        texts = [text] if isinstance(text, str) else text
        
        try:
            response = await self._client.embeddings.create(
                model=model,
                input=texts
            )
            
            embeddings = [item.embedding for item in response.data]
            logger.debug(f"Generated {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Embedding creation failed: {e}")
            self._handle_error(e)
    
    def _handle_error(self, error: Exception):
        """Handle and classify API errors"""
        error_str = str(error).lower()
        
        # Rate limit errors
        if "rate limit" in error_str or "429" in error_str:
            logger.warning("OpenAI rate limit exceeded")
            raise OpenAIRateLimitError(
                "Rate limit exceeded. Please try again later.",
                status_code=429,
                error_type="rate_limit"
            )
        
        # Authentication errors
        if "authentication" in error_str or "401" in error_str or "api key" in error_str:
            logger.error("OpenAI authentication failed")
            raise OpenAIAuthenticationError(
                "Authentication failed. Please check your API key.",
                status_code=401,
                error_type="authentication"
            )
        
        # Context length errors
        if "context length" in error_str or "token" in error_str:
            logger.error("Context length exceeded")
            raise OpenAIAPIError(
                "Input too long. Please reduce the message length.",
                status_code=400,
                error_type="context_length"
            )
        
        # Re-raise as generic API error
        logger.error(f"OpenAI API error: {error}")
        raise OpenAIAPIError(str(error), error_type="api_error")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check API connectivity and return status
        
        Returns:
            Health status dictionary
        """
        try:
            # Simple request to verify connectivity
            response = await self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            
            return {
                "status": "healthy",
                "provider": "openai",
                "model": response.model,
                "latency_ms": None,  # Could be tracked with timing
                "error": None
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "provider": "openai",
                "model": None,
                "latency_ms": None,
                "error": str(e)
            }


# Convenience function for quick usage
def create_openai_client(
    api_key: Optional[str] = None,
    model: str = "gpt-4o",
    **kwargs
) -> OpenAIClient:
    """
    Create OpenAI client with simple parameters
    
    Args:
        api_key: API key (defaults to env var)
        model: Model name
        **kwargs: Additional config options
        
    Returns:
        Configured OpenAIClient
    """
    if api_key:
        config = OpenAIConfig(
            api_key=api_key,
            default_model=OpenAIModel(model),
            **kwargs
        )
        return OpenAIClient(config)
    
    return OpenAIClient()
