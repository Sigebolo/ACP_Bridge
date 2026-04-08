#!/usr/bin/env python3
"""
ACP Bridge Hook Handler - 处理Windsurf事件的轻量级处理器
"""

import asyncio
import json
import sys
import argparse
from datetime import datetime

# 导入ACP Bridge管理器
sys.path.append("d:/Gemini/agent-hand/bridge")
from acp_bridge_manager import acp_bridge

async def handle_hook_event():
    """处理Hook事件"""
    parser = argparse.ArgumentParser(description="ACP Bridge Hook Handler")
    parser.add_argument("--event", required=True, help="事件类型")
    parser.add_argument("--file", help="文件路径")
    parser.add_argument("--content", help="文件内容")
    parser.add_argument("--diff", help="代码差异")
    parser.add_argument("--command", help="执行的命令")
    parser.add_argument("--output", help="命令输出")
    parser.add_argument("--tool", help="MCP工具名称")
    parser.add_argument("--result", help="MCP工具结果")
    parser.add_argument("--reasoning", help="代理推理")
    
    args = parser.parse_args()
    
    # 构建事件数据
    event_data = {}
    
    if args.file:
        event_data["file"] = args.file
    if args.content:
        event_data["content"] = args.content
    if args.diff:
        event_data["diff"] = args.diff
    if args.command:
        event_data["command"] = args.command
    if args.output:
        event_data["output"] = args.output
    if args.tool:
        event_data["tool"] = args.tool
    if args.result:
        event_data["result"] = args.result
    if args.reasoning:
        event_data["reasoning"] = args.reasoning
    
    try:
        # 处理事件
        await acp_bridge.handle_windsurf_event(args.event, event_data)
        print(f"[ACP Hook] 事件 {args.event} 处理成功")
    except Exception as e:
        print(f"[ACP Hook] 事件 {args.event} 处理失败: {e}")

if __name__ == "__main__":
    asyncio.run(handle_hook_event())
