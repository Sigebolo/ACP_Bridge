import subprocess
import sys

# 模拟 Windsurf 的钩子调用
def simulate_windsurf_hook():
    script = "d:/Gemini/agent-hand/bridge/acp_hook_handler.py"
    cmd = ["python", script, "--event", "test", "--message", "Handshake from Windsurf simulator"]
    
    print("🚀 模拟 Windsurf 发送钩子信号...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"📡 桥接返回: {result.stdout}")
        if result.stderr:
            print(f"❌ 错误: {result.stderr}")
    except Exception as e:
        print(f"💥 无法触发钩子: {e}")

if __name__ == "__main__":
    simulate_windsurf_hook()
