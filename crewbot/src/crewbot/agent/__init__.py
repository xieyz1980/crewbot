# Agent Framework

"""
Agent框架 - 可扩展的智能体系统
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import time

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Agent配置"""
    name: str
    description: str = ""
    model: str = "gpt-3.5-turbo"  # 默认模型
    temperature: float = 0.7
    max_tokens: int = 4000
    system_prompt: str = ""
    skills: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    memory_enabled: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "system_prompt": self.system_prompt,
            "skills": self.skills,
            "tools": self.tools,
            "memory_enabled": self.memory_enabled
        }


class BaseAgent(ABC):
    """
    Agent基类
    
    所有Agent必须继承此类并实现execute方法
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.memory: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(f"Agent.{config.name}")
        self.logger.info(f"初始化Agent: {config.name}")
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> str:
        """
        执行Agent的核心逻辑
        
        Args:
            input_data: 输入数据，包含task、context等
            
        Returns:
            执行结果字符串
        """
        pass
    
    def add_to_memory(self, role: str, content: str):
        """添加到记忆"""
        if self.config.memory_enabled:
            self.memory.append({
                "role": role,
                "content": content,
                "timestamp": time.time()
            })
            # 限制记忆长度（保留最近20条）
            if len(self.memory) > 20:
                self.memory = self.memory[-20:]
    
    def get_memory(self, limit: int = 10) -> List[Dict[str, str]]:
        """获取记忆"""
        if not self.config.memory_enabled:
            return []
        return [{"role": m["role"], "content": m["content"]} 
                for m in self.memory[-limit:]]
    
    def clear_memory(self):
        """清空记忆"""
        self.memory = []
    
    def get_info(self) -> Dict[str, Any]:
        """获取Agent信息"""
        return {
            "name": self.config.name,
            "description": self.config.description,
            "model": self.config.model,
            "skills": self.config.skills,
            "memory_size": len(self.memory),
            "config": self.config.to_dict()
        }


class WriterAgent(BaseAgent):
    """写作Agent - 擅长各类写作任务"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        if config is None:
            config = AgentConfig(
                name="writer",
                description="专业写作助手，擅长文章、报告、文案等",
                model="claude-3-sonnet",
                temperature=0.8,
                system_prompt="""你是一个专业的写作助手。你的任务是：
1. 根据用户需求撰写高质量内容
2. 结构清晰，逻辑严密
3. 语言流畅，表达准确
4. 适当使用修辞手法增强表现力
""",
                skills=["writing", "editing", "copywriting", "translation"]
            )
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> str:
        """执行写作任务"""
        task = input_data.get("task", "")
        topic = input_data.get("topic", "")
        style = input_data.get("style", "正式")
        length = input_data.get("length", "medium")  # short/medium/long
        
        self.logger.info(f"执行写作任务: {topic}")
        self.add_to_memory("user", f"任务: {task}, 主题: {topic}")
        
        # 这里应该调用实际的LLM API
        # 现在使用模拟实现
        result = f"""# {topic}

这是关于"{topic}"的写作内容。

## 引言

在当前快速发展的技术环境下，{topic}已经成为了一个重要的话题。

## 正文

根据您的要求，我以{style}的风格撰写了这篇文章。内容涵盖了核心要点，并进行了深入的探讨。

## 结论

总的来说，{topic}值得我们持续关注和深入研究。

---
*由CrewBot写作Agent生成*
"""
        
        self.add_to_memory("assistant", result)
        return result


class CoderAgent(BaseAgent):
    """编程Agent - 擅长代码相关任务"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        if config is None:
            config = AgentConfig(
                name="coder",
                description="专业程序员助手，擅长代码编写、审查、调试",
                model="gpt-4",
                temperature=0.2,
                system_prompt="""你是一个专业的编程助手。你的任务是：
