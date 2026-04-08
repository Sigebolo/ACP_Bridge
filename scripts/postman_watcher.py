import os
import time
import re
import subprocess
import json
from datetime import datetime

# Paths
BRIDGE_WORKSPACE = r'D:\Gemini\agent-hand\bridge\workspace'
ANTIGRAVITY_TASKS = os.path.join(BRIDGE_WORKSPACE, 'antigravity_tasks')
COMM_FILE = r'D:\Gemini\agent-hand\openclaw-automation\Atom-Quant\ATOM_COMM.md'
SCRIPTS_DIR = r'D:\Gemini\agent-hand\bridge\scripts'

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [Postman] {msg}")

def ensure_dirs():
    os.makedirs(ANTIGRAVITY_TASKS, exist_ok=True)

def parse_comm_file():
    if not os.path.exists(COMM_FILE):
        return []
    
    with open(COMM_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to find tasks like [TASK-ID]
    tasks = re.findall(r'\[(TASK-[^\]]+)\] 状态：([^\n]+)\n目标：([^\n]+)', content)
    return tasks

def wake_antigravity(task_id, goal):
    log(f"Waking up Antigravity for task {task_id}...")
    
    # 1. Create task file
    task_file = os.path.join(ANTIGRAVITY_TASKS, f"{task_id}.md")
    with open(task_file, 'w', encoding='utf-8') as f:
        f.write(f"# Task: {task_id}\n\n## Goal\n{goal}\n\n## Status\nAssigned\n")
    
    # 2. Trigger wake-up script
    try:
        cmd = [
            'python', 
            os.path.join(SCRIPTS_DIR, 'trigger_antigravity.py'),
            f"收到新任务 {task_id}。请检查 workspace/antigravity_tasks 目录。目标：{goal}"
        ]
        subprocess.run(cmd, check=True)
        log(f"Trigger script executed for {task_id}")
    except Exception as e:
        log(f"Failed to trigger Antigravity: {e}")

def main():
    ensure_dirs()
    log("Postman watcher started. Polling ATOM_COMM.md every 30s...")
    
    processed_tasks = set()
    
    # Load previously processed tasks from last run if needed
    # For simplicity, we just look at files in ANTIGRAVITY_TASKS
    for f in os.listdir(ANTIGRAVITY_TASKS):
        if f.endswith('.md'):
            processed_tasks.add(f.replace('.md', ''))

    while True:
        try:
            tasks = parse_comm_file()
            for tid, status, goal in tasks:
                if tid not in processed_tasks and '进行中' in status:
                    log(f"Found new active task: {tid}")
                    wake_antigravity(tid, goal)
                    processed_tasks.add(tid)
            
            # Pulse
            pulse_file = os.path.join(ANTIGRAVITY_TASKS, 'last_pulse.txt')
            with open(pulse_file, 'w') as f:
                f.write(str(time.time()))
                
        except Exception as e:
            log(f"Error in main loop: {e}")
            
        time.sleep(30)

if __name__ == "__main__":
    main()
