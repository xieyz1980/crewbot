"""
Retry mechanism and error handling for CrewBot
Provides exponential backoff, circuit breaker, and failure recovery
"""

import asyncio
import logging
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, Tuple, Union
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class RetryStrategy(Enum):
    """Retry strategies"""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR = "linear"
    FIXED = "fixed"
    NONE = "none"


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered


@dataclass
class RetryConfig:
    """Configuration for retry mechanism"""
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
    on_retry: Optional[Callable[[Exception, int], None]] = None
    on_giveup: Optional[Callable[[Exception], None]] = None
    jitter: bool = True
    jitter_max: float = 1.0


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    half_open_max_calls: int = 3
    success_threshold: int = 2


@dataclass
class RetryResult:
    """Result of a retry operation"""
    success: bool
    result: Any = None
    error: Optional[Exception] = None
    attempts: int = 0
    total_time: float = 0.0
    retry_history: List[Dict] = field(default_factory=list)


class RetryExhaustedError(Exception):
    """Raised when all retry attempts are exhausted"""
    def __init__(self, message: str, last_error: Exception = None, attempts: int = 0):
        super().__init__(message)
        self.last_error = last_error
        self.attempts = attempts


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass


class RetryHandler:
    """
    Handles retry logic with exponential backoff and jitter
    """
    
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
    
    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for given attempt
        
        Args:
            attempt: Current attempt number (0-indexed)
            
        Returns:
            Delay in seconds
        """
        if self.config.strategy == RetryStrategy.NONE:
            return 0
        
        if self.config.strategy == RetryStrategy.FIXED:
            delay = self.config.base_delay
        
        elif self.config.strategy == RetryStrategy.LINEAR:
            delay = self.config.base_delay * (attempt + 1)
        
        else:  # EXPONENTIAL_BACKOFF
            delay = self.config.base_delay * (self.config.exponential_base ** attempt)
        
        # Cap at max delay
        delay = min(delay, self.config.max_delay)
        
        # Add jitter to prevent thundering herd
        if self.config.jitter:
            jitter = random.uniform(0, self.config.jitter_max)
            delay += jitter
        
        return delay
    
    async def execute(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> RetryResult:
        """
        Execute function with retry logic
        
        Args:
            func: Async function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            RetryResult with success status and details
        """
        start_time = time.time()
        retry_history = []
        last_error = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                logger.debug(f"Attempt {attempt + 1}/{self.config.max_retries + 1}")
                
                result = await func(*args, **kwargs)
                
                total_time = time.time() - start_time
                
                return RetryResult(
                    success=True,
                    result=result,
                    attempts=attempt + 1,
                    total_time=total_time,
                    retry_history=retry_history
                )
                
            except Exception as e:
                last_error = e
                
                # Check if exception is retryable
                if not isinstance(e, self.config.retryable_exceptions):
                    logger.warning(f"Non-retryable exception: {e}")
                    raise
                
                # Don't retry if this was the last attempt
                if attempt >= self.config.max_retries:
                    break
                
                # Calculate delay
                delay = self.calculate_delay(attempt)
                
                # Record retry
                retry_info = {
                    "attempt": attempt + 1,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "delay": delay,
                    "timestamp": time.time()
                }
                retry_history.append(retry_info)
                
                # Call on_retry callback
                if self.config.on_retry:
                    try:
                        self.config.on_retry(e, attempt + 1)
                    except Exception as callback_error:
                        logger.warning(f"on_retry callback failed: {callback_error}")
                
                logger.warning(
                    f"Attempt {attempt + 1} failed: {e}. "
                    f"Retrying in {delay:.2f}s..."
                )
                
                # Wait before retry
                await asyncio.sleep(delay)
        
        # All retries exhausted
        total_time = time.time() - start_time
        
        if self.config.on_giveup:
            try:
                self.config.on_giveup(last_error)
            except Exception as callback_error:
                logger.warning(f"on_giveup callback failed: {callback_error}")
        
        logger.error(f"All {self.config.max_retries + 1} attempts failed. Last error: {last_error}")
        
        return RetryResult(
            success=False,
            error=last_error,
            attempts=self.config.max_retries + 1,
            total_time=total_time,
            retry_history=retry_history
        )


class CircuitBreaker:
    """
    Circuit breaker pattern implementation
    Prevents cascading failures by temporarily rejecting requests
    """
    
    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        self._lock = asyncio.Lock()
        
        logger.info(f"Circuit breaker '{name}' initialized (CLOSED)")
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call function with circuit breaker protection
        
        Args:
            func: Async function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerOpenError: If circuit is open
        """
        async with self._lock:
            await self._update_state()
            
            if self.state == CircuitState.OPEN:
                logger.warning(f"Circuit '{self.name}' is OPEN - rejecting request")
                raise CircuitBreakerOpenError(
                    f"Circuit breaker '{self.name}' is open"
                )
            
            if self.state == CircuitState.HALF_OPEN:
                if self.half_open_calls >= self.config.half_open_max_calls:
                    logger.warning(f"Circuit '{self.name}' HALF_OPEN limit reached")
                    raise CircuitBreakerOpenError(
                        f"Circuit breaker '{self.name}' half-open limit reached"
                    )
                self.half_open_calls += 1
        
        # Execute the function outside the lock
        try:
            result = await func(*args, **kwargs)
            await self._record_success()
            return result
        except Exception as e:
            await self._record_failure()
            raise
    
    async def _update_state(self):
        """Update circuit state based on time and failures"""
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self.last_failure_time:
                elapsed = time.time() - self.last_failure_time
                if elapsed >= self.config.recovery_timeout:
                    logger.info(f"Circuit '{self.name}' transitioning to HALF_OPEN")
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_calls = 0
                    self.success_count = 0
    
    async def _record_success(self):
        """Record a successful call"""
        async with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                
                if self.success_count >= self.config.success_threshold:
                    logger.info(f"Circuit '{self.name}' transitioning to CLOSED")
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
            else:
                self.failure_count = max(0, self.failure_count - 1)
    
    async def _record_failure(self):
        """Record a failed call"""
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.state == CircuitState.HALF_OPEN:
                logger.warning(f"Circuit '{self.name}' failed in HALF_OPEN - opening")
                self.state = CircuitState.OPEN
            elif self.failure_count >= self.config.failure_threshold:
                if self.state != CircuitState.OPEN:
                    logger.warning(
                        f"Circuit '{self.name}' failure threshold reached - opening"
                    )
                    self.state = CircuitState.OPEN
    
    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "half_open_calls": self.half_open_calls,
            "last_failure_time": self.last_failure_time,
            "config": {
                "failure_threshold": self.config.failure_threshold,
                "recovery_timeout": self.config.recovery_timeout
            }
        }


