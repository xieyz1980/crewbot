#!/usr/bin/env python3
"""
CrewBot - 轻量级多Agent协作平台
主入口
"""

import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from crewbot.web import start_web_ui
from crewbot.core import get_orchestrator
from crewbot.agent import get_registry


def main():
    """主函数"""
    print("""
    ╔════════════════════════════════════════════════╗
    ║                                                ║
    ║   🤖 CrewBot - 轻量级多Agent协作平台           ║
    ║                                                ║
    ║   让每个人都能拥有专属的AI团队                 ║
    ║                                                ║
    ╚════════════════════════════════════════════════╝
    """)
    
    # 初始化核心组件
    orchestrator = get_orchestrator()
    registry = get_registry()
    
    print(f"✅ 已加载 {len(registry.list_agents())} 个Agent")
    print(f"✅ 已配置 {len([m for m in registry.list_agents()])} 个模型")
    print()
    
    # 启动Web UI
    import asyncio
    asyncio.run(orchestrator.start())
    
    try:
        start_web_ui(host="0.0.0.0", port=8080)
    except KeyboardInterrupt:
        print("\n👋 感谢使用CrewBot！")
        asyncio.run(orchestrator.stop())


if __name__ == "__main__":
    main()