import requests
import json

def test_nvidia_nim():
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "nvidia/llama-3.1-nemotron-70b-instruct",
        "messages": [{"role": "user", "content": "Hello, verify model connectivity."}],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_nvidia_nim()
