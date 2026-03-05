"""
CrewBot Agent Framework
Agent定义、注册、执行框架
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import logging

from crewbot.core.engine import Agent, AgentConfig, Task, TaskType
from crewbot.router.model_router import ModelRouter, router as default_router

logger = logging.getLogger(__name__)


@dataclass
class Skill:
    """技能定义"""
    name: str
    description: str
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    examples: List[Dict] = field(default_factory=list)


class LLMAgent(Agent):
    """
    基于LLM的Agent
    可以调用不同的模型提供商
    """
    
    def __init__(self, config: AgentConfig, router: ModelRouter = None):
        super().__init__(config)
        self.router = router or default_router
        self.conversation_history: List[Dict] = []
        
    async def execute(self, task: Task) -> Dict[str, Any]:
        """执行任务 - 调用LLM"""
        logger.info(f"LLMAgent {self.config.name} processing: {task.name}")
        self.status = "busy"
        self.current_task = task.id
        
        try:
            # 1. 选择模型
            model_config = self.router.select_model(
                task_content=task.description,
                task_type=task.task_type.value,
                budget=task.budget
            )
            
            if not model_config:
                raise Exception("No suitable model available")
            
            # 2. 构建提示词
            prompt = self._build_prompt(task)
            
            # 3. 调用模型（模拟）
            # 实际实现中这里会调用OpenAI/Claude等API
            result = await self._call_llm(model_config, prompt)
            
            # 4. 更新历史
            self.conversation_history.append({
                "task": task.name,
                "model": model_config.name,
                "input": task.input_data,
                "output": result,
            })
            
            self.status = "idle"
            self.current_task = None
            
            return {
                "success": True,
                "model_used": model_config.name,
                "output": result,
                "agent": self.config.name,
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            self.status = "error"
            raise
    
    def _build_prompt(self, task: Task) -> str:
        """构建提示词"""
        system_prompt = f"You are {self.config.name}, {self.config.description}\n\n"
        system_prompt += f"Your skills: {', '.join(self.config.skills)}\n\n"
        
        user_prompt = f"Task: {task.name}\n"
        user_prompt += f"Description: {task.description}\n"
        
        if task.input_data:
            user_prompt += f"Input: {task.input_data}\n"
        
        return system_prompt + user_prompt
    
    async def _call_llm(self, model_config, prompt: str) -> str:
        """调用LLM（模拟实现）"""
        # 这里实际应该调用对应的API
        # 为了演示，返回模拟结果
        await asyncio.sleep(0.5)  # 模拟API延迟
        
        return f"[Simulated response from {model_config.name}]\n\n"
        f"Task '{prompt[:50]}...' has been processed.\n"
        f"This is a placeholder response. In production, this would call the actual API."


class AgentRegistry:
    """
    Agent注册中心
    管理所有Agent的注册、发现、加载
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentConfig] = {}
        self.agent_instances: Dict[str, Agent] = {}
        self.skills: Dict[str, Skill] = {}
        logger.info("AgentRegistry initialized")
    
    def register(self, config: AgentConfig, agent_class=LLMAgent) -> Agent:
        """注册Agent"""
        self.agents[config.name] = config
        
        # 创建实例
        agent = agent_class(config)
        self.agent_instances[config.name] = agent
        
        logger.info(f"Agent registered: {config.name}")
        return agent
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """获取Agent实例"""
        return self.agent_instances.get(name)
    
    def get_config(self, name: str) -> Optional[AgentConfig]:
        """获取Agent配置"""
        return self.agents.get(name)
    
    def list_agents(self) -> List[Dict]:
        """列出所有Agent"""
        return [
            {
                "name": name,
                "description": config.description,
                "skills": config.skills,
                "model": config.model,
                "status": self.agent_instances.get(name, {}).get_status() if name in self.agent_instances else "unknown",
            }
            for name, config in self.agents.items()
        ]
    
    def find_agents_by_skill(self, skill: str) -> List[str]:
        """根据技能查找Agent"""
        return [
            name for name, config in self.agents.items()
            if skill in config.skills
        ]
    
    def unregister(self, name: str) -> bool:
        """注销Agent"""
        if name in self.agents:
            del self.agents[name]
            if name in self.agent_instances:
                del self.agent_instances[name]
            logger.info(f"Agent unregistered: {name}")
            return True
        return False


# 预定义的Agent模板
DEFAULT_AGENTS = {
    "writer": AgentConfig(
        name="writer",
        description="专业的写作助手，擅长撰写文章、博客、技术文档",
        skills=["writing", "general"],
        model="claude-3-sonnet",
        temperature=0.7,
    ),
    "coder": AgentConfig(
        name="coder",
        description="资深程序员，擅长代码编写、调试、代码审查",
        skills=["coding", "general"],
        model="gpt-4",
        temperature=0.2,
    ),
    "analyst": AgentConfig(
        name="analyst",
        description="数据分析师，擅长数据分析、可视化、洞察提取",
        skills=["analysis", "research", "general"],
        model="claude-3-sonnet",
        temperature=0.3,
    ),
    "researcher": AgentConfig(
        name="researcher",
        description="研究专家，擅长信息搜集、文献综述、深度研究",
        skills=["research", "analysis", "general"],
        model="claude-3-opus",
        temperature=0.5,
    ),
}


def create_default_agents(registry: AgentRegistry) -> None:
    """创建默认Agent"""
    for config in DEFAULT_AGENTS.values():
        registry.register(config)
    logger.info(f"Created {len(DEFAULT_AGENTS)} default agents")


# 全局注册表
registry = AgentRegistry()
