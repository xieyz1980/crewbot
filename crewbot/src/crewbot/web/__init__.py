# Web UI Module

"""
Web UI - FastAPI + Jinja2模板
提供可视化的Agent管理和任务执行界面
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
from typing import Dict, Any, List
import asyncio

from crewbot.core import get_orchestrator, Task, TaskStatus
from crewbot.agent import get_registry, AgentConfig
from crewbot.router import get_router

logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(title="CrewBot", version="0.1.0")

# 模板配置
templates = Jinja2Templates(directory="templates")

# 全局实例
orchestrator = get_orchestrator()
registry = get_registry()
router = get_router()


# ============ 页面路由 ============

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """首页"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "CrewBot - 轻量级多Agent协作平台"
    })


@app.get("/agents", response_class=HTMLResponse)
async def agents_page(request: Request):
    """Agent管理页面"""
    agents = registry.list_agents()
    return templates.TemplateResponse("agents.html", {
        "request": request,
        "agents": agents
    })


@app.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request):
    """任务管理页面"""
    tasks = await orchestrator.task_manager.list_tasks()
    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "tasks": [t.to_dict() for t in tasks]
    })


@app.get("/models", response_class=HTMLResponse)
async def models_page(request: Request):
    """模型配置页面"""
    models = router.get_model_info()
    return templates.TemplateResponse("models.html", {
        "request": request,
        "models": models
    })


# ============ API路由 ============

@app.get("/api/agents")
async def list_agents():
    """获取Agent列表"""
    return {
        "success": True,
        "data": registry.list_agents()
    }


@app.post("/api/agents")
async def create_agent(config: Dict[str, Any]):
    """创建Agent"""
    try:
        agent_config = AgentConfig(
            name=config.get("name"),
            description=config.get("description", ""),
            model=config.get("model", "gpt-3.5-turbo"),
            temperature=config.get("temperature", 0.7),
            skills=config.get("skills", [])
        )
        agent = registry.create_agent(agent_config)
        return {
            "success": True,
            "data": agent.get_info()
        }
    except Exception as e:
        logger.error(f"创建Agent失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    """获取Agent详情"""
    agent = registry.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {
        "success": True,
        "data": agent.get_info()
    }


@app.post("/api/tasks")
async def create_task(task_data: Dict[str, Any]):
    """创建任务"""
    try:
        # 创建任务
        task = await orchestrator.task_manager.create_task(
            name=task_data.get("name", "未命名任务"),
            description=task_data.get("description", ""),
            input_data=task_data.get("input", {})
        )
        
        # 如果指定了Agent，设置Agent
        if "agent_id" in task_data:
            task.agent_id = task_data["agent_id"]
        
        # 执行任务
        asyncio.create_task(orchestrator.execute_task(task))
        
        return {
            "success": True,
            "data": task.to_dict()
        }
    except Exception as e:
        logger.error(f"创建任务失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/tasks")
async def list_tasks(status: str = None):
    """获取任务列表"""
    task_status = None
    if status:
        try:
            task_status = TaskStatus(status)
        except ValueError:
            pass
    
    tasks = await orchestrator.task_manager.list_tasks(task_status)
    return {
        "success": True,
        "data": [t.to_dict() for t in tasks]
    }


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """获取任务详情"""
    task = await orchestrator.task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "success": True,
        "data": task.to_dict()
    }


@app.post("/api/tasks/{task_id}/cancel")
async def cancel_task(task_id: str):
    """取消任务"""
    success = await orchestrator.task_manager.cancel_task(task_id)
    return {
        "success": success
    }


@app.get("/api/models")
async def list_models():
    """获取模型列表"""
    return {
        "success": True,
        "data": router.get_model_info()
    }


@app.post("/api/chat")
async def chat(message: Dict[str, Any]):
    """聊天接口"""
    try:
        prompt = message.get("message", "")
        preferred_model = message.get("model")
        
        # 智能选择模型
        if preferred_model and preferred_model in router.models:
            model_name = preferred_model
            model_config = router.models[preferred_model]
        else:
            model_name, model_config = router.select_model(prompt)
        
        logger.info(f"使用模型: {model_name}")
        
        # 这里应该调用实际的LLM API
        # 现在返回模拟响应
        response = f"""这是来自 {model_name} 的回复：

我理解了您的问题："{prompt[:50]}..."

作为一个AI助手，我可以帮助您：
1. 回答各类问题
2. 协助写作和编程
3. 分析数据
4. 提供建议和见解

请问有什么具体我可以帮您的吗？

---
*模型: {model_name} | 费用估算: ${router.estimate_cost(prompt, model_name):.4f}*"""
        
        return {
            "success": True,
            "data": {
                "response": response,
                "model": model_name,
                "cost": router.estimate_cost(prompt, model_name)
            }
        }
    except Exception as e:
        logger.error(f"聊天失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """获取统计信息"""
    tasks = await orchestrator.task_manager.list_tasks()
    return {
        "success": True,
        "data": {
            "total_tasks": len(tasks),
            "pending_tasks": len([t for t in tasks if t.status == TaskStatus.PENDING]),
            "running_tasks": len([t for t in tasks if t.status == TaskStatus.RUNNING]),
            "completed_tasks": len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
            "failed_tasks": len([t for t in tasks if t.status == TaskStatus.FAILED]),
            "total_agents": len(registry.list_agents()),
            "available_models": len(router.list_models(enabled_only=True))
        }
    }


# ============ 启动函数 ============

def start_web_ui(host: str = "0.0.0.0", port: int = 8080, debug: bool = False):
    """启动Web UI"""
    logger.info(f"启动CrewBot Web UI: http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")


# 如果直接运行此文件
if __name__ == "__main__":
    start_web_ui()