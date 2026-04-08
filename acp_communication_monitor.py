import time
import os
import sys
import threading
from datetime import datetime

# Path to the shared task directory
TASKS_DIR = r"D:\Gemini\Dingning_Obsidian_Vault\80_crew AI project folder\多Agent协同工作SOP\03_Tasks"

def get_agent_status():
    """Simple status check based on files in the Tasks directory"""
    if not os.path.exists(TASKS_DIR):
        return "Directory not found"
    
    tasks = [f for f in os.listdir(TASKS_DIR) if f.endswith('.md')]
    if not tasks:
        return "IDLE (No active tasks)"
    
    # Read the most recent task status (simplistic)
    latest_task = sorted(tasks)[-1]
    with open(os.path.join(TASKS_DIR, latest_task), 'r', encoding='utf-8') as f:
        content = f.read()
        if "ACTIVE_INIT" in content: return "ACTIVE (Initializing)"
        if "IN_PROGRESS" in content: return "ACTIVE (Working)"
        if "COMPLETED" in content: return "READY"
    return "UNKNOWN"

def display_dashboard():
    """Main dashboard loop"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*60)
        print("🤖 多Agent协同工作看板 (Native ACP Monitor)")
        print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Mock status for bridge components
        print(f"📞 ACP Bridge: [ONLINE] (Port 33334)")
        print(f"🛰️ Windsurf Agent: {get_agent_status()}")
        print(f"⚖️ Claude Reviewer: STANDBY")
        print(f"🧠 Lead Planner: READY")
        
        print("="*60)
        print("📝 最新任务进度:")
        if os.path.exists(TASKS_DIR):
            for task in os.listdir(TASKS_DIR):
                print(f"  - {task}")
        
        print("\n[Ctrl+C 退出]")
        time.sleep(2)

if __name__ == "__main__":
    try:
        display_dashboard()
    except KeyboardInterrupt:
        print("\nExiting dashboard...")
        sys.exit(0)
