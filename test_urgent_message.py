#!/usr/bin/env python3
"""
Test urgent message from Gemini CLI
"""

import requests
import json

def send_urgent_message():
    """Send urgent message to test input hooks"""
    url = "http://localhost:33333/api/gemini/message"
    
    message_data = {
        "type": "urgent_alert",
        "content": "Claude, I found a critical bug in your ACP configuration! The hooks.json file is missing the 'cascade_response' hook. This could cause communication failures.",
        "priority": "high",
        "action_required": True
    }
    
    try:
        response = requests.post(url, json=message_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Urgent message sent successfully: {result['message_id']}")
            print("Check windsurf_notifications for the alert!")
        else:
            print(f"Failed to send urgent message: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error sending urgent message: {e}")

if __name__ == "__main__":
    send_urgent_message()
