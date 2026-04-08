#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
停止 ACP Bridge 后台服务
移除 ACP Bridge 依赖，切换到纯 CrewAI 方案
"""

import subprocess
import sys
import os
from datetime import datetime

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def find_acp_bridge_processes():
    """查找 ACP Bridge 相关进程"""
    processes = []
    
    try:
        # 查找 Python 进程中包含 acp_bridge_manager 的
        result = subprocess.run([
            'tasklist', '/fi', 'imagename eq python.exe', '/fo', 'csv'
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines[1:]:  # 跳过标题行
                if 'acp_bridge_manager' in line or 'acp_bridge' in line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        pid = parts[1].strip()
                        name = parts[0].strip()
                        processes.append({'pid': pid, 'name': name})
        
    except Exception as e:
        log(f"❌ 查找进程失败: {e}")
    
    return processes

def stop_process(pid, name):
    """停止指定进程"""
    try:
        log(f"🛑 停止进程: {name} (PID: {pid})")
        
        # 尝试优雅停止
        result = subprocess.run(['taskkill', '/PID', pid, '/T'], 
                           capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            log(f"✅ 进程 {name} 已停止")
            return True
        else:
            # 强制停止
            result = subprocess.run(['taskkill', '/PID', pid, '/F'], 
                               capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                log(f"⚠️ 强制停止进程 {name}")
                return True
            else:
                log(f"❌ 无法停止进程 {name}: {result.stderr}")
                return False
                
    except Exception as e:
        log(f"❌ 停止进程失败: {e}")
        return False

def stop_acp_bridge_services():
    """停止所有 ACP Bridge 相关服务"""
    log("🔍 查找 ACP Bridge 相关进程...")
    
    processes = find_acp_bridge_processes()
    
    if not processes:
        log("✅ 未发现运行中的 ACP Bridge 进程")
        return True
    
    log(f"📊 发现 {len(processes)} 个 ACP Bridge 进程")
    
    success_count = 0
    for proc in processes:
        if stop_process(proc['pid'], proc['name']):
            success_count += 1
    
    log(f"📊 成功停止 {success_count}/{len(processes)} 个进程")
    
    return success_count == len(processes)

def cleanup_acp_bridge_files():
    """清理 ACP Bridge 相关文件"""
    log("🧹 清理 ACP Bridge 相关文件...")
    
    files_to_cleanup = [
        "d:/Gemini/agent-hand/bridge/acp_bridge_manager.py",
        "d:/Gemini/agent-hand/bridge/acp_agents_config.json",
        "d:/Gemini/agent-hand/bridge/crewai.yaml",
        "d:/Gemini/agent-hand/bridge/crewai-run-script.py",
        "d:/Gemini/agent-hand/bridge/test_acp_bridge_crewai.py"
    ]
    
    cleaned_count = 0
    for file_path in files_to_cleanup:
        if os.path.exists(file_path):
            try:
                # 重命名为备份文件，而不是删除
                backup_path = file_path + ".backup"
                os.rename(file_path, backup_path)
                log(f"✅ 已备份: {file_path} -> {backup_path}")
                cleaned_count += 1
            except Exception as e:
                log(f"❌ 备份失败: {file_path} - {e}")
    
    log(f"📊 清理完成: {cleaned_count} 个文件已备份")
    return cleaned_count > 0

def main():
    """主函数"""
    print("🛑 ACP Bridge 清理工具")
    print("=" * 50)
    print("📋 功能:")
    print("  - 🛑 停止 ACP Bridge 后台服务")
    print("  - 🧹 清理 ACP Bridge 相关文件")
    print("  - 🚀 准备切换到纯 CrewAI 方案")
    print("=" * 50)
    
    # 停止服务
    services_stopped = stop_acp_bridge_services()
    
    # 清理文件
    files_cleaned = cleanup_acp_bridge_files()
    
    print("\n🎉 清理完成！")
    print("📋 结果:")
    print(f"  - 🛑 服务停止: {'✅ 成功' if services_stopped else '❌ 失败'}")
    print(f"  - 🧹 文件清理: {'✅ 成功' if files_cleaned else '❌ 失败'}")
    
    print("\n🚀 下一步:")
    print("  1. 运行: python d:/Gemini/agent-hand/bridge/crewai-pure-run.py")
    print("  2. 访问: http://localhost:8080")
    print("  3. 在 Windsurf 中开始开发")
    print("  4. 享受纯 CrewAI 多Agent协作！")

if __name__ == "__main__":
    main()
