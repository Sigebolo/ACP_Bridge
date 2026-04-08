#!/usr/bin/env python3
"""
智能循环检测和自动推进机制
"""

import json
import os
import asyncio
from datetime import datetime, timedelta

class WorkflowIntelligence:
    """工作流智能管理器"""
    
    def __init__(self):
        self.response_dir = "d:/Gemini/agent-hand/bridge/gemini_responses"
        self.notification_dir = "d:/Gemini/agent-hand/bridge/windsurf_notifications"
        self.state_file = "d:/Gemini/agent-hand/bridge/workflow_state.json"
        
    def load_workflow_state(self):
        """加载工作流状态"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {
                "current_stage": "planning",
                "last_gemini_suggestion": None,
                "loop_count": 0,
                "stagnation_count": 0,
                "last_action": None
            }
        except Exception as e:
            print(f"[Workflow Intelligence] 加载状态失败: {e}")
            return {"current_stage": "planning", "loop_count": 0}
    
    def save_workflow_state(self, state):
        """保存工作流状态"""
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Workflow Intelligence] 保存状态失败: {e}")
    
    def analyze_gemini_responses(self):
        """分析Gemini最近的响应"""
        try:
            if not os.path.exists(self.response_dir):
                return {"has_new_suggestions": False, "analysis": "无响应文件"}
            
            # 获取最近的响应文件
            response_files = [f for f in os.listdir(self.response_dir) if f.endswith('.json')]
            response_files.sort(reverse=True)  # 最新的在前
            
            if not response_files:
                return {"has_new_suggestions": False, "analysis": "无响应文件"}
            
            # 分析最近的3个响应
            recent_responses = []
            for file in response_files[:3]:
                try:
                    with open(os.path.join(self.response_dir, file), "r", encoding="utf-8") as f:
                        response_data = json.load(f)
                        recent_responses.append({
                            "file": file,
                            "timestamp": response_data.get("timestamp"),
                            "task_type": response_data.get("task_type"),
                            "response": response_data.get("response")
                        })
                except Exception as e:
                    print(f"[Workflow Intelligence] 分析响应文件失败 {file}: {e}")
            
            if not recent_responses:
                return {"has_new_suggestions": False, "analysis": "无法分析响应"}
            
            # 检查是否有新的改进建议
            latest_response = recent_responses[0]
            current_state = self.load_workflow_state()
            last_suggestion = current_state.get("last_gemini_suggestion")
            
            has_new_suggestions = False
            improvement_suggestions = []
            
            # 分析响应内容寻找改进建议
            if latest_response["task_type"] in ["code_review", "test_plan"]:
                response_text = str(latest_response["response"])
                
                # 寻找改进建议的关键词
                improvement_keywords = [
                    "修改", "改进", "优化", "建议", "调整", "更新", "增强",
                    "重构", "fix", "修复", "补充", "完善", "提升"
                ]
                
                for keyword in improvement_keywords:
                    if keyword in response_text:
                        has_new_suggestions = True
                        improvement_suggestions.append(keyword)
                
                # 检查是否有具体的技术建议
                if "通过" in response_text and "建议" in response_text:
                    has_new_suggestions = True
                    improvement_suggestions.append("需要修改")
                
                # 检查是否有测试相关建议
                if "测试" in response_text and "建议" in response_text:
                    has_new_suggestions = True
                    improvement_suggestions.append("需要测试")
            
            analysis = {
                "latest_response_time": latest_response["timestamp"],
                "response_type": latest_response["task_type"],
                "has_improvements": has_new_suggestions,
                "improvement_keywords": improvement_suggestions,
                "stagnation_detected": self.detect_stagnation(recent_responses),
                "recommendation": self.generate_recommendation(has_new_suggestions, current_state)
            }
            
            return {
                "has_new_suggestions": has_new_suggestions,
                "analysis": analysis
            }
            
        except Exception as e:
            print(f"[Workflow Intelligence] 分析响应失败: {e}")
            return {"has_new_suggestions": False, "analysis": f"分析错误: {e}"}
    
    def detect_stagnation(self, recent_responses):
        """检测工作流停滞"""
        if len(recent_responses) < 2:
            return False
        
        # 检查响应时间间隔
        times = [datetime.fromisoformat(r["timestamp"]) for r in recent_responses]
        if len(times) < 2:
            return False
            
        # 计算平均间隔
        intervals = []
        for i in range(1, len(times)):
            interval = (times[i] - times[i-1]).total_seconds()
            intervals.append(interval)
        
        avg_interval = sum(intervals) / len(intervals)
        
        # 如果间隔超过2小时，认为停滞
        return avg_interval > 7200  # 2小时
    
    def generate_recommendation(self, has_new_suggestions, current_state):
        """生成工作流建议"""
        if not has_new_suggestions:
            return {
                "action": "auto_advance",
                "message": "Gemini CLI无新的改进建议，自动推进到下一阶段",
                "next_stage": self.get_next_stage(current_state.get("current_stage")),
                "reason": "避免无限循环，继续项目进展"
            }
        else:
            return {
                "action": "continue_review",
                "message": "Gemini CLI有新的改进建议，继续当前阶段的审核",
                "next_stage": current_state.get("current_stage"),
                "reason": "基于新的反馈进行优化"
            }
    
    def get_next_stage(self, current_stage):
        """获取下一个阶段"""
        stage_flow = {
            "planning": "development",
            "development": "code_review", 
            "code_review": "test_plan",
            "test_plan": "testing",
            "testing": "deployment"
        }
        return stage_flow.get(current_stage, "deployment")
    
    def update_state(self, updates):
        """更新工作流状态"""
        current_state = self.load_workflow_state()
        current_state.update(updates)
        current_state["last_updated"] = datetime.now().isoformat()
        self.save_workflow_state(current_state)
        
        print(f"[Workflow Intelligence] 状态更新: {updates}")

async def run_workflow_intelligence():
    """运行工作流智能分析"""
    
    print("🧠 启动工作流智能分析...")
    
    intelligence = WorkflowIntelligence()
    
    while True:
        try:
            # 分析Gemini响应
            analysis = intelligence.analyze_gemini_responses()
            
            print(f"📊 分析结果:")
            print(f"  新建议: {analysis['has_new_suggestions']}")
            print(f"  停滞检测: {analysis['analysis'].get('stagnation_detected', False)}")
            
            # 生成建议
            if analysis["has_new_suggestions"]:
                recommendation = analysis["analysis"]["recommendation"]
                print(f"💡 建议: {recommendation['message']}")
                print(f"🎯 下一阶段: {recommendation['next_stage']}")
                
                # 更新状态
                intelligence.update_state({
                    "last_gemini_suggestion": str(analysis["analysis"]),
                    "loop_count": intelligence.load_workflow_state().get("loop_count", 0) + 1,
                    "last_action": recommendation["action"]
                })
                
                # 如果是自动推进，可以触发相应的Hook
                if recommendation["action"] == "auto_advance":
                    await trigger_auto_advance(recommendation["next_stage"])
            
            # 等待30秒后重新分析
            print("⏰ 等待30秒后重新分析...")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ 工作流智能分析错误: {e}")
            await asyncio.sleep(60)

async def trigger_auto_advance(next_stage):
    """触发自动推进到下一阶段"""
    print(f"🚀 自动推进到阶段: {next_stage}")
    
    # 这里可以实现自动触发下一阶段的Hook
    # 比如创建特定文件或发送特定命令
    # 具体实现可以根据需要添加
    
    stage_actions = {
        "development": "create_dev_plan_file",
        "code_review": "create_test_plan_file", 
        "test_plan": "run_tests",
        "testing": "prepare_deployment"
    }
    
    action = stage_actions.get(next_stage, "monitor_current")
    print(f"📋 执行行动: {action}")

if __name__ == "__main__":
    asyncio.run(run_workflow_intelligence())
