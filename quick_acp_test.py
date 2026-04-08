#!/usr/bin/env python3
"""
快速ACP链路测试
"""

import subprocess
import json
import time
import asyncio

async def quick_acp_test():
    """快速测试ACP Bridge链路"""
    
    print("🚀 快速ACP链路测试")
    print("=" * 40)
    
    # 1. 测试Gemini CLI连接
    print("1️⃣ 测试Gemini CLI连接...")
    try:
        process = subprocess.Popen(
            ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # 发送初始化
        init_msg = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientInfo": {"name": "Quick Test", "version": "1.0"},
                "capabilities": ["file_access"]
            }
        }
        
        process.stdin.write(json.dumps(init_msg) + "\n")
        process.stdin.flush()
        
        # 等待响应
        time.sleep(2)
        
        # 读取响应
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                agent_info = response["result"].get("agentInfo", {})
                print(f"   ✅ Gemini CLI连接成功: {agent_info.get('name', 'Unknown')} v{agent_info.get('version', 'Unknown')}")
            else:
                print("   ❌ Gemini CLI初始化失败")
        else:
            print("   ❌ Gemini CLI无响应")
        
        process.terminate()
        
    except Exception as e:
        print(f"   ❌ Gemini CLI测试失败: {e}")
    
    # 2. 测试Hook Handler
    print("\n2️⃣ 测试Hook Handler...")
    try:
        result = subprocess.run([
            "python", "d:/Gemini/agent-hand/bridge/acp_hook_handler.py",
            "--event", "test",
            "--message", "ACP Bridge测试"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("   ✅ Hook Handler响应正常")
        else:
            print(f"   ❌ Hook Handler错误: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Hook Handler测试失败: {e}")
    
    # 3. 检查配置文件
    print("\n3️⃣ 检查配置文件...")
    try:
        with open("d:/Gemini/agent-hand/bridge/acp_agents_config.json", "r") as f:
            config = json.load(f)
            agents = config.get("agents", [])
            gemini_found = any("Gemini CLI" in agent.get("name", "") for agent in agents)
            
            if gemini_found:
                print("   ✅ Gemini CLI配置存在")
            else:
                print("   ❌ Gemini CLI配置缺失")
                
    except Exception as e:
        print(f"   ❌ 配置文件检查失败: {e}")
    
    # 4. 检查Windsurf配置
    print("\n4️⃣ 检查Windsurf配置...")
    try:
        with open("c:/Users/Administrator/AppData/Roaming/Windsurf/User/settings.json", "r") as f:
            settings = json.load(f)
            hooks = settings.get("windsurf.cascade.hooks", {})
            
            if hooks:
                print("   ✅ Windsurf Cascade Hooks已配置")
                for hook_name in hooks.keys():
                    print(f"      - {hook_name}")
            else:
                print("   ❌ Windsurf Cascade Hooks未配置")
                
    except Exception as e:
        print(f"   ❌ Windsurf配置检查失败: {e}")
    
    print("\n🎯 测试完成!")
    print("如果所有检查都通过，可以在Windsurf中编辑文件来测试ACP通讯。")

if __name__ == "__main__":
    asyncio.run(quick_acp_test())
