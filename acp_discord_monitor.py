#!/usr/bin/env python3
"""
ACP Discord-Style Monitor - 打造人类友好的 Agent 协作流
过滤噪音，只显示意图、动作和对话。
"""

import json
import os
import sys
import time
from datetime import datetime
from colorama import init, Fore, Style

# 初始化彩色输出
init(autoreset=True)

class DiscordMonitor:
    def __init__(self):
        self.log_file = "d:/Gemini/agent-hand/bridge/acp_communication_log.txt"
        self.last_pos = 0
        self.agent_name = f"{Fore.CYAN}[Gemini CLI]"
        self.windsurf_name = f"{Fore.MAGENTA}[Windsurf]"
        self.sys_name = f"{Fore.YELLOW}[System]"
        
    def parse_log_entry(self, entry_text):
        """解析原始日志条目并转化为人性化描述"""
        try:
            # 简单的正则或字符串切分来获取方向和内容
            if "方向: 📤 发送" in entry_text:
                content_start = entry_text.find("📄 内容:") + 7
                content_end = entry_text.rfind("="*80)
                content_json = entry_text[content_start:content_end].strip()
                data = json.loads(content_json)
                
                method = data.get("method", "")
                params = data.get("params", {})
                
                if method == "initialize":
                    return f"{self.sys_name} 🔌 正在建立 ACP 连接..."
                elif method == "session/new":
                    return f"{self.sys_name} 🏗️ 正在创建新任务会话..."
                elif method == "session/prompt":
                    prompt = params.get("prompt", [])
                    if prompt and isinstance(prompt, list):
                        text = prompt[0].get("text", "")
                        # 尝试识别 Windsurf 事件
                        if "Event:" in text or "write" in text.lower():
                            return f"{self.windsurf_name} 🚀 触发动作: {self._format_windsurf_action(text)}"
                        return f"{self.windsurf_name} 💬 说: {text}"
                    
            elif "方向: 📥 接收" in entry_text:
                content_start = entry_text.find("📄 内容:") + 7
                content_end = entry_text.rfind("="*80)
                content_json = entry_text[content_start:content_end].strip()
                data = json.loads(content_json)
                
                # 处理通知 (流式内容)
                if "method" in data and data["method"] == "session/update":
                    update = data.get("params", {}).get("update", {})
                    if update.get("sessionUpdate") == "agent_message_chunk":
                        chunk = update.get("content", {}).get("text", "")
                        return f"{self.agent_name} ✍️ {chunk}"
                    elif update.get("sessionUpdate") == "tool_call":
                        tool = update.get("title", "未知工具")
                        return f"{self.agent_name} 🛠️ 正在使用工具: {Fore.GREEN}{tool}"
                
                # 处理最终结果 (过滤噪音)
                if "result" in data and "full_content" in data["result"]:
                    return f"{self.agent_name} ✅ 回复完成。"
                    
        except Exception:
            return None # 无法解析的噪音，忽略
        return None

    def _format_windsurf_action(self, text):
        """格式化 Windsurf 的动作描述"""
        if "write" in text.lower():
            # 尝试提取文件名
            import re
            match = re.search(r"file:?\s*([^\s,]+)", text.lower())
            filename = match.group(1) if match else "某个文件"
            return f"📝 正在修改 {Fore.WHITE}{filename}"
        elif "cmd" in text.lower() or "command" in text.lower():
            return "💻 正在执行终端命令"
        return "执行了某个操作"

    def run(self):
        print(f"\n{Style.BRIGHT}{Fore.BLUE}{'='*30} Agent 协作频道 (Discord 风格) {'='*30}\n")
        print(f"{self.sys_name} 正在监控协作流水线...\n")
        
        # 先显示最近的记录
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                content = f.read()
                entries = content.split("="*80 + "\n\n")
                for entry in entries[-10:]: # 只显示最后10条
                    parsed = self.parse_log_entry(entry)
                    if parsed:
                        print(parsed)
                self.last_pos = f.tell()

        # 实时监控
        try:
            while True:
                if not os.path.exists(self.log_file):
                    time.sleep(1)
                    continue
                    
                with open(self.log_file, "r", encoding="utf-8") as f:
                    f.seek(self.last_pos)
                    new_content = f.read()
                    if new_content:
                        entries = new_content.split("="*80 + "\n\n")
                        for entry in entries:
                            parsed = self.parse_log_entry(entry)
                            if parsed:
                                # 处理流式输出不换行的情况（可选）
                                if "✍️" in parsed:
                                    print(parsed.replace(f"{self.agent_name} ✍️ ", ""), end="", flush=True)
                                else:
                                    print(f"\n{parsed}")
                        self.last_pos = f.tell()
                time.sleep(0.5)
        except KeyboardInterrupt:
            print(f"\n\n{self.sys_name} 监控已停止。")

if __name__ == "__main__":
    monitor = DiscordMonitor()
    monitor.run()
