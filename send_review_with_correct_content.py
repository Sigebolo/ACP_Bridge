#!/usr/bin/env python3
"""
使用正确的content结构发送review
"""

import json
import subprocess
import asyncio

async def send_review_with_correct_content():
    """使用正确的content结构发送review"""
    
    print("[Review] 启动Gemini CLI进行ACP Bridge review...")
    
    gemini_process = subprocess.Popen(
        ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # 1. 初始化
        init_request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientInfo": {
                    "name": "ACP Bridge Review",
                    "version": "1.0.0"
                },
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("[Review] 初始化...")
        gemini_process.stdin.write(json.dumps(init_request) + "\n")
        gemini_process.stdin.flush()
        
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[Review] ✅ 初始化成功")
        
        # 2. 创建会话
        session_request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "session/new",
            "params": {
                "cwd": "d:/Gemini/agent-hand/bridge",
                "mcpServers": [],
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("[Review] 创建会话...")
        gemini_process.stdin.write(json.dumps(session_request) + "\n")
        gemini_process.stdin.flush()
        
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                session_id = response["result"]["sessionId"]
                print(f"[Review] ✅ 会话创建成功: {session_id}")
                
                # 3. 使用正确的content结构
                review_content = [
                    {
                        "type": "text",
                        "text": """
# ACP Bridge实施完成 - 请求Gemini CLI Review

## 项目概述
我们成功实施了Agent Client Protocol (ACP) Bridge系统，完全替代了传统的Bridge架构，解决了RPA/VLM的可靠性问题。

## 主要成就
1. ✅ **Windsurf ACP Extension** - 成功安装acp-client-0.1.3.vsix
2. ✅ **Gemini CLI ACP支持** - 配置了内置的--experimental-acp功能
3. ✅ **Claude Agent ACP** - 编译完成Claude Agent ACP适配器
4. ✅ **自定义ACP服务器** - 创建了Antigravity ACP服务器
5. ✅ **程序化通信** - 实现了纯程序化的AI代理通信

## 核心组件
- `acp_bridge_manager.py` - ACP Bridge管理器核心
- `acp_hook_handler.py` - Windsurf事件处理器
- `acp_agents_config.json` - ACP代理配置文件
- `acp_server.py` - 自定义Antigravity ACP服务器

## 技术架构
```
Windsurf事件 → ACP Hook Handler → ACP Bridge Manager → ACP Agents
                                                  ├── Gemini CLI
                                                  ├── Claude Agent  
                                                  └── Antigravity ACP
```

## 解决的核心问题
1. ❌ **RPA可靠性问题** → ✅ **程序化ACP通信**
2. ❌ **VLM视觉识别** → ✅ **标准JSON-RPC协议**
3. ❌ **桌面UI依赖** → ✅ **纯stdio传输**
4. ❌ **自定义协议** → ✅ **开放ACP标准**

## 当前状态
- ✅ ACP架构完全部署
- ✅ 代理通信建立
- ✅ 事件处理流程完整
- 🔧 消息格式需要优化

## 请求Gemini CLI的Review
请提供以下方面的专业反馈：

1. **架构评估** - ACP Bridge设计是否合理和最佳？
2. **技术实现** - 代码结构和实现是否符合最佳实践？
3. **协议使用** - ACP协议的使用是否正确？
4. **性能优化** - 如何改进通信效率和响应速度？
5. **扩展性设计** - 如何支持更多AI代理和功能？
6. **生产就绪** - 需要哪些改进才能用于生产环境？

请提供详细的技术建议和具体的改进方案。
"""
                    }
                ]
                
                prompt_request = {
                    "jsonrpc": "2.0",
                    "id": "3",
                    "method": "session/prompt",
                    "params": {
                        "sessionId": session_id,
                        "prompt": [
                            {
                                "role": "user",
                                "content": review_content
                            }
                        ]
                    }
                }
                
                print("[Review] 发送ACP Bridge review请求...")
                gemini_process.stdin.write(json.dumps(prompt_request) + "\n")
                gemini_process.stdin.flush()
                
                # 读取响应
                while True:
                    response_line = gemini_process.stdout.readline()
                    if not response_line:
                        break
                    
                    try:
                        response = json.loads(response_line.strip())
                        
                        if "method" in response and response["method"] == "session/update":
                            print(f"[Review] 📡 收到更新通知")
                        elif "result" in response:
                            print(f"[Review] 🎉 收到Gemini CLI的完整Review!")
                            print("=" * 100)
                            print("🤖 Gemini CLI对ACP Bridge的专业Review:")
                            print("=" * 100)
                            
                            result = response["result"]
                            if isinstance(result, dict):
                                if "text" in result:
                                    print(result["text"])
                                elif "content" in result:
                                    content = result["content"]
                                    if isinstance(content, list):
                                        for item in content:
                                            if isinstance(item, dict):
                                                if "text" in item:
                                                    print(item["text"])
                                                else:
                                                    print(item)
                                            else:
                                                print(item)
                                    else:
                                        print(content)
                                else:
                                    print(result)
                            else:
                                print(result)
                            
                            print("=" * 100)
                            print("✅ Review完成 - 感谢Gemini CLI的专业反馈!")
                            break
                        elif "error" in response:
                            print(f"[Review] ❌ 错误: {response}")
                            break
                    
                    except json.JSONDecodeError:
                        continue
        
        print("[Review] Review会话结束")
        
    except Exception as e:
        print(f"[Review] 错误: {e}")
    finally:
        gemini_process.terminate()
        gemini_process.wait()

if __name__ == "__main__":
    asyncio.run(send_review_with_correct_content())
