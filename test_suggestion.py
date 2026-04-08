#!/usr/bin/env python3
"""
Test suggestion from Gemini CLI
"""

import requests
import json

def send_suggestion():
    """Send suggestion to test input hooks"""
    url = "http://localhost:33333/api/gemini/suggestion"
    
    suggestion_data = {
        "context": "ACP Bridge Performance",
        "suggestion": "Consider implementing Redis caching for frequently accessed configuration data to reduce disk I/O and improve response times.",
        "confidence": 0.95
    }
    
    try:
        response = requests.post(url, json=suggestion_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Suggestion sent successfully: {result['suggestion_id']}")
            print("Check windsurf_notifications for the suggestion!")
        else:
            print(f"Failed to send suggestion: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error sending suggestion: {e}")

if __name__ == "__main__":
    send_suggestion()
