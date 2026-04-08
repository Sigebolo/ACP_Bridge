#!/usr/bin/env python3
"""
ACP Diagnostic Tool - Self-healing for Agent connections
"""
import json
import subprocess
import os

def diagnose_acp():
    print("[ACP Diag] Checking ACP Bridge status...")
    
    # Check config files
    config_files = [
        "d:/Gemini/agent-hand/bridge/acp_agents_config.json",
        "d:/Gemini/agent-hand/bridge/config/hooks.json"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"[ACP Diag] OK: {config_file}")
        else:
            print(f"[ACP Diag] MISSING: {config_file}")
            return False
    
    # Check directories
    directories = [
        "d:/Gemini/agent-hand/bridge/logs",
        "d:/Gemini/agent-hand/bridge/windsurf_notifications",
        "d:/Gemini/agent-hand/bridge/gemini_responses"
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"[ACP Diag] OK: {directory}")
        else:
            print(f"[ACP Diag] MISSING: {directory}")
            return False
    
    # Test Gemini CLI
    try:
        result = subprocess.run(["npx", "@google/gemini-cli", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("[ACP Diag] OK: Gemini CLI available")
            print(f"[ACP Diag] Version: {result.stdout.strip()}")
        else:
            print("[ACP Diag] ERROR: Gemini CLI not working")
            return False
    except Exception as e:
        print(f"[ACP Diag] ERROR: {e}")
        return False
    
    print("[ACP Diag] All systems ready!")
    return True

if __name__ == "__main__":
    diagnose_acp()
