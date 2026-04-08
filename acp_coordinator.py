import subprocess
import os
import json

from datetime import datetime

class ACPCoordinator:
    def __init__(self):
        self.bridge_manager_path = "D:\\Gemini\\agent-hand\\bridge\\acp_bridge_manager.py"
        self.vault_base = "D:\\Gemini\\Dingning_Obsidian_Vault\\80_crew AI project folder\\多Agent协同工作SOP"

    def send_to_agent(self, agent_name, message):
        print(f"📡 Sending to {agent_name}: {message}")
        # Call the existing bridge manager
        cmd = ["python", self.bridge_manager_path, "--agent", agent_name, "--message", message]
        subprocess.run(cmd, capture_output=True, text=True)

    def update_obsidian_log(self, task_name, status):
        log_path = os.path.join(self.vault_base, "04_Worklog", f"{task_name}.md")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"# Worklog: {task_name}\nStatus: {status}\nTime: {datetime.now()}")

if __name__ == "__main__":
    coordinator = ACPCoordinator()
    print("🤖 ACP Coordinator Active")
    coordinator.send_to_agent("Windsurf", "Please acknowledge initialization of the new SOP workspace.")
    coordinator.update_obsidian_log("Initialization", "Sent signal to Windsurf agent.")
