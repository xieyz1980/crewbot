"""
CrewBot 测试用例
"""

import pytest
import asyncio
from crewbot.core import TaskManager, Task, TaskStatus, get_orchestrator
from crewbot.router import ModelRouter, TaskType, get_router
from crewbot.agent import WriterAgent, CoderAgent, get_registry, AgentConfig


# ============ 核心模块测试 ============

class TestTaskManager:
    """任务管理器测试"""
    
    @pytest.fixture
    async def task_manager(self):
        return TaskManager()
    
    @pytest.mark.asyncio
    async def test_create_task(self):
        """测试创建任务"""
        manager = TaskManager()
        task = await manager.create_task(
            name="测试任务",
            description="这是一个测试任务",
            input_data={"key": "value"}
        )
        
        assert task.name == "测试任务"
        assert task.status == TaskStatus.PENDING
        assert task.id is not None
    
    @pytest.mark.asyncio
    async def test_get_task(self):
        """测试获取任务"""
        manager = TaskManager()
        task = await manager.create_task(
            name="测试任务",
            description="描述",
            input_data={}
        )
        
        retrieved = await manager.get_task(task.id)
        assert retrieved is not None
        assert retrieved.name == task.name
    
    @pytest.mark.asyncio
    async def test_update_task_status(self):
        """测试更新任务状态"""
        manager = TaskManager()
        task = await manager.create_task(
            name="测试任务",
            description="描述",
            input_data={}
        )
        
        await manager.update_task_status(
            task.id,
            TaskStatus.COMPLETED,
            output_data={"result": "成功"}
        )
        
        updated = await manager.get_task(task.id)
        assert updated.status == TaskStatus.COMPLETED
        assert updated.output_data["result"] == "成功"
    
    @pytest.mark.asyncio
    async def test_list_tasks(self):
        """测试列出任务"""
        manager = TaskManager()
        
        # 创建多个任务
        for i in range(3):
            await manager.create_task(
                name=f"任务{i}",
                description="描述",
                input_data={}
            )
        
        tasks = await manager.list_tasks()
        assert len(tasks) == 3


# ============ 路由模块测试 ============

class TestModelRouter:
    """模型路由器测试"""
    
    @pytest.fixture
    def router(self):
        return ModelRouter()
    
    def test_classify_task_writing(self, router):
        """测试写作任务分类"""
        prompt = "帮我写一篇关于AI的文章"
        task_type = router.classify_task(prompt)
        assert task_type in [TaskType.CREATIVE_WRITING, TaskType.TECHNICAL_WRITING]
    
    def test_classify_task_code(self, router):
        """测试代码任务分类"""
        prompt = "写一个Python函数处理数据"
        task_type = router.classify_task(prompt)
        assert task_type == TaskType.CODE_GENERATION
    
    def test_classify_task_analysis(self, router):
        """测试分析任务分类"""
        prompt = "分析这个数据集的趋势"
        task_type = router.classify_task(prompt)
        assert task_type == TaskType.DATA_ANALYSIS
    
    def test_select_model(self, router):
        """测试模型选择"""
        prompt = "写一段代码"
        model_name, model_config = router.select_model(prompt)
        
        assert model_name is not None
        assert model_config is not None
        assert model_name in router.models
    
    def test_estimate_cost(self, router):
        """测试成本估算"""
        prompt = "这是一个测试提示词"
        cost = router.estimate_cost(prompt, "gpt-3.5-turbo", output_tokens=100)
        
        assert cost > 0
        assert isinstance(cost, float)


# ============ Agent模块测试 ============

class TestAgent:
    """Agent测试"""
    
    @pytest.mark.asyncio
    async def test_writer_agent(self):
        """测试写作Agent"""
        agent = WriterAgent()
        
        result = await agent.execute({
            "task": "写作",
            "topic": "AI技术",
            "style": "正式"
        })
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_coder_agent(self):
        """测试编程Agent"""
        agent = CoderAgent()
        
        result = await agent.execute({
            "task": "写一个函数",
            "language": "python"
        })
        
        assert result is not None
        assert "def" in result  # 应该包含函数定义
    
    @pytest.mark.asyncio
    async def test_agent_memory(self):
        """测试Agent记忆功能"""
        agent = WriterAgent()
        
        # 添加记忆
        agent.add_to_memory("user", "你好")
        agent.add_to_memory("assistant", "你好！有什么可以帮助你？")
        
        memory = agent.get_memory()
        assert len(memory) == 2
        assert memory[0]["role"] == "user"


# ============ 集成测试 ============

class TestIntegration:
    """集成测试"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """测试完整工作流程"""
        # 初始化组件
        orchestrator = get_orchestrator()
        registry = get_registry()
        router = get_router()
        
        # 1. 创建任务
        task = await orchestrator.task_manager.create_task(
            name="写代码",
            description="写一个Python函数",
            input_data={
                "task": "写一个排序函数",
                "language": "python"
            }
        )
        
        assert task.status == TaskStatus.PENDING
        
        # 2. 任务应该被自动分配Agent
        agent_id = await orchestrator._select_agent(task)
        assert agent_id is not None
        
        # 3. 验证Agent存在
        agent = registry.get(agent_id)
        assert agent is not None
    
    @pytest.mark.asyncio
    async def test_model_routing(self):
        """测试模型路由功能"""
        router = get_router()
        
        # 不同类型的任务应该选择不同的模型
        writing_prompt = "写一篇文章"
        code_prompt = "写一个函数"
        
        writing_model, _ = router.select_model(writing_prompt)
        code_model, _ = router.select_model(code_prompt)
        
        # 验证模型被正确选择
        assert writing_model in router.models
        assert code_model in router.models


# ============ 性能测试 ============

@pytest.mark.asyncio
async def test_concurrent_tasks():
    """测试并发任务处理"""
    manager = TaskManager()
    
    # 创建多个并发任务
    tasks = []
    for i in range(10):
        task = await manager.create_task(
            name=f"并发任务{i}",
            description="测试并发",
            input_data={}
        )
        tasks.append(task)
    
    # 验证所有任务都被创建
    assert len(tasks) == 10
    
    # 验证可以并发获取
    results = await asyncio.gather(*[
        manager.get_task(t.id) for t in tasks
    ])
    
    assert all(r is not None for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])