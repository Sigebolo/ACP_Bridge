#!/usr/bin/env python3
"""
验证ACP Bridge状态脚本
"""

import subprocess
import json
import time
import os

def check_bridge_status():
    """检查ACP Bridge Manager状态"""
    
    print("🔍 ACP Bridge状态检查")
    print("=" * 50)
    
    # 1. 检查必要文件
    required_files = [
        "d:/Gemini/agent-hand/bridge/acp_bridge_manager.py",
        "d:/Gemini/agent-hand/bridge/acp_hook_handler.py", 
        "d:/Gemini/agent-hand/bridge/acp_agents_config.json"
    ]
    
    print("📁 检查必要文件:")
    for file_path in required_files:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
    
    # 2. 检查配置文件
    print("\n⚙️ 检查配置文件:")
    try:
        with open("d:/Gemini/agent-hand/bridge/acp_agents_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            agents = config.get("agents", [])
            print(f"  ✅ 找到 {len(agents)} 个代理配置:")
            for agent in agents:
                print(f"    - {agent.get('name', 'Unknown')}")
    except Exception as e:
        print(f"  ❌ 配置文件读取失败: {e}")
    
    # 3. 检查Gemini CLI
    print("\n🤖 检查Gemini CLI:")
    try:
        result = subprocess.run(
            ["npx", "@google/gemini-cli", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"  ✅ Gemini CLI可用: {result.stdout.strip()}")
        else:
            print("  ❌ Gemini CLI不可用")
    except Exception as e:
        print(f"  ❌ Gemini CLI检查失败: {e}")
    
    # 4. 检查Windsurf配置
    print("\n🌊 检查Windsurf配置:")
    settings_file = "c:/Users/Administrator/AppData/Roaming/Windsurf/User/settings.json"
    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)
            hooks = settings.get("cascade.hooks", {})
            if hooks:
                print("  ✅ 找到Cascade Hooks配置:")
                for hook_name, hook_config in hooks.items():
                    print(f"    - {hook_name}")
            else:
                print("  ❌ 未找到Cascade Hooks配置")
    except Exception as e:
        print(f"  ❌ Windsurf配置读取失败: {e}")
    
    # 5. 建议的Windsurf配置
    print("\n💡 建议的Windsurf配置:")
    print("请将以下内容添加到Windsurf的settings.json中:")
    print("""
{
    "windsurf.cascade.hooks": {
        "onWrite": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event write --file ${file} --diff ${diff}",
        "onCommand": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event cmd --command ${command} --output ${output}",
        "onResponse": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event response --reasoning ${reasoning}"
    }
}
""")
    
    print("\n🎯 状态检查完成!")
    print("如果所有检查都通过，可以开始测试ACP通讯。")

if __name__ == "__main__":
    check_bridge_status()
