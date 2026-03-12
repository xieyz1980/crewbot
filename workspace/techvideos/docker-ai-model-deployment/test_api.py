#!/usr/bin/env python3
"""
API测试脚本
用于测试Docker部署的AI模型推理服务
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"

def test_health():
    """测试健康检查接口"""
    print("=" * 50)
    print("测试1: 健康检查")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.json().get('gpu_available'):
            print("✅ GPU可用！")
        else:
            print("⚠️ GPU不可用，将使用CPU推理")
        
        return True
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_info():
    """测试模型信息接口"""
    print("\n" + "=" * 50)
    print("测试2: 模型信息")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/info", timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_generate():
    """测试文本生成接口"""
    print("\n" + "=" * 50)
    print("测试3: 文本生成")
    print("=" * 50)
    
    prompts = [
        "什么是Docker？用简洁的中文回答：",
        "List 3 benefits of using containers:",
        "Explain quantum computing in one sentence:"
    ]
    
    for prompt in prompts:
        print(f"\n📝 Prompt: {prompt}")
        
        data = {
            "prompt": prompt,
            "max_length": 200,
            "temperature": 0.7
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/generate",
                json=data,
                timeout=60
            )
            elapsed = time.time() - start_time
            
            result = response.json()
            print(f"⏱️  耗时: {elapsed:.2f}秒")
            print(f"🤖 生成: {result.get('generated', 'N/A')[:200]}...")
            
        except Exception as e:
            print(f"❌ 错误: {e}")

def test_generate_batch():
    """测试批量生成接口"""
    print("\n" + "=" * 50)
    print("测试4: 批量文本生成")
    print("=" * 50)
    
    data = {
        "prompts": [
            "Docker的优点是什么？",
            "How does GPU acceleration work?",
            "What is containerization?"
        ],
        "max_length": 150,
        "temperature": 0.7
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/generate_batch",
            json=data,
            timeout=120
        )
        elapsed = time.time() - start_time
        
        result = response.json()
        print(f"⏱️  总耗时: {elapsed:.2f}秒")
        print(f"📊 生成数量: {result.get('count', 0)}")
        
        for i, item in enumerate(result.get('results', [])):
            print(f"\n--- 结果 {i+1} ---")
            print(f"Prompt: {item.get('prompt', 'N/A')}")
            print(f"Generated: {item.get('generated', 'N/A')[:150]}...")
            
    except Exception as e:
        print(f"❌ 错误: {e}")

def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 50)
    print("交互模式 (输入 'quit' 退出)")
    print("=" * 50)
    
    while True:
        prompt = input("\n📝 输入你的问题: ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print("再见！")
            break
        
        if not prompt:
            continue
        
        data = {
            "prompt": prompt,
            "max_length": 300,
            "temperature": 0.7
        }
        
        try:
            print("🤔 思考中...")
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/generate",
                json=data,
                timeout=60
            )
            elapsed = time.time() - start_time
            
            result = response.json()
            print(f"\n✨ 回答 (耗时 {elapsed:.2f}秒):")
            print(result.get('generated', 'N/A'))
            
        except Exception as e:
            print(f"❌ 错误: {e}")

def main():
    """主函数"""
    print("🚀 Docker AI模型推理服务测试脚本")
    print(f"API地址: {BASE_URL}")
    
    # 检查服务是否可用
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except:
        print("\n❌ 无法连接到服务，请确保：")
        print("1. Docker容器已启动: docker-compose up -d")
        print("2. 服务正在监听端口 5000")
        sys.exit(1)
    
    # 运行测试
    if test_health():
        test_info()
        test_generate()
        test_generate_batch()
        
        # 询问是否进入交互模式
        print("\n" + "=" * 50)
        choice = input("是否进入交互模式? (y/n): ").strip().lower()
        if choice == 'y':
            interactive_mode()
    else:
        print("\n❌ 健康检查失败，请检查服务状态")
        sys.exit(1)

if __name__ == "__main__":
    main()
