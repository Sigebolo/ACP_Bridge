#!/usr/bin/env python3
"""
最简单的Gemini CLI测试 - 确保能看到所有输出
"""

import subprocess
import json
import time

def test_gemini_simple():
    """最简单的Gemini CLI测试"""
    
    print("🚀 启动最简单的Gemini CLI测试...")
    
    # 启动Gemini CLI
    cmd = ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"]
    print(f"📡 执行命令: {' '.join(cmd)}")
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    print("✅ Gemini CLI进程已启动")
    
    try:
        # 1. 发送初始化
        init_msg = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientInfo": {"name": "Simple Test", "version": "1.0"},
                "capabilities": ["file_access"]
            }
        }
        
        print(f"📤 发送�: {json.dumps(init_msg)}")
        
        # 发送并立即刷新
        process.stdin.write(json.dumps(init_msg) + "\n")
        process.stdin.flush()
        print("✅ 初始化消息已发送")
        
        # 等待并读取响应
        print("⏰ 等待响应...")
        
        # 设置超时
        start_time = time.time()
        timeout = 10
        
        while time.time() - start_time < timeout:
            # 检查是否有输出
            if process.poll() is not None:
                print(f"🔚 进程已结束，返回码: {process.returncode}")
                break
            
            # 尝试读取一行
            try:
                line = process.stdout.readline()
                if line:
                    print(f"📥 收到响应: {line.strip()}")
                    try:
                        parsed = json.loads(line.strip())
                        print(f"✅ 解析成功: {parsed}")
                        return True
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON解析错误: {e}")
                        print(f"原始内容: {repr(line)}")
                else:
                    print("⏳ 暂无输出，继续等待...")
                    time.sleep(0.5)
            except Exception as e:
                print(f"❌ 读取错误: {e}")
                break
        
        # 检查错误输出
        if process.stderr:
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"🚨 错误输出: {stderr_output}")
        
        print(f"⏰ {timeout}秒超时")
        return False
        
    except Exception as e:
        print(f"❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        print("🧹 清理进程...")
        process.terminate()
        try:
            process.wait(timeout=3)
            print("✅ 进程已停止")
        except subprocess.TimeoutExpired:
            print("⚠️ 强制杀死进程")
            process.kill()

if __name__ == "__main__":
    print("🎯 最简单的Gemini CLI通讯测试")
    print("=" * 50)
    success = test_gemini_simple()
    print("=" * 50)
    if success:
        print("🎉 测试成功!")
    else:
        print("❌ 测试失败!")
