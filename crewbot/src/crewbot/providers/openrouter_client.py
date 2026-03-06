"""
OpenRouter Client for CrewBot
统一接入多模型（GPT-4/Claude/DeepSeek/Gemini等）
基于OpenRouter API: https://openrouter.ai/docs
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, AsyncGenerator, Union
from dataclasses import dataclass, field
from enum import Enum
import asyncio

# Configure logging
logger = logging.getLogger(__name__)


class OpenRouterModel(str, Enum):
    """Popular models available through OpenRouter"""
    # OpenAI
    GPT_4O = "openai/gpt-4o"
    GPT_4O_MINI = "openai/gpt-4o-mini"
    GPT_4_TURBO = "openai/gpt-4-turbo"
    GPT_4 = "openai/gpt-4"
    GPT_3_5_TURBO = "openai/gpt-3.5-turbo"
    O1_PREVIEW = "openai/o1-preview"
    O1_MINI = "openai/o1-mini"
    
    # Anthropic
    CLAUDE_3_5_SONNET = "anthropic/claude-3.5-sonnet"
    CLAUDE_3_5_HAIKU = "anthropic/claude-3.5-haiku"
    CLAUDE_3_OPUS = "anthropic/claude-3-opus"
    CLAUDE_3_SONNET = "anthropic/claude-3-sonnet"
    CLAUDE_3_HAIKU = "anthropic/claude-3-haiku"
    
    # DeepSeek
    DEEPSEEK_CHAT = "deepseek/deepseek-chat"
    DEEPSEEK_CODER = "deepseek/deepseek-coder"
    
    # Google
    GEMINI_1_5_PRO = "google/gemini-1.5-pro-latest"
    GEMINI_1_5_FLASH = "google/gemini-1.5-flash-latest"
    GEMINI_PRO = "google/gemini-pro"
    
    # Meta
    LLAMA_3_1_405B = "meta-llama/llama-3.1-405b-instruct"
    LLAMA_3_1_70B = "meta-llama/llama-3.1-70b-instruct"
    LLAMA_3_1_8B = "meta-llama/llama-3.1-8b-instruct"
    
    # Mistral
    MISTRAL_LARGE = "mistralai/mistral-large"
    MISTRAL_MEDIUM = "mistralai/mistral-medium"
    MISTRAL_SMALL = "mistralai/mistral-small"
    
    # Qwen
    QWEN_2_5_72B = "qwen/qwen-2.5-72b-instruct"
    QWEN_2_5_32B = "qwen/qwen-2.5-32b-instruct"
    
    # Default/Balanced choice
    DEFAULT = "openai/gpt-4o-mini"  # Cost-effective default
    BEST = "anthropic/claude-3.5-sonnet"  # Best quality
    CHEAPEST = "openai/gpt-4o-mini"  # Most cost-effective


@dataclass
class ModelPricing:
    """Model pricing info from OpenRouter"""
    prompt: float = 0.0  # per 1K tokens
    completion: float = 0.0  # per 1K tokens


@dataclass
class OpenRouterConfig:
    """Configuration for OpenRouter client"""
    api_key: str
    base_url: str = "https://openrouter.ai/api/v1"
    default_model: str = "openai/gpt-4o-mini"
    timeout: float = 60.0
    max_retries: int = 3
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    site_url: Optional[str] = None  # For rankings on openrouter.ai
    site_name: Optional[str] = None  # App name for rankings
    extra_headers: Dict[str, str] = field(default_factory=dict)


@dataclass
class Message:
    """Chat message structure"""
    role: str  # system, user, assistant, tool
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None


@dataclass
class ChatResponse:
    """Standardized chat response"""
    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str
    provider: str  # e.g., "OpenAI", "Anthropic"
    cost_usd: Optional[float] = None
    raw_response: Optional[Dict] = None


@dataclass
class ModelInfo:
    """Model information from OpenRouter"""
    id: str
    name: str
    description: str
    context_length: int
    pricing: ModelPricing
    architecture: Dict[str, Any]
    top_provider: Dict[str, Any]
    per_request_limits: Optional[Dict] = None


class OpenRouterError(Exception):
    """Base exception for OpenRouter client errors"""
    pass


class OpenRouterAPIError(OpenRouterError):
    """API-specific errors"""
    def __init__(self, message: str, status_code: int = None, error_type: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_type = error_type


class OpenRouterRateLimitError(OpenRouterAPIError):
    """Rate limit exceeded"""
    pass


class OpenRouterAuthenticationError(OpenRouterAPIError):
    """Authentication failed"""
    pass


class OpenRouterModelError(OpenRouterAPIError):
    """Model-specific errors (e.g., context length)"""
    pass


class OpenRouterClient:
    """
    OpenRouter API Client - 统一多模型接入
    
    Features:
    - 单API密钥访问200+模型
    - 自动故障转移
    - 实时价格追踪
    - 流式响应支持
    - 标准化的请求/响应格式
    """
    
    def __init__(self, config: Optional[OpenRouterConfig] = None):
        """
        Initialize OpenRouter client
        
        Args:
            config: Configuration. If None, uses environment variables
        """
        self.config = config or self._create_config_from_env()
        self._client = None
        self._model_cache: Dict[str, ModelInfo] = {}
        self._initialize_client()
        logger.info(f"OpenRouter client initialized with model: {self.config.default_model}")
    
    def _create_config_from_env(self) -> OpenRouterConfig:
        """Create config from environment variables"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise OpenRouterError("OPENROUTER_API_KEY environment variable not set")
        
        return OpenRouterConfig(
            api_key=api_key,
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            default_model=os.getenv("OPENROUTER_DEFAULT_MODEL", "openai/gpt-4o-mini"),
            timeout=float(os.getenv("OPENROUTER_TIMEOUT", "60.0")),
            max_retries=int(os.getenv("OPENROUTER_MAX_RETRIES", "3")),
            temperature=float(os.getenv("OPENROUTER_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENROUTER_MAX_TOKENS")) if os.getenv("OPENROUTER_MAX_TOKENS") else None,
            site_url=os.getenv("OPENROUTER_SITE_URL"),
            site_name=os.getenv("OPENROUTER_SITE_NAME"),
        )
    
    def _initialize_client(self):
        """Initialize the OpenAI-compatible client"""
        try:
            import openai
            
            client_kwargs = {
                "api_key": self.config.api_key,
                "base_url": self.config.base_url,
                "timeout": self.config.timeout,
                "max_retries": self.config.max_retries
            }
            
            self._client = openai.AsyncOpenAI(**client_kwargs)
            logger.debug("OpenRouter async client initialized successfully")
            
        except ImportError:
            logger.error("openai package not installed. Run: pip install openai")
            raise OpenRouterError("openai package not installed")
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter client: {e}")
            raise OpenRouterError(f"Client initialization failed: {e}")
    
    def _get_extra_headers(self) -> Dict[str, str]:
        """Get extra headers for OpenRouter"""
        headers = self.config.extra_headers.copy()
        if self.config.site_url:
            headers["HTTP-Referer"] = self.config.site_url
        if self.config.site_name:
            headers["X-Title"] = self.config.site_name
        return headers
    
    async def chat(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        transforms: Optional[List[str]] = None,  # OpenRouter-specific
        **kwargs
    ) -> Union[ChatResponse, AsyncGenerator[str, None]]:
        """
        Send chat completion request
        
        Args:
            messages: List of messages
            model: Model ID (e.g., "anthropic/claude-3.5-sonnet")
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            tools: Tools for function calling
            tool_choice: Tool choice configuration
            transforms: OpenRouter transforms (e.g., ["middle-out"])
            **kwargs: Additional parameters
            
        Returns:
            ChatResponse or AsyncGenerator for streaming
        """
        model = model or self.config.default_model
        temperature = temperature if temperature is not None else self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens
        
        # Convert Message objects to dict format
        message_dicts = []
        for msg in messages:
            msg_dict: Dict[str, Any] = {"role": msg.role, "content": msg.content}
            if msg.name:
                msg_dict["name"] = msg.name
            if msg.tool_calls:
                msg_dict["tool_calls"] = msg.tool_calls
            if msg.tool_call_id:
                msg_dict["tool_call_id"] = msg.tool_call_id
            message_dicts.append(msg_dict)
        
        request_params: Dict[str, Any] = {
            "model": model,
            "messages": message_dicts,
            "temperature": temperature,
            "stream": stream,
            "extra_headers": self._get_extra_headers(),
            **kwargs
        }
        
        if max_tokens:
            request_params["max_tokens"] = max_tokens
        
        if tools:
            request_params["tools"] = tools
        
        if tool_choice:
            request_params["tool_choice"] = tool_choice
        
        if transforms:
            request_params["transforms"] = transforms
        
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
            
            # Calculate cost if usage info available
            cost_usd = None
            if hasattr(response, 'usage') and response.usage:
                model_info = await self.get_model_info(params['model'])
                if model_info:
                    prompt_cost = (response.usage.prompt_tokens / 1000) * model_info.pricing.prompt
                    completion_cost = (response.usage.completion_tokens / 1000) * model_info.pricing.completion
                    cost_usd = prompt_cost + completion_cost
            
            return ChatResponse(
                content=message.content or "",
                model=response.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                },
                finish_reason=choice.finish_reason,
                provider=getattr(response, 'provider', 'unknown'),
                cost_usd=cost_usd,
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
    
    async def simple_chat(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        """
        Simple one-turn chat
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            model: Optional model override
            
        Returns:
            Assistant's response text
        """
        messages = []
        if system_prompt:
            messages.append(Message(role="system", content=system_prompt))
        messages.append(Message(role="user", content=prompt))
        
        response = await self.chat(messages, model=model)
        return response.content
    
    async def get_available_models(self, refresh: bool = False) -> List[ModelInfo]:
        """
        Get list of available models from OpenRouter
        
        Args:
            refresh: Force refresh cache
            
        Returns:
            List of ModelInfo objects
        """
        if self._model_cache and not refresh:
            return list(self._model_cache.values())
        
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.config.base_url}/models",
                    headers={"Authorization": f"Bearer {self.config.api_key}"}
                )
                response.raise_for_status()
                data = response.json()
                
                models = []
                for model_data in data.get("data", []):
                    pricing = ModelPricing(
                        prompt=model_data.get("pricing", {}).get("prompt", 0),
                        completion=model_data.get("pricing", {}).get("completion", 0)
                    )
                    
                    model_info = ModelInfo(
                        id=model_data.get("id"),
                        name=model_data.get("name", model_data.get("id")),
                        description=model_data.get("description", ""),
                        context_length=model_data.get("context_length", 4096),
                        pricing=pricing,
                        architecture=model_data.get("architecture", {}),
                        top_provider=model_data.get("top_provider", {}),
                        per_request_limits=model_data.get("per_request_limits")
                    )
                    
                    models.append(model_info)
                    self._model_cache[model_info.id] = model_info
                
                logger.info(f"Fetched {len(models)} models from OpenRouter")
                return models
                
        except Exception as e:
            logger.error(f"Failed to fetch models: {e}")
            return list(self._model_cache.values())
    
    async def get_model_info(self, model_id: str) -> Optional[ModelInfo]:
        """Get information about a specific model"""
        if model_id in self._model_cache:
            return self._model_cache[model_id]
        
        # Fetch all models
        models = await self.get_available_models(refresh=True)
        
        for model in models:
            if model.id == model_id:
                return model
        
        return None
    
    async def get_generation_stats(self, generation_id: str) -> Optional[Dict]:
        """
        Get generation statistics by ID
        
        OpenRouter provides generation IDs in response headers
        """
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.config.base_url}/generation",
                    params={"id": generation_id},
                    headers={"Authorization": f"Bearer {self.config.api_key}"}
                )
                response.raise_for_status()
                return response.json().get("data", {})
                
        except Exception as e:
            logger.error(f"Failed to get generation stats: {e}")
            return None
    
    def estimate_cost(self, model_id: str, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for a request
        
        Args:
            model_id: Model ID
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Estimated cost in USD
        """
        model_info = self._model_cache.get(model_id)
        if not model_info:
            logger.warning(f"Model {model_id} not in cache, cannot estimate cost")
            return 0.0
        
        input_cost = (input_tokens / 1000) * model_info.pricing.prompt
        output_cost = (output_tokens / 1000) * model_info.pricing.completion
        return input_cost + output_cost
    
    def _handle_error(self, error: Exception):
        """Handle and classify API errors"""
        error_str = str(error).lower()
        
        # Rate limit errors
        if "rate limit" in error_str or "429" in error_str:
            logger.warning("OpenRouter rate limit exceeded")
            raise OpenRouterRateLimitError(
                "Rate limit exceeded. Please try again later.",
                status_code=429,
                error_type="rate_limit"
            )
        
        # Authentication errors
        if "authentication" in error_str or "401" in error_str or "api key" in error_str:
            logger.error("OpenRouter authentication failed")
            raise OpenRouterAuthenticationError(
                "Authentication failed. Please check your API key.",
                status_code=401,
                error_type="authentication"
            )
        
        # Model errors (context length, etc.)
        if "context length" in error_str or "maximum context" in error_str:
            logger.error("Context length exceeded")
            raise OpenRouterModelError(
                "Input too long. Please reduce the message length.",
                status_code=400,
                error_type="context_length"
            )
        
        # Provider errors
        if any(x in error_str for x in ["provider", "model", "not found"]):
            logger.error(f"Model/provider error: {error}")
            raise OpenRouterModelError(
                f"Model error: {error}",
                error_type="model_error"
            )
        
        # Re-raise as generic API error
        logger.error(f"OpenRouter API error: {error}")
        raise OpenRouterAPIError(str(error), error_type="api_error")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check API connectivity and return status
        
        Returns:
            Health status dictionary
        """
        try:
            start = asyncio.get_event_loop().time()
            
            response = await self._client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5,
                extra_headers=self._get_extra_headers()
            )
            
            latency_ms = (asyncio.get_event_loop().time() - start) * 1000
            
            return {
                "status": "healthy",
                "provider": "openrouter",
                "model": response.model,
                "latency_ms": round(latency_ms, 2),
                "error": None
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "provider": "openrouter",
                "model": None,
                "latency_ms": None,
                "error": str(e)
            }
    
    async def test_models(self, models: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Test connectivity to specified models
        
        Args:
            models: List of model IDs to test. If None, tests popular ones.
            
        Returns:
            Test results for each model
        """
        test_models = models or [
            "openai/gpt-4o-mini",
            "anthropic/claude-3.5-sonnet",
            "deepseek/deepseek-chat",
            "google/gemini-1.5-flash",
        ]
        
        results = {}
        
        for model in test_models:
            try:
                start = asyncio.get_event_loop().time()
                
                response = await self._client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say OK"}],
                    max_tokens=5,
                    extra_headers=self._get_extra_headers()
                )
                
                latency_ms = (asyncio.get_event_loop().time() - start) * 1000
                
                results[model] = {
                    "status": "success",
                    "latency_ms": round(latency_ms, 2),
                    "response": response.choices[0].message.content
                }
                
            except Exception as e:
                results[model] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        return results


# Model selection helpers
class ModelSelector:
    """Helper class for selecting the right model"""
    
    # Task type to recommended models mapping
    TASK_MODELS = {
        "coding": [
            "anthropic/claude-3.5-sonnet",  # Best for code
            "openai/gpt-4o",
            "deepseek/deepseek-coder",
        ],
        "writing": [
            "anthropic/claude-3.5-sonnet",  # Best for creative writing
            "openai/gpt-4o",
            "anthropic/claude-3-opus",
        ],
        "analysis": [
            "openai/gpt-4o",  # Good at structured analysis
            "anthropic/claude-3.5-sonnet",
            "deepseek/deepseek-chat",
        ],
        "chat": [
            "openai/gpt-4o-mini",  # Fast and cheap
            "google/gemini-1.5-flash",
            "anthropic/claude-3.5-haiku",
        ],
        "vision": [
            "openai/gpt-4o",
            "anthropic/claude-3.5-sonnet",
            "google/gemini-1.5-pro",
        ],
    }
    
    PRICING = {
        # Approximate pricing per 1K tokens (prompt + completion avg)
        "openai/gpt-4o": 0.015,
        "openai/gpt-4o-mini": 0.0003,
        "anthropic/claude-3.5-sonnet": 0.006,
        "anthropic/claude-3.5-haiku": 0.00125,
        "deepseek/deepseek-chat": 0.0007,
        "deepseek/deepseek-coder": 0.0007,
        "google/gemini-1.5-pro": 0.007,
        "google/gemini-1.5-flash": 0.0007,
    }
    
    @classmethod
    def for_task(cls, task_type: str, priority: str = "balanced") -> str:
        """
        Get recommended model for task
        
        Args:
            task_type: Type of task (coding, writing, analysis, chat, vision)
            priority: "quality", "speed", or "balanced"
        
        Returns:
            Model ID string
        """
        models = cls.TASK_MODELS.get(task_type, cls.TASK_MODELS["chat"])
        
        if priority == "quality":
            return models[0]
        elif priority == "speed":
            return models[-1]
        else:  # balanced
            return models[1] if len(models) > 1 else models[0]
    
    @classmethod
    def by_budget(cls, budget_per_1k_tokens: float) -> str:
        """Get best model within budget"""
        affordable = [
            (model, price) for model, price in cls.PRICING.items()
            if price <= budget_per_1k_tokens
        ]
        
        if not affordable:
            return "openai/gpt-4o-mini"  # Cheapest fallback
        
        # Sort by price descending to get best quality in budget
        affordable.sort(key=lambda x: x[1], reverse=True)
        return affordable[0][0]


# Convenience function for quick usage
def create_openrouter_client(
    api_key: Optional[str] = None,
    model: str = "openai/gpt-4o-mini",
    **kwargs
) -> OpenRouterClient:
    """
    Create OpenRouter client with simple parameters
    
    Args:
        api_key: API key (defaults to env var)
        model: Default model name
        **kwargs: Additional config options
        
    Returns:
        Configured OpenRouterClient
    """
    if api_key:
        config = OpenRouterConfig(
            api_key=api_key,
            default_model=model,
            **kwargs
        )
        return OpenRouterClient(config)
    
    return OpenRouterClient()


# Example usage / quick test
if __name__ == "__main__":
    async def demo():
        """Demo the OpenRouter client"""
        print("🚀 OpenRouter Client Demo\n")
        
        try:
            client = OpenRouterClient()
            
            # Health check
            print("📡 Health Check...")
            health = await client.health_check()
            print(f"   Status: {health['status']}")
            print(f"   Latency: {health['latency_ms']}ms\n")
            
            # Test multiple models
            print("🧪 Testing Models...")
            test_results = await client.test_models()
            for model, result in test_results.items():
                status = "✅" if result["status"] == "success" else "❌"
                print(f"   {status} {model}: {result.get('latency_ms', 'N/A')}ms")
            print()
            
            # Simple chat
            print("💬 Simple Chat (gpt-4o-mini)...")
            response = await client.simple_chat(
                prompt="What is 2+2? Answer in one word.",
                system_prompt="You are a helpful assistant."
            )
            print(f"   Response: {response}\n")
            
            # Multi-turn conversation
            print("💬 Multi-turn Conversation (Claude)...")
            messages = [
                Message(role="system", content="You are a helpful coding assistant."),
                Message(role="user", content="What is recursion in programming?"),
            ]
            response = await client.chat(
                messages=messages,
                model="anthropic/claude-3.5-sonnet"
            )
            print(f"   Response: {response.content[:100]}...\n")
            
            # Model selection helper
            print("🎯 Model Selection:")
            print(f"   Coding (quality): {ModelSelector.for_task('coding', 'quality')}")
            print(f"   Chat (speed): {ModelSelector.for_task('chat', 'speed')}")
            print(f"   Budget $0.001/1k: {ModelSelector.by_budget(0.001)}")
            
        except OpenRouterError as e:
            print(f"❌ Error: {e}")
    
    asyncio.run(demo())