class FallbackStrategy(Enum):
    """Fallback strategies when all retries fail"""
    RAISE_ERROR = "raise_error"
    RETURN_DEFAULT = "return_default"
    CALL_FALLBACK_FUNCTION = "call_fallback_function"


@dataclass
class FallbackConfig:
    """Configuration for fallback behavior"""
    strategy: FallbackStrategy = FallbackStrategy.RAISE_ERROR
    default_value: Any = None
    fallback_function: Optional[Callable] = None


class ResilientExecutor:
    """
    Combines retry, circuit breaker, and fallback for resilient execution
    """
    
    def __init__(
        self,
        retry_config: Optional[RetryConfig] = None,
        circuit_breaker: Optional[CircuitBreaker] = None,
        fallback_config: Optional[FallbackConfig] = None
    ):
        self.retry_handler = RetryHandler(retry_config)
        self.circuit_breaker = circuit_breaker
        self.fallback_config = fallback_config or FallbackConfig()
    
    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with full resilience stack
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or fallback value
        """
        async def _execute_with_retry():
            return await self.retry_handler.execute(func, *args, **kwargs)
        
        try:
            if self.circuit_breaker:
                result = await self.circuit_breaker.call(_execute_with_retry)
            else:
                result = await _execute_with_retry()
            
            if isinstance(result, RetryResult):
                if result.success:
                    return result.result
                else:
                    raise RetryExhaustedError(
                        "All retry attempts failed",
                        last_error=result.error,
                        attempts=result.attempts
                    )
            return result
            
        except Exception as e:
            return await self._handle_fallback(e)
    
    async def _handle_fallback(self, error: Exception) -> Any:
        """Handle failure with fallback strategy"""
        if self.fallback_config.strategy == FallbackStrategy.RAISE_ERROR:
            raise error
        
        elif self.fallback_config.strategy == FallbackStrategy.RETURN_DEFAULT:
            logger.warning(f"Returning default value due to error: {error}")
            return self.fallback_config.default_value
        
        elif self.fallback_config.strategy == FallbackStrategy.CALL_FALLBACK_FUNCTION:
            if self.fallback_config.fallback_function:
                logger.warning(f"Calling fallback function due to error: {error}")
                return await self.fallback_config.fallback_function()
            else:
                raise ValueError("Fallback function not configured")
        
        else:
            raise error


# Decorators for easy usage

def with_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    **retry_kwargs
):
    """
    Decorator to add retry logic to async functions
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries
        max_delay: Maximum delay cap
        retryable_exceptions: Exceptions that trigger retry
        **retry_kwargs: Additional retry configuration
    """
    config = RetryConfig(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        retryable_exceptions=retryable_exceptions,
        **retry_kwargs
    )
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            handler = RetryHandler(config)
            result = await handler.execute(func, *args, **kwargs)
            
            if result.success:
                return result.result
            else:
                raise RetryExhaustedError(
                    f"Function {func.__name__} failed after {result.attempts} attempts",
                    last_error=result.error,
                    attempts=result.attempts
                )
        
        return wrapper
    return decorator


def with_circuit_breaker(
    name: str,
    failure_threshold: int = 5,
    recovery_timeout: float = 60.0
):
    """
    Decorator to add circuit breaker to async functions
    
    Args:
        name: Circuit breaker name
        failure_threshold: Failures before opening circuit
        recovery_timeout: Seconds before attempting recovery
    """
    config = CircuitBreakerConfig(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout
    )
    
    # Shared circuit breakers storage
    _circuit_breakers: Dict[str, CircuitBreaker] = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if name not in _circuit_breakers:
                _circuit_breakers[name] = CircuitBreaker(name, config)
            
            breaker = _circuit_breakers[name]
            return await breaker.call(func, *args, **kwargs)
        
        return wrapper
    return decorator


# Common retry configurations for different scenarios

RETRY_CONFIG_DEFAULT = RetryConfig(
    max_retries=3,
    base_delay=1.0,
    max_delay=30.0,
    strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
    jitter=True
)

RETRY_CONFIG_API_CALLS = RetryConfig(
    max_retries=5,
    base_delay=1.0,
    max_delay=60.0,
    strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
    retryable_exceptions=(ConnectionError, TimeoutError, Exception),
    jitter=True
)

RETRY_CONFIG_DATABASE = RetryConfig(
    max_retries=3,
    base_delay=0.5,
    max_delay=10.0,
    strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
    jitter=True
)

RETRY_CONFIG_AGGRESSIVE = RetryConfig(
    max_retries=10,
    base_delay=0.1,
    max_delay=5.0,
    strategy=RetryStrategy.LINEAR,
    jitter=False
)


# Utility functions

async def retry_with_fallback(
    func: Callable,
    fallback_value: Any,
    max_retries: int = 3,
    **retry_kwargs
) -> Any:
    """
    Retry function and return fallback value on failure
    
    Args:
        func: Function to retry
        fallback_value: Value to return if all retries fail
        max_retries: Maximum retry attempts
        **retry_kwargs: Additional retry options
        
    Returns:
        Function result or fallback value
    """
    config = RetryConfig(max_retries=max_retries, **retry_kwargs)
    handler = RetryHandler(config)
    
    result = await handler.execute(func)
    
    if result.success:
        return result.result
    else:
        logger.warning(f"Returning fallback value due to: {result.error}")
        return fallback_value


@asynccontextmanager
async def resilience_context(
    retry_config: Optional[RetryConfig] = None,
    circuit_name: Optional[str] = None
):
    """
    Async context manager for resilient execution
    
    Args:
        retry_config: Retry configuration
        circuit_name: Circuit breaker name (optional)
    """
    executor = ResilientExecutor(retry_config=retry_config)
    
    if circuit_name:
        executor.circuit_breaker = CircuitBreaker(circuit_name)
    
    try:
        yield executor
    except Exception as e:
        logger.error(f"Resilience context failed: {e}")
        raise
