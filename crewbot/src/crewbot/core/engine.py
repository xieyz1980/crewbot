"""
CrewBot Core Engine - 编排调度引擎
负责任务分解、Agent调度、流程控制
"""

import asyncio
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    PENDING = "pending"
    SCHEDULING = "scheduling"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class TaskType(Enum):
    CODING = "coding"
    WRITING = "writing"
    ANALYSIS = "analysis"
    RESEARCH = "research"
    GENERAL = "general"


@dataclass
class Task:
    """任务定义"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    task_type: TaskType = TaskType.GENERAL
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    parent_task: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    max_retries: int = 3
    retry_count: int = 0
    priority: int = 1  # 1-10, 10为最高
    budget: float = 1.0  # 成本预算（美元）
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "task_type": self.task_type.value,
            "status": self.status.value,
            "assigned_agent": self.assigned_agent,
            "created_at": self.created_at.isoformat(),
            "priority": self.priority,
            "budget": self.budget,
        }


@dataclass
class AgentConfig:
    """Agent配置"""
    name: str
    description: str
    skills: List[str]
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4000
    timeout: int = 300
    resource_limits: Dict[str, Any] = field(default_factory=dict)


class Agent:
    """Agent基类"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.status = "idle"
        self.current_task: Optional[str] = None
        logger.info(f"Agent {config.name} initialized")
    
    async def execute(self, task: Task) -> Dict[str, Any]:
        """执行任务 - 子类需要重写"""
        raise NotImplementedError("Subclasses must implement execute()")
    
    def get_status(self) -> str:
        return self.status


class SimpleAgent(Agent):
    """简单示例Agent - 用于测试"""
    
    async def execute(self, task: Task) -> Dict[str, Any]:
        logger.info(f"Agent {self.config.name} executing task: {task.name}")
        self.status = "busy"
        self.current_task = task.id
        
        # 模拟处理时间
        await asyncio.sleep(1)
        
        result = {
            "agent": self.config.name,
            "task": task.name,
            "output": f"Processed: {task.description}",
            "timestamp": datetime.now().isoformat(),
        }
        
        self.status = "idle"
        self.current_task = None
        return result


class CoreEngine:
    """
    CrewBot核心编排引擎
    - 任务管理
    - Agent调度
    - 状态管理
    - 事件驱动
    """
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.agents: Dict[str, Agent] = {}
        self.agent_configs: Dict[str, AgentConfig] = {}
        self.running = False
        self.task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.event_handlers: List[Callable] = []
        logger.info("CoreEngine initialized")
    
    def register_agent(self, agent: Agent) -> None:
        """注册Agent"""
        self.agents[agent.config.name] = agent
        self.agent_configs[agent.config.name] = agent.config
        logger.info(f"Agent registered: {agent.config.name}")
    
    def create_task(self, 
                   name: str, 
                   description: str,
                   task_type: TaskType = TaskType.GENERAL,
                   input_data: Optional[Dict] = None,
                   priority: int = 1,
                   budget: float = 1.0) -> Task:
        """创建任务"""
        task = Task(
            name=name,
            description=description,
            task_type=task_type,
            input_data=input_data or {},
            priority=priority,
            budget=budget,
        )
        self.tasks[task.id] = task
        # 加入优先级队列 (priority, task_id)
        asyncio.create_task(self.task_queue.put((-priority, task.id)))
        logger.info(f"Task created: {task.name} (ID: {task.id})")
        return task
    
    def select_agent(self, task: Task) -> Optional[Agent]:
        """根据任务类型选择最佳Agent"""
        # 简单策略：根据task_type匹配
        for agent_name, agent in self.agents.items():
            if agent.status == "idle":
                # 检查Agent技能是否匹配任务类型
                if task.task_type.value in agent.config.skills:
                    return agent
        
        # 如果没有匹配的，返回第一个空闲Agent
        for agent in self.agents.values():
            if agent.status == "idle":
                return agent
        
        return None
    
    async def execute_task(self, task: Task) -> bool:
        """执行单个任务"""
        agent = self.select_agent(task)
        
        if not agent:
            logger.warning(f"No available agent for task: {task.name}")
            task.status = TaskStatus.WAITING
            return False
        
        task.status = TaskStatus.RUNNING
        task.assigned_agent = agent.config.name
        task.started_at = datetime.now()
        
        try:
            logger.info(f"Executing task {task.name} with agent {agent.config.name}")
            result = await asyncio.wait_for(
                agent.execute(task),
                timeout=agent.config.timeout
            )
            
            task.output_data = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            logger.info(f"Task completed: {task.name}")
            return True
            
        except asyncio.TimeoutError:
            logger.error(f"Task timeout: {task.name}")
            task.error_message = "Execution timeout"
            task.status = TaskStatus.FAILED
            return False
            
        except Exception as e:
            logger.error(f"Task failed: {task.name}, error: {str(e)}")
            task.error_message = str(e)
            
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.RETRYING
                logger.info(f"Retrying task: {task.name} (attempt {task.retry_count})")
                return False
            else:
                task.status = TaskStatus.FAILED
                return False
    
    async def process_queue(self):
        """处理任务队列"""
        while self.running:
            try:
                # 获取队列中的任务（非阻塞）
                priority, task_id = await asyncio.wait_for(
                    self.task_queue.get(), 
                    timeout=1.0
                )
                
                task = self.tasks.get(task_id)
                if not task or task.status not in [TaskStatus.PENDING, TaskStatus.RETRYING]:
                    continue
                
                success = await self.execute_task(task)
                
                # 如果失败且可以重试，重新加入队列
                if not success and task.status == TaskStatus.RETRYING:
                    await asyncio.sleep(2 ** task.retry_count)  # 指数退避
                    await self.task_queue.put((priority, task_id))
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing queue: {e}")
    
    async def start(self):
        """启动引擎"""
        self.running = True
        logger.info("CoreEngine started")
        await self.process_queue()
    
    def stop(self):
        """停止引擎"""
        self.running = False
        logger.info("CoreEngine stopped")
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        task = self.tasks.get(task_id)
        return task.to_dict() if task else None
    
    def get_all_tasks(self) -> List[Dict]:
        """获取所有任务状态"""
        return [task.to_dict() for task in self.tasks.values()]
    
    def get_agent_status(self) -> List[Dict]:
        """获取所有Agent状态"""
        return [
            {
                "name": name,
                "status": agent.get_status(),
                "current_task": agent.current_task,
                "config": {
                    "model": agent.config.model,
                    "skills": agent.config.skills,
                }
            }
            for name, agent in self.agents.items()
        ]


# 全局引擎实例
engine = CoreEngine()
