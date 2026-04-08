#!/usr/bin/env python3
"""
高级循环检测和自动推进系统
"""

import json
import os
import asyncio
from datetime import datetime, timedelta
import re

class SmartLoopDetector:
    """智能循环检测器"""
    
    def __init__(self):
        self.response_dir = "d:/Gemini/agent-hand/bridge/gemini_responses"
        self.state_file = "d:/Gemini/agent-hand/bridge/workflow_state.json"
        self.no_improvement_count = 0
        self.max_no_improvement_cycles = 3  # 连续3次无改进后自动推进
        
    def load_state(self):
        """加载工作流状态"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {
                "current_stage": "planning",
                "last_gemini_response": None,
                "no_improvement_count": 0,
                "auto_advance_count": 0
            }
        except Exception as e:
            print(f"[Smart Loop Detector] 加载状态失败: {e}")
            return {"current_stage": "planning", "no_improvement_count": 0}
    
    def save_state(self, state):
        """保存工作流状态"""
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Smart Loop Detector] 保存状态失败: {e}")
    
    def analyze_latest_response(self):
        """分析最新的Gemini响应"""
        try:
            if not os.path.exists(self.response_dir):
                return {"has_improvements": False, "analysis": "无响应文件"}
            
            # 获取最新的响应文件
            response_files = [f for f in os.listdir(self.response_dir) if f.endswith('.json')]
            response_files.sort(reverse=True)
            
            if not response_files:
                return {"has_improvements": False, "analysis": "无响应文件"}
            
            # 分析最新响应
            latest_file = response_files[0]
            with open(os.path.join(self.response_dir, latest_file), "r", encoding="utf-8") as f:
                response_data = json.load(f)
            
            # 检查是否有改进建议
            response_text = str(response_data.get("response", ""))
            return self.detect_improvements(response_text)
            
        except Exception as e:
            print(f"[Smart Loop Detector] 分析响应失败: {e}")
            return {"has_improvements": False, "analysis": f"分析错误: {e}"}
    
    def detect_improvements(self, response_text):
        """检测响应中的改进建议"""
        # 改进建议关键词
        improvement_patterns = [
            r'修改|改进|优化|调整|更新|增强|重构|fix|修复|补充|完善|提升',
            r'建议|推荐|应该|需要|必须|可以',
            r'通过|不通过|有问题|错误|缺陷',
            r'测试|验证|检查|确认|审核'
        ]
        
        # 检查是否有改进相关内容
        has_improvements = False
        matched_patterns = []
        
        for pattern in improvement_patterns:
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            if matches:
                has_improvements = True
                matched_patterns.extend([pattern])
        
        # 特殊检测：确认通过但无具体改进建议
        if "通过" in response_text and not has_improvements:
            has_improvements = True
            matched_patterns.append("通过但无改进建议")
        
        return {
            "has_improvements": has_improvements,
            "matched_patterns": matched_patterns,
            "improvement_count": len(matched_patterns),
            "response_length": len(response_text)
        }
    
    def should_auto_advance(self, current_state):
        """判断是否应该自动推进"""
        # 如果连续多次无改进建议，且当前不是最终阶段
        if self.no_improvement_count >= self.max_no_improvement_cycles:
            current_stage = current_state.get("current_stage", "")
            
            # 不在最终阶段时自动推进
            if current_stage not in ["testing", "deployment"]:
                return {
                    "should_advance": True,
                    "reason": f"连续{self.no_improvement_count}次无改进建议，自动推进到下一阶段",
                    "next_stage": self.get_next_stage(current_stage)
                }
        
        return {
            "should_advance": False,
            "reason": "等待新的改进建议"
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
    
    async def trigger_auto_advance(self, next_stage):
        """触发自动推进"""
        print(f"🚀 [Smart Loop Detector] 自动推进到阶段: {next_stage}")
        
        # 创建自动推进的触发文件
        advance_trigger_file = f"d:/Gemini/agent-hand/bridge/auto_advance_{next_stage}.json"
        
        try:
            with open(advance_trigger_file, "w", encoding="utf-8") as f:
                json.dump({
                    "action": "auto_advance",
                    "from_stage": self.load_state().get("current_stage"),
                    "to_stage": next_stage,
                    "timestamp": datetime.now().isoformat(),
                    "reason": "智能检测到连续无改进建议，自动推进"
                }, f, indent=2, ensure_ascii=False)
            
            print(f"📋 [Smart Loop Detector] 自动推进触发文件已创建: {advance_trigger_file}")
            
            # 重置计数器
            self.no_improvement_count = 0
            
            return True
            
        except Exception as e:
            print(f"[Smart Loop Detector] 创建自动推进文件失败: {e}")
            return False
    
    async def run_detection(self):
        """运行智能检测"""
        print("🧠 [Smart Loop Detector] 启动智能循环检测...")
        
        while True:
            try:
                # 分析最新响应
                analysis = self.analyze_latest_response()
                
                print(f"📊 [Smart Loop Detector] 分析结果:")
                print(f"  有改进建议: {analysis['has_improvements']}")
                print(f"  匹配模式: {analysis['matched_patterns']}")
                print(f"  无改进计数: {self.no_improvement_count}")
                
                # 更新状态
                current_state = self.load_state()
                
                if analysis["has_improvements"]:
                    # 有改进建议，重置计数器
                    self.no_improvement_count = 0
                    current_state["no_improvement_count"] = 0
                    current_state["last_action"] = "improvements_found"
                else:
                    # 无改进建议，增加计数器
                    self.no_improvement_count += 1
                    current_state["No_improvement_count"] = self.no_improvement_count
                    current_state["last_action"] = "no_improvements"
                
                self.save_state(current_state)
                
                # 检查是否应该自动推进
                auto_advance_decision = self.should_auto_advance(current_state)
                
                if auto_advance_decision["should_advance"]:
                    # 自动推进到下一阶段
                    success = await self.trigger_auto_advance(auto_advance_decision["next_stage"])
                    if success:
                        # 更新状态
                        current_state["current_stage"] = auto_advance_decision["next_stage"]
                        current_state["auto_advance_count"] = current_state.get("auto_advance_count", 0) + 1
                        current_state["last_action"] = "auto_advanced"
                        self.save_state(current_state)
                        
                        print(f"✅ [Smart Loop Detector] 自动推进成功，新阶段: {auto_advance_decision['next_stage']}")
                
                print("⏰ [Smart Loop Detector] 等待60秒后重新分析...")
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"❌ [Smart Loop Detector] 检测错误: {e}")
                await asyncio.sleep(60)

if __name__ == "__main__":
    detector = SmartLoopDetector()
    asyncio.run(detector.run_detection())
