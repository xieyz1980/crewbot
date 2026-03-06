"""
CrewBot Core Modules
"""

from .retry import (
    RetryHandler,
    RetryConfig,
    RetryResult,
    RetryStrategy,
    RetryExhaustedError,
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
    CircuitBreakerOpenError,
    ResilientExecutor,
    FallbackStrategy,
    FallbackConfig,
    with_retry,
    with_circuit_breaker,
    RETRY_CONFIG_DEFAULT,
    RETRY_CONFIG_API_CALLS,
    RETRY_CONFIG_DATABASE,
    RETRY_CONFIG_AGGRESSIVE,
    retry_with_fallback,
    resilience_context
)

__all__ = [
    # Retry
    "RetryHandler",
    "RetryConfig",
    "RetryResult",
    "RetryStrategy",
    "RetryExhaustedError",
    
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitState",
    "CircuitBreakerOpenError",
    
    # Executor
    "ResilientExecutor",
    "FallbackStrategy",
    "FallbackConfig",
    
    # Decorators
    "with_retry",
    "with_circuit_breaker",
    
    # Presets
    "RETRY_CONFIG_DEFAULT",
    "RETRY_CONFIG_API_CALLS",
    "RETRY_CONFIG_DATABASE",
    "RETRY_CONFIG_AGGRESSIVE",
    
    # Utilities
    "retry_with_fallback",
    "resilience_context"
]
