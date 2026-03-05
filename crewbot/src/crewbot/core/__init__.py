# CrewBot Core

"""
CrewBot - 轻量级多Agent协作平台
核心引擎模块
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """任务定义"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    agent_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "status": self.status.value,
            "agent_id": self.agent_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "error": self.error
        }


class TaskManager:
    """任务管理器"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self._lock = asyncio.Lock()
    
    async def create_task(self, name: str, description: str, 
                         input_data: Dict[str, Any]) -> Task:
        """创建新任务"""
        task = Task(
            name=name,
            description=description,
            input_data=input_data
        )
        async with self._lock:
            self.tasks[task.id] = task
        logger.info(f"创建任务: {task.id} - {name}")
        return task
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    async def update_task_status(self, task_id: str, 
                                 status: TaskStatus,
                                 output_data: Optional[Dict] = None,
                                 error: Optional[str] = None):
        """更新任务状态"""
        async with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.status = status
                task.updated_at = time.time()
                if output_data:
                    task.output_data = output_data
                if error:
                    task.error = error
                logger.info(f"更新任务状态: {task_id} -> {status.value}")
    
    async def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """列出任务"""
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return sorted(tasks, key=lambda x: x.created_at, reverse=True)
    
    async def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        async with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
                    task.status = TaskStatus.CANCELLED
                    task.updated_at = time.time()
                    logger.info(f"取消任务: {task_id}")
                    return True
        return False


class CrewOrchestrator:
    """Crew编排器 - 核心引擎"""
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.agents: Dict[str, Any] = {}
        self.running = False
    
    def register_agent(self, agent_id: str, agent: Any):
        """注册Agent"""
        self.agents[agent_id] = agent
        logger.info(f"注册Agent: {agent_id}")
    
    async def execute_task(self, task: Task) -> Task:
        """执行任务"""
        try:
            # 更新任务状态为运行中
            await self.task_manager.update_task_status(
                task.id, TaskStatus.RUNNING
            )
            
            # 根据任务类型选择Agent
            if not task.agent_id:
                task.agent_id = await self._select_agent(task)
            
            agent = self.agents.get(task.agent_id)
            if not agent:
                raise ValueError(f"Agent not found: {task.agent_id}")
            
            # 执行Agent
            logger.info(f"执行任务: {task.id} with Agent: {task.agent_id}")
            result = await agent.execute(task.input_data)
            
            # 更新任务完成
            await self.task_manager.update_task_status(
                task.id,
                TaskStatus.COMPLETED,
                output_data={"result": result}
            )
            
            return await self.task_manager.get_task(task.id)
            
        except Exception as e:
            logger.error(f"任务执行失败: {task.id}, 错误: {str(e)}")
            await self.task_manager.update_task_status(
                task.id,
                TaskStatus.FAILED,
                error=str(e)
            )
            raise
    
    async def _select_agent(self, task: Task) -> str:
        """智能选择Agent"""
        # 简单实现：根据任务名称关键词匹配
        task_name = task.name.lower()
        
        if any(kw in task_name for kw in ["写", "write", "文章", "article"]):
            return "writer"
        elif any(kw in task_name for kw in ["代码", "code", "编程", "program"]):
            return "coder"
        elif any(kw in task_name for kw in ["分析", "analyze", "数据", "data"]):
            return "analyst"
        else:
            # 默认使用第一个注册的Agent
            return list(self.agents.keys())[0] if self.agents else "default"
    
    async def start(self):
        """启动编排器"""
        self.running = True
        logger.info("CrewOrchestrator 启动")
    
    async def stop(self):
        """停止编排器"""
        self.running = False
        logger.info("CrewOrchestrator 停止")


# 全局实例
_orchestrator: Optional[CrewOrchestrator] = None

def get_orchestrator() -> CrewOrchestrator:
    """获取全局编排器实例"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = CrewOrchestrator()
    return _orchestrator