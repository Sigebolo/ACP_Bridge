#!/usr/bin/env python3
"""
修复Claude ACP编码问题并查看Gemini CLI ACP文档
"""

import json
import subprocess
import asyncio
import time
import sys

async def connect_to_claude_acp_encoding_fixed():
    """连接Claude Agent ACP - 修复编码问题"""
    
    print("[Claude ACP] 启动Claude Agent ACP (编码修复版)...")
    
    try:
        # 启动Claude Agent ACP进程，指定UTF-8编码
        claude_process = subprocess.Popen(
            ["node", "d:/Gemini/agent-hand/claude-agent-acp/dist/index.js"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # 1. 初始化Claude Agent
        init_request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientInfo": {
                    "name": "Windsurf ACP Bridge",
                    "version": "1.0.0"
                },
                "capabilities": ["file_access", "terminal", "tools", "streaming"]
            }
        }
        
        print("[Claude ACP] 发送初始化请求...")
        init_json = json.dumps(init_request, ensure_ascii=False)
        claude_process.stdin.write(init_json + "\n")
        claude_process.stdin.flush()
        
        # 读取初始化响应
        response_line = claude_process.stdout.readline()
        if response_line:
            try:
                response = json.loads(response_line.strip())
                print(f"[Claude ACP] ✅ 初始化成功")
                if "result" in response and "agentInfo" in response["result"]:
                    agent_info = response["result"]["agentInfo"]
                    print(f"[Claude ACP] Claude Agent: {agent_info.get('name', 'Unknown')} v{agent_info.get('version', 'Unknown')}")
            except json.JSONDecodeError as e:
                print(f"[Claude ACP] 初始化响应JSON解析错误: {e}")
                print(f"[Claude ACP] 原始响应: {response_line}")
        
        # 2. 创建会话（添加必需参数）
        session_request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "session/new",
            "params": {
                "cwd": "d:/Gemini/agent-hand/bridge",
                "mcpServers": [],
                "capabilities": ["file_access", "terminal", "tools", "streaming"]
            }
        }
        
        print("[Claude ACP] 发送会话创建请求...")
        session_json = json.dumps(session_request, ensure_ascii=False)
        claude_process.stdin.write(session_json + "\n")
        claude_process.stdin.flush()
        
        # 读取会话响应
        response_line = claude_process.stdout.readline()
        if response_line:
            try:
                response = json.loads(response_line.strip())
                print(f"[Claude ACP] 会话响应: {response}")
                
                if "result" in response:
                    session_id = response["result"].get("sessionId", "unknown")
                    print(f"[Claude ACP] ✅ 会话创建成功: {session_id}")
                    
                    # 3. 向Claude介绍ACP Bridge项目
                    project_introduction = """你好Claude！很高兴通过Agent Client Protocol与你连接！

# ACP Bridge项目介绍

我是Windsurf ACP Bridge系统，专门设计来替代传统的Bridge架构，解决RPA/VLM的可靠性问题。

## 项目背景
我们成功实施了完整的Agent Client Protocol (ACP)生态系统：

### 🎯 核心成就
1. **✅ Windsurf ACP Extension** - 已安装acp-client-0.1.3.vsix
2. **✅ Gemini CLI ACP支持** - 配置了内置ACP功能  
3. **✅ Claude Agent ACP** - 你！已经编译完成并准备就绪
4. **✅ 自定义Antigravity ACP** - 完全可控的服务器

### 🏗️ 技术架构
```
Windsurf事件 → ACP Hook Handler → ACP Bridge Manager → ACP Agents
                                                  ├── Gemini CLI
                                                  ├── Claude Agent (就是你！)
                                                  └── Antigravity ACP
```

### 🔧 解决的核心问题
- ❌ RPA桌面自动化 → ✅ 程序化ACP通信
- ❌ VLM视觉识别 → ✅ 标准JSON-RPC协议
- ❌ UI依赖问题 → ✅ 纯stdio传输

### 📁 核心组件
- `acp_bridge_manager.py` - ACP Bridge管理器
- `acp_hook_handler.py` - Windsurf事件处理器
- `acp_agents_config.json` - 代理配置文件
- `acp_server.py` - 自定义Antigravity ACP服务器

### 🎊 当前状态
- ✅ ACP架构完全部署
- ✅ 多代理支持建立
- ✅ 事件处理流程完整
- 🔧 Gemini CLI消息格式需要调试
- 🔧 Claude ACP编码问题已修复

## 🤝 邀请Claude参与

现在我们想邀请你：
1. **作为主要AI代理** - 参与Windsurf的实时协作
2. **提供技术反馈** - 对ACP Bridge架构的建议
3. **协助优化** - 帮助改进系统性能和稳定性

## 📋 测试请求

请你在10秒后反馈：
1. 你是否理解了这个ACP Bridge项目？
2. 你准备好参与Windsurf的实时协作了吗？
3. 你对ACP Bridge有什么技术建议？

期待你的快速响应！🚀

---
*通过Agent Client Protocol发送 - 2026-04-07*
"""
                    
                    prompt_request = {
                        "jsonrpc": "2.0",
                        "id": "3",
                        "method": "session/prompt",
                        "params": {
                            "sessionId": session_id,
                            "prompt": [
                                {
                                    "role": "user",
                                    "content": project_introduction
                                }
                            ]
                        }
                    }
                    
                    print("[Claude ACP] 发送项目介绍...")
                    prompt_json = json.dumps(prompt_request, ensure_ascii=False)
                    claude_process.stdin.write(prompt_json + "\n")
                    claude_process.stdin.flush()
                    
                    print("[Claude ACP] ⏰ 等待Claude的10秒反馈...")
                    
                    # 读取响应，等待15秒
                    start_time = time.time()
                    claude_response = None
                    
                    while time.time() - start_time < 15:
                        response_line = claude_process.stdout.readline()
                        if not response_line:
                            await asyncio.sleep(0.1)
                            continue
                        
                        try:
                            response = json.loads(response_line.strip())
                            
                            if "method" in response and response["method"] == "session/update":
                                print(f"[Claude ACP] 📡 收到更新通知")
                                continue
                            
                            elif "result" in response:
                                claude_response = response["result"]
                                elapsed = time.time() - start_time
                                print(f"[Claude ACP] 🎉 收到Claude响应! (耗时: {elapsed:.1f}秒)")
                                print("=" * 80)
                                print("🤖 Claude Agent的回应:")
                                print("=" * 80)
                                
                                # 格式化输出Claude的响应
                                if isinstance(claude_response, dict):
                                    if "text" in claude_response:
                                        print(claude_response["text"])
                                    elif "content" in claude_response:
                                        content = claude_response["content"]
                                        if isinstance(content, list):
                                            for item in content:
                                                if isinstance(item, dict):
                                                    if "text" in item:
                                                        print(item["text"])
                                                    elif "type" in item and item["type"] == "text":
                                                        print(item.get("text", str(item)))
                                                    else:
                                                        print(item)
                                                else:
                                                    print(item)
                                        else:
                                            print(content)
                                    else:
                                        print(claude_response)
                                else:
                                    print(claude_response)
                                
                                print("=" * 80)
                                break
                            
                            elif "error" in response:
                                print(f"[Claude ACP] ❌ 错误响应: {response}")
                                break
                            
                            else:
                                print(f"[Claude ACP] 📄 其他响应: {response}")
                        
                        except json.JSONDecodeError as e:
                            print(f"[Claude ACP] JSON解析错误: {e}")
                            continue
                        
                        except Exception as e:
                            print(f"[Claude ACP] 处理响应错误: {e}")
                            continue
                    
                    if claude_response:
                        print("[Claude ACP] ✅ Claude Agent成功连接并回应!")
                        print("[Claude ACP] 🎊 ACP Bridge + Claude Agent 集成成功!")
                        print("[Claude ACP] 🚀 现在可以开始Windsurf + Claude的实时协作!")
                    else:
                        print("[Claude ACP] ⚠️ 15秒内未收到Claude响应")
                        print("[Claude ACP] 📋 可能需要检查Claude Agent配置")
                
                elif "error" in response:
                    error_info = response["error"]
                    print(f"[Claude ACP] ❌ 会话创建错误: {error_info}")
                    print(f"[Claude ACP] 错误代码: {error_info.get('code', 'Unknown')}")
                    print(f"[Claude ACP] 错误消息: {error_info.get('message', 'Unknown')}")
            
            except json.JSONDecodeError as e:
                print(f"[Claude ACP] 会话响应JSON解析错误: {e}")
                print(f"[Claude ACP] 原始响应: {response_line}")
        
        print("[Claude ACP] 🎯 Claude ACP连接测试完成")
        
    except Exception as e:
        print(f"[Claude ACP] ❌ 连接错误: {e}")
        print(f"[Claude ACP] 错误类型: {type(e)}")
        print(f"[Claude ACP] 错误详情: {str(e)}")
    
    finally:
        # 清理
        print("[Claude ACP] 🧹 清理Claude Agent进程...")
        if 'claude_process' in locals():
            claude_process.terminate()
            try:
                claude_process.wait(timeout=5)
                print("[Claude ACP] ✅ Claude Agent进程已停止")
            except subprocess.TimeoutExpired:
                print("[Claude ACP] ⚠️ 强制停止Claude Agent进程")
                claude_process.kill()

if __name__ == "__main__":
    asyncio.run(connect_to_claude_acp_encoding_fixed())
