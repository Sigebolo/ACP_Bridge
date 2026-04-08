#!/usr/bin/env python3
"""
增强版ACP Hook Handler - 支持完整AI辅助开发工作流
"""

import asyncio
import json
import sys
import argparse
from datetime import datetime
import os

# 导入ACP Bridge管理器
sys.path.append("d:/Gemini/agent-hand/bridge")
from acp_bridge_manager import acp_bridge

async def handle_enhanced_hook_event():
    """处理增强版Hook事件 - 支持完整AI开发工作流"""
    
    parser = argparse.ArgumentParser(description="Enhanced ACP Hook Handler")
    parser.add_argument("--event", required=True, help="事件类型")
    parser.add_argument("--file", help="文件路径")
    parser.add_argument("--content", help="文件内容")
    parser.add_argument("--diff", help="代码差异")
    parser.add_argument("--command", help="执行的命令")
    parser.add_argument("--output", help="命令输出")
    parser.add_argument("--tool", help="MCP工具名称")
    parser.add_argument("--result", help="MCP工具结果")
    parser.add_argument("--reasoning", help="代理推理")
    parser.add_argument("--stage", help="开发阶段")
    
    args = parser.parse_args()
    
    # 构建增强事件数据
    event_data = {
        "file": args.file,
        "content": args.content,
        "diff": args.diff,
        "command": args.command,
        "output": args.output,
        "tool": args.tool,
        "result": args.result,
        "reasoning": args.reasoning,
        "stage": args.stage,
        "timestamp": datetime.now().isoformat(),
        "project_context": get_project_context()
    }
    
    print(f"[Enhanced ACP Hook] 收到事件: {args.event}")
    
    try:
        # 根据事件类型进行特殊处理
        if args.event in ["write", "read", "cmd"]:
            await handle_development_event(args.event, event_data)
        elif args.event == "review_request":
            await handle_review_request(event_data)
        elif args.event == "code_review":
            await handle_code_review(event_data)
        elif args.event == "test_plan":
            await handle_test_plan(event_data)
        else:
            await handle_general_event(args.event, event_data)
            
    except Exception as e:
        print(f"[Enhanced ACP Hook] 事件处理失败: {e}")

async def handle_development_event(event_type: str, event_data: dict):
    """处理开发阶段事件"""
    
    # 获取项目上下文
    project_context = event_data.get("project_context", {})
    
    # 根据事件类型构建不同的Gemini CLI任务
    if event_type == "write" or event_type == "read":
        # 文件操作 - 要求Gemini CLI审核implement计划
        task_message = f"""
# AI辅助开发 - 计划审核请求

## 项目上下文
{json.dumps(project_context, indent=2, ensure_ascii=False)}

## 最近变更
- 事件类型: {event_type}
- 文件: {event_data.get('file', 'N/A')}
- 变更内容: {event_data.get('diff', 'N/A')}

## 任务要求
请审核当前的项目状态和变更内容，并提供以下反馈：

### 1. 实施计划评估
- 当前实施方向是否合理？
- 需要哪些调整或优化？
- 优先级建议

### 2. 技术建议
- 架构设计建议
- 最佳实践建议
- 潜在风险评估

### 3. 下一步行动
- 具体的实施步骤
- 测试建议
- 质量保证措施

请提供详细的审核意见，我们将根据你的反馈进行调整。
"""
        
    elif event_type == "cmd":
        # 命令执行 - 要求Gemini CLI提供技术建议
        task_message = f"""
# AI辅助开发 - 技术咨询

## 执行的命令
{event_data.get('command', 'N/A')}

## 输出结果
{event_data.get('output', 'N/A')}

## 咨询内容
请分析这个命令的执行结果，并提供：

### 1. 结果分析
- 命令是否成功执行？
- 结果是否符合预期？
- 存在什么问题或改进空间？

### 2. 技术建议
- 优化建议
- 替代方案
- 最佳实践推荐

### 3. 后续行动
- 推荐的下一步操作
- 需要注意的事项

请基于当前项目状态提供专业的技术指导。
"""
    
    # 发送任务给Gemini CLI
    await send_to_gemini_cli(task_message, event_type)

async def handle_review_request(event_data: dict):
    """处理审核请求"""
    print("[Enhanced ACP Hook] 处理审核请求...")
    
    # 构建审核任务
    task_message = f"""
# 代码审核请求

## 审核内容
{event_data.get('content', 'N/A')}

## 项目状态
{json.dumps(event_data.get('project_context', {}), indent=2, ensure_ascii=False)}

## 审核要求
请提供详细的代码审核，包括：

### 1. 代码质量评估
- 代码结构和组织
- 命名规范和可读性
- 错误处理和边界情况
- 性能考虑

### 2. 功能正确性
- 逻辑实现是否正确
- 边界条件处理
- 与需求的一致性

### 3. 最佳实践
- 代码复用性
- 安全性考虑
- 可维护性

### 4. 改进建议
- 具体的修改方案
- 优化建议
- 重构建议

请提供审核结果和具体的修改指导。
"""
    
    await send_to_gemini_cli(task_message, "code_review")

