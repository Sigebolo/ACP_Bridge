#!/usr/bin/env python3
"""
Test Bridge health and phone line status
"""

import requests
import json

def test_bridge_health():
    """Test Bridge server health"""
    try:
        response = requests.get("http://localhost:33333/health", timeout=3)
        if response.status_code == 200:
            health_data = response.json()
            print(f"Bridge Health: {health_data}")
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Health check error: {e}")
        return False

def test_phone_lines():
    """Test all phone lines"""
    endpoints = [
        ("/api/gemini/message", "Message Line"),
        ("/api/gemini/review", "Review Line"), 
        ("/api/gemini/suggestion", "Suggestion Line")
    ]
    
    results = {}
    for endpoint, name in endpoints:
        try:
            # Test with a simple ping message
            test_data = {
                "type": "test",
                "content": f"Testing {name}",
                "priority": "low"
            }
            
            response = requests.post(f"http://localhost:33333{endpoint}", 
                                    json=test_data, timeout=3)
            if response.status_code == 200:
                results[name] = "CONNECTED"
            else:
                results[name] = f"ERROR: {response.status_code}"
        except Exception as e:
            results[name] = f"FAILED: {str(e)}"
    
    return results

if __name__ == "__main__":
    print("=== Windsurf Phone Line Status Check ===\n")
    
    # Test bridge health
    print("1. Bridge Server Health:")
    health_ok = test_bridge_health()
    print(f"   Status: {'HEALTHY' if health_ok else 'UNHEALTHY'}\n")
    
    # Test phone lines
    print("2. Phone Line Status:")
    lines = test_phone_lines()
    for name, status in lines.items():
        print(f"   {name}: {status}")
    
    print(f"\n=== Summary ===")
    if health_ok and all("CONNECTED" in status for status in lines.values()):
        print("All phone lines are OPEN and READY for Gemini CLI calls!")
    else:
        print("Some phone lines need attention.")
