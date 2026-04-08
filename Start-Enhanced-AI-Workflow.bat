@echo off
chcp 65001 >nul
title ACP Bridge - 智能AI辅助开发系统
echo ========================================
echo    启动完整的智能AI辅助开发系统
echo    包含: ACP Bridge, 智能循环检测, 自动推进机制
echo ========================================
echo.

echo [1/4] 启动工作流智能检测器...
start "Smart Loop Detector" /min cmd /c "python smart_loop_detector.py"

echo [2/4] 启动ACP通讯监控器...
start "ACP Monitor" /min cmd /c "python acp_communication_monitor.py"

echo [3/4] 启动基础ACP Bridge Manager...
start "ACP Bridge" /min cmd /c "python acp_bridge_manager.py"

echo.
echo ========================================
echo    系统组件启动完成！
echo.
echo    智能循环检测器: 自动检测停滞并推进
echo    ACP通讯监控器: 实时监控Gemini CLI通讯
echo    ACP Bridge Manager: 处理Windsorf事件和AI代理通信
echo.
echo    现在可以在Windsorf中开始项目开发！
echo    系统将自动:
echo      - 检测Gemini CLI响应中的改进建议
echo      - 识别工作流停滞
echo      - 自动推进到下一阶段
echo      - 防止无限循环
echo.
echo ========================================
echo.
echo 按任意键查看系统状态...
echo    - 智能检测器状态: workflow_state.json
echo    - Gemini CLI响应: gemini_responses/
echo    - 通讯日志: acp_communication_log.txt
echo    - 自动推进记录: auto_advance_*.json
echo ========================================
pause
