"""
CrewBot CLI Entry Point
"""

import argparse
import sys
from crewbot.web.api import run_server


def main():
    parser = argparse.ArgumentParser(description="CrewBot - 轻量级多Agent协作平台")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="服务器主机地址 (默认: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="服务器端口 (默认: 8080)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="CrewBot 0.1.0"
    )
    
    args = parser.parse_args()
    
    print(f"""
🚀 CrewBot v0.1.0
轻量级多Agent协作平台

启动服务器: http://{args.host}:{args.port}
API文档: http://{args.host}:{args.port}/docs
    """)
    
    try:
        run_server(host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n👋 CrewBot stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()
