"""
CrewBot - 轻量级多Agent协作平台
"""

__version__ = "0.1.0"
__author__ = "CrewBot Team"

from crewbot.core.engine import CoreEngine, Task, TaskType, Agent, AgentConfig
from crewbot.agent.framework import AgentRegistry, LLMAgent
from crewbot.router.model_router import ModelRouter

__all__ = [
    "CoreEngine",
    "Task",
    "TaskType",
    "Agent",
    "AgentConfig",
    "AgentRegistry",
    "LLMAgent",
    "ModelRouter",
]
