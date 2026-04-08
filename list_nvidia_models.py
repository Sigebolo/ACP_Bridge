import requests

def list_nvidia_models():
    url = "https://integrate.api.nvidia.com/v1/models"
    headers = {
        "Authorization": "Bearer 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"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            models = response.json().get('data', [])
            for model in models:
                print(f"Model ID: {model.get('id')}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    list_nvidia_models()
