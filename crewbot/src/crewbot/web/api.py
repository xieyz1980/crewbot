"""
CrewBot Web API
FastAPI-based REST API and WebSocket interface
"""

import asyncio
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging

from crewbot.core.engine import CoreEngine, Task, TaskType, engine as default_engine
from crewbot.agent.framework import AgentRegistry, create_default_agents, registry as default_registry
from crewbot.router.model_router import ModelRouter, router as default_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for API
class TaskCreateRequest(BaseModel):
    name: str
    description: str
    task_type: str = "general"
    input_data: Optional[Dict] = None
    priority: int = 1
    budget: float = 1.0


class TaskResponse(BaseModel):
    id: str
    name: str
    description: str
    status: str
    assigned_agent: Optional[str] = None
    created_at: str
    priority: int
    budget: float


class AgentInfo(BaseModel):
    name: str
    description: str
    skills: List[str]
    model: str
    status: str


class ModelInfo(BaseModel):
    name: str
    provider: str
    context_length: int
    input_price: float
    output_price: float
    supports_vision: bool
    supports_functions: bool
    available: bool


# Global instances
engine: CoreEngine = default_engine
registry: AgentRegistry = default_registry
router: ModelRouter = default_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # Startup
    logger.info("Starting CrewBot...")
    
    # 注册默认Agent
    create_default_agents(registry)
    for agent in registry.agent_instances.values():
        engine.register_agent(agent)
    
    # 启动引擎
    asyncio.create_task(engine.start())
    
    logger.info("CrewBot started successfully!")
    yield
    
    # Shutdown
    logger.info("Shutting down CrewBot...")
    engine.stop()


# Create FastAPI app
app = FastAPI(
    title="CrewBot API",
    description="轻量级多Agent协作平台",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "CrewBot",
        "version": "0.1.0",
        "description": "轻量级多Agent协作平台",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "engine_running": engine.running,
        "agents_count": len(engine.agents),
        "tasks_count": len(engine.tasks),
    }


# Task endpoints
@app.post("/api/v1/tasks", response_model=TaskResponse)
async def create_task(request: TaskCreateRequest):
    """创建任务"""
    try:
        task_type = TaskType(request.task_type)
    except ValueError:
        task_type = TaskType.GENERAL
    
    task = engine.create_task(
        name=request.name,
        description=request.description,
        task_type=task_type,
        input_data=request.input_data or {},
        priority=request.priority,
        budget=request.budget,
    )
    
    return TaskResponse(
        id=task.id,
        name=task.name,
        description=task.description,
        status=task.status.value,
        assigned_agent=task.assigned_agent,
        created_at=task.created_at.isoformat(),
        priority=task.priority,
        budget=task.budget,
    )


@app.get("/api/v1/tasks", response_model=List[TaskResponse])
async def list_tasks():
    """列出所有任务"""
    tasks = engine.get_all_tasks()
    return [TaskResponse(
        id=t["id"],
        name=t["name"],
        description=t["description"],
        status=t["status"],
        assigned_agent=t.get("assigned_agent"),
        created_at=t["created_at"],
        priority=t["priority"],
        budget=t["budget"],
    ) for t in tasks]


@app.get("/api/v1/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """获取任务详情"""
    task_data = engine.get_task_status(task_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskResponse(
        id=task_data["id"],
        name=task_data["name"],
        description=task_data["description"],
        status=task_data["status"],
        assigned_agent=task_data.get("assigned_agent"),
        created_at=task_data["created_at"],
        priority=task_data["priority"],
        budget=task_data["budget"],
    )


# Agent endpoints
@app.get("/api/v1/agents", response_model=List[AgentInfo])
async def list_agents():
    """列出所有Agent"""
    agents = registry.list_agents()
    return [AgentInfo(
        name=a["name"],
        description=a["description"],
        skills=a["skills"],
        model=a["model"],
        status=a["status"],
    ) for a in agents]


@app.get("/api/v1/agents/status")
async def get_agent_status():
    """获取Agent状态"""
    return engine.get_agent_status()


# Model router endpoints
@app.get("/api/v1/models", response_model=List[ModelInfo])
async def list_models():
    """列出所有可用模型"""
    models = router.get_model_info()
    return [ModelInfo(
        name=m["name"],
        provider=m["provider"],
        context_length=m["context_length"],
        input_price=m["input_price"],
        output_price=m["output_price"],
        supports_vision=m["supports_vision"],
        supports_functions=m["supports_functions"],
        available=m["available"],
    ) for m in models]


@app.post("/api/v1/models/select")
async def select_model(task_content: str, budget: Optional[float] = None):
    """为任务选择最佳模型"""
    model_config = router.select_model(task_content, budget=budget)
    
    if not model_config:
        raise HTTPException(status_code=400, detail="No suitable model found")
    
    cost_estimate = router.estimate_task_cost(task_content)
    
    return {
        "selected_model": model_config.name,
        "provider": model_config.provider.value,
        "estimated_cost": cost_estimate,
    }


@app.post("/api/v1/models/estimate-cost")
async def estimate_cost(
    task_content: str,
    input_tokens: int = 1000,
    output_tokens: int = 500
):
    """估算任务成本"""
    estimate = router.estimate_task_cost(task_content, input_tokens, output_tokens)
    return estimate


# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket实时通信"""
    await websocket.accept()
    logger.info("WebSocket client connected")
    
    try:
        while True:
            # 发送当前状态
            status = {
                "type": "status_update",
                "engine_running": engine.running,
                "tasks_count": len(engine.tasks),
                "agents_status": engine.get_agent_status(),
            }
            await websocket.send_json(status)
            
            # 每秒更新一次
            await asyncio.sleep(1)
            
    except Exception as e:
        logger.info(f"WebSocket client disconnected: {e}")


# Statistics endpoint
@app.get("/api/v1/stats")
async def get_stats():
    """获取系统统计信息"""
    completed_tasks = [t for t in engine.tasks.values() if t.status.value == "completed"]
    failed_tasks = [t for t in engine.tasks.values() if t.status.value == "failed"]
    
    return {
        "total_tasks": len(engine.tasks),
        "completed_tasks": len(completed_tasks),
        "failed_tasks": len(failed_tasks),
        "pending_tasks": len(engine.tasks) - len(completed_tasks) - len(failed_tasks),
        "agents_count": len(engine.agents),
        "available_models": len(router.get_available_models()),
    }


def run_server(host: str = "0.0.0.0", port: int = 8080):
    """运行服务器"""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
