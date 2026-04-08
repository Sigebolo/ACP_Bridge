#!/usr/bin/env python3
"""
Test code review from Gemini CLI
"""

import requests
import json

def send_code_review():
    """Send code review to test input hooks"""
    url = "http://localhost:33333/api/gemini/review"
    
    review_data = {
        "file": "d:/Gemini/agent-hand/bridge/src/server.js",
        "review": "I've analyzed your server.js file and found several areas for improvement:\n\n1. **Security**: The handleGeminiMessage function doesn't validate input properly\n2. **Performance**: Consider adding request rate limiting\n3. **Error Handling**: Some error responses lack proper logging\n\nOverall the structure is good, but these improvements would make it more robust.",
        "suggestions": [
            "Add input validation middleware",
            "Implement rate limiting with express-rate-limit",
            "Add structured logging with winston",
            "Consider adding request timeouts"
        ]
    }
    
    try:
        response = requests.post(url, json=review_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Code review sent successfully: {result['review_id']}")
            print("Check windsurf_notifications for the review!")
        else:
            print(f"Failed to send code review: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error sending code review: {e}")

if __name__ == "__main__":
    send_code_review()