async def handle_code_review(event_data: dict):
    """处理代码审核"""
    print("[Enhanced ACP Hook] 处理代码审核...")
    
    task_message = f"""
# 开发阶段审核 - 代码质量检查

## 审核结果
{event_data.get('result', 'N/A')}

## 项目进展评估
基于当前代码质量，请评估：

### 1. 质量评分
- 代码质量: 1-10分
- 功能完整性: 1-10分
- 测试覆盖度: 1-10分

### 2. 通过/不通过判断
- 是否通过当前的审核标准？
- 如果不通过，需要哪些改进？
- 下一轮审核的预期时间

### 3. 后续计划
- 优先修复项
- 测试计划调整
- 发布准备状态

请提供明确的审核结论和后续行动计划。
"""
    
    await send_to_gemini_cli(task_message, "test_plan")

async def handle_test_plan(event_data: dict):
    """处理测试计划"""
    print("[Enhanced ACP Hook] 处理测试计划...")
    
    task_message = f"""
# 测试计划审核

## 当前测试状态
{event_data.get('content', 'N/A')}

## 测试计划评估
请审核以下测试计划：

### 1. 测试覆盖度
- 功能测试覆盖
- 边界条件测试
- 性能测试计划
- 集成测试考虑

### 2. 测试方法
- 单元测试策略
- 集成测试方法
- 用户验收测试

### 3. 风险评估
- 潜在风险点
- 缓解措施
- 回滚计划

### 4. 时间安排
- 测试阶段划分
- 里程碑设置
- 发布时间预估

请提供测试计划优化建议和确认。
"""
    
    await send_to_gemini_cli(task_message, "general")

async def handle_general_event(event_type: str, event_data: dict):
    """处理一般事件"""
    print(f"[Enhanced ACP Hook] 处理一般事件: {event_type}")
    
    # 构建通用消息
    message = f"事件类型: {event_type}\n数据: {json.dumps(event_data, ensure_ascii=False)}"
    
    await send_to_gemini_cli(message, "general")

async def send_to_gemini_cli(message: str, task_type: str):
    """发送消息给Gemini CLI"""
    try:
        # 获取默认代理
        session_id = await acp_bridge.get_or_create_session("Gemini CLI")
        if not session_id:
            print("[Enhanced ACP Hook] 无法创建Gemini CLI会话")
            return
        
        # 发送任务消息
        response = await acp_bridge.send_message(session_id, message)
        
        if response:
            print(f"[Enhanced ACP Hook] Gemini CLI {task_type}任务发送成功")
            
            # 保存响应到文件
            await save_gemini_response(response, task_type)
            
            # 如果是审核类任务，可能需要触发Windsorf显示
            if task_type in ["code_review", "test_plan"]:
                await notify_windsurf_response(response, task_type)
        else:
            print(f"[Enhanced ACP Hook] Gemini CLI {task_type}任务发送失败")
    
    except Exception as e:
        print(f"[Enhanced ACP Hook] 发送消息失败: {e}")

async def save_gemini_response(response: dict, task_type: str):
    """保存Gemini CLI响应到文件"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"d:/Gemini/agent-hand/bridge/gemini_responses/{task_type}_{timestamp}.json"
        
        os.makedirs("d:/Gemini/agent-hand/bridge/gemini_responses", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "task_type": task_type,
                "response": response,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        print(f"[Enhanced ACP Hook] 响应已保存到: {filename}")
        
    except Exception as e:
        print(f"[Enhanced ACP Hook] 保存响应失败: {e}")

async def notify_windsurf_response(response: dict, task_type: str):
    """通知Windsorf显示响应"""
    try:
        # 这里可以实现Windsorf的通知机制
        # 比如写入到特定文件或发送通知
        notification_file = f"d:/Gemini/agent-hand/bridge/windsurf_notifications/{task_type}_notification.json"
        
        os.makedirs("d:/Gemini/agent-hand/bridge/windsurf_notifications", exist_ok=True)
        
        with open(notification_file, "w", encoding="utf-8") as f:
            json.dump({
                "type": "gemini_response",
                "task_type": task_type,
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "display_in_windsurf": True
            }, f, indent=2, ensure_ascii=False)
        
        print(f"[Enhanced ACP Hook] Windsorf通知已创建: {notification_file}")
        
    except Exception as e:
        print(f"[Enhanced ACP Hook] 创建通知失败: {e}")

def get_project_context():
    """获取项目上下文"""
    try:
        # 扫描项目文件获取上下文
        context = {
            "project_root": "d:/Gemini/agent-hand/bridge",
            "acp_bridge_version": "1.0",
            "supported_agents": ["Gemini CLI", "Claude Agent ACP", "Custom ACP"],
            "recent_files": [],
            "active_features": ["ACP通讯", "Windsorf集成", "AI辅助开发"]
        }
        
        # 获取最近的文件
        bridge_dir = "d:/Gemini/agent-hand/bridge"
        if os.path.exists(bridge_dir):
            for item in os.listdir(bridge_dir):
                if item.endswith('.py') and item.startswith('test_'):
                    context["recent_files"].append(item)
        
        return context
        
    except Exception as e:
        print(f"[Enhanced ACP Hook] 获取项目上下文失败: {e}")
        return {}

if __name__ == "__main__":
    asyncio.run(handle_enhanced_hook_event())
