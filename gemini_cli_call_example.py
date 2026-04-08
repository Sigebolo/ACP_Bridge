#!/usr/bin/env python3
"""
Gemini CLI Call Example - How to "call" Windsurf via input hooks
"""

import requests
import json
import time

class GeminiPhone:
    """Telephone for Gemini CLI to call Windsurf"""
    
    def __init__(self, bridge_url="http://localhost:33333"):
        self.bridge_url = bridge_url
        
    def send_message(self, content, message_type="message", priority="normal", action_required=False):
        """Send a message to Windsurf"""
        try:
            response = requests.post(f"{self.bridge_url}/api/gemini/message", json={
                "type": message_type,
                "content": content,
                "priority": priority,
                "action_required": action_required
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"Message sent successfully: {result['message_id']}")
                return True
            else:
                print(f"Failed to send message: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def send_review(self, file_path, review_content, suggestions=None):
        """Send code review to Windsurf"""
        try:
            response = requests.post(f"{self.bridge_url}/api/gemini/review", json={
                "file": file_path,
                "review": review_content,
                "suggestions": suggestions or []
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"Review sent successfully: {result['review_id']}")
                return True
            else:
                print(f"Failed to send review: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending review: {e}")
            return False
    
    def send_suggestion(self, context, suggestion, confidence=0.8):
        """Send suggestion to Windsurf"""
        try:
            response = requests.post(f"{self.bridge_url}/api/gemini/suggestion", json={
                "context": context,
                "suggestion": suggestion,
                "confidence": confidence
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"Suggestion sent successfully: {result['suggestion_id']}")
                return True
            else:
                print(f"Failed to send suggestion: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending suggestion: {e}")
            return False

# Example usage
def demo_calls():
    """Demonstrate different types of calls"""
    phone = GeminiPhone()
    
    print("=== Gemini CLI Telephone Demo ===")
    
    # 1. Simple message
    phone.send_message(
        "Hey! I noticed you're working on the ACP Bridge system. Need any help with the hooks configuration?",
        message_type="general",
        priority="normal"
    )
    
    time.sleep(1)
    
    # 2. Code review
    phone.send_review(
        file_path="d:/Gemini/agent-hand/bridge/acp_hook_handler.py",
        review_content="The hook handler looks good overall. Consider adding more error handling for network timeouts.",
        suggestions=[
            "Add retry logic for failed requests",
            "Implement request queuing for high load",
            "Add logging for debugging purposes"
        ]
    )
    
    time.sleep(1)
    
    # 3. Suggestion
    phone.send_suggestion(
        context="ACP Bridge Architecture",
        suggestion="Consider implementing a message queue system for better reliability in high-throughput scenarios.",
        confidence=0.9
    )
    
    time.sleep(1)
    
    # 4. Action required message
    phone.send_message(
        "I found a potential security issue in the authentication logic. Please review the acp_config.json file.",
        message_type="security_alert",
        priority="high",
        action_required=True
    )
    
    print("\n=== All calls completed! ===")
    print("Check your Windsurf notifications for the messages.")

if __name__ == "__main__":
    demo_calls()