1. 编写高质量、可维护的代码
2. 遵循最佳实践和代码规范
3. 添加必要的注释
4. 考虑边界情况和错误处理
""",
                skills=["coding", "debugging", "code_review", "refactoring"],
                tools=["exec", "read", "write"]
            )
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> str:
        """执行编程任务"""
        task = input_data.get("task", "")
        language = input_data.get("language", "python")
        
        self.logger.info(f"执行编程任务: {language}")
        self.add_to_memory("user", f"任务: {task}, 语言: {language}")
        
        # 模拟代码生成
        if "function" in task.lower():
            result = f"""```{language}
def process_data(data):
    \"\"\"
    处理数据的函数
    
    Args:
        data: 输入数据
        
    Returns:
        处理后的结果
    \"\"\"
    if not data:
        return None
    
    # 核心处理逻辑
    result = []
    for item in data:
        processed = item.strip().lower()
        if processed:
            result.append(processed)
    
    return result
```
"""
        else:
            result = f"""```{language}
# {task}

class Solution:
    def __init__(self):
        self.data = []
    
    def run(self):
        \"\"\"主运行函数\"\"\"
        print("程序开始执行...")
        # 实现逻辑
        return self.data

if __name__ == "__main__":
    solution = Solution()
    result = solution.run()
    print(f"结果: {{result}}")
```
"""
        
        self.add_to_memory("assistant", result)
        return result


class AnalystAgent(BaseAgent):
    """分析Agent - 擅长数据分析任务"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        if config is None:
            config = AgentConfig(
                name="analyst",
                description="数据分析专家，擅长数据解读和洞察",
                model="gpt-4",
                temperature=0.3,
                system_prompt="""你是一个数据分析专家。你的任务是：
1. 深入分析数据，发现关键洞察
2. 提供清晰的数据解读
3. 给出可行的建议
4. 使用适当的可视化方式呈现结果
""",
                skills=["data_analysis", "visualization", "reporting"]
            )
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> str:
        """执行分析任务"""
        data = input_data.get("data", "")
        analysis_type = input_data.get("type", "general")
        
        self.logger.info(f"执行分析任务: {analysis_type}")
        
        result = f"""# 数据分析报告

## 数据概览

- 数据类型: {analysis_type}
- 分析时间: {time.strftime("%Y-%m-%d %H:%M")}

## 关键发现

1. **趋势分析**: 数据显示出明显的增长趋势
2. **异常检测**: 发现3个异常值，需要进一步调查
3. **相关性**: 主要指标之间存在强相关性

## 详细分析

### 1. 描述性统计

| 指标 | 数值 |
|------|------|
| 平均值 | 125.5 |
| 中位数 | 118.2 |
| 标准差 | 32.1 |

### 2. 洞察与建议

- 建议1: 关注异常波动的原因
- 建议2: 优化关键指标监控
- 建议3: 建立预警机制

## 结论

基于当前数据分析，建议采取以下行动...
"""
        
        return result


class AgentRegistry:
    """Agent注册中心"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_configs: Dict[str, AgentConfig] = {}
        self._register_default_agents()
    
    def _register_default_agents(self):
        """注册默认Agent"""
        self.register("writer", WriterAgent())
        self.register("coder", CoderAgent())
        self.register("analyst", AnalystAgent())
    
    def register(self, agent_id: str, agent: BaseAgent):
        """注册Agent"""
        self.agents[agent_id] = agent
        self.agent_configs[agent_id] = agent.config
        logger.info(f"注册Agent: {agent_id}")
    
    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """获取Agent"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """列出所有Agent"""
        return [agent.get_info() for agent in self.agents.values()]
    
    def create_agent(self, config: AgentConfig) -> BaseAgent:
        """动态创建Agent"""
        # 根据配置创建对应的Agent类型
        if "writing" in config.skills or config.name == "writer":
            agent = WriterAgent(config)
        elif "coding" in config.skills or config.name == "coder":
            agent = CoderAgent(config)
        elif "data_analysis" in config.skills or config.name == "analyst":
            agent = AnalystAgent(config)
        else:
            # 默认创建通用Agent
            agent = WriterAgent(config)
        
        self.register(config.name, agent)
        return agent


# 全局注册中心
_registry: Optional[AgentRegistry] = None

def get_registry() -> AgentRegistry:
    """获取全局注册中心"""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry