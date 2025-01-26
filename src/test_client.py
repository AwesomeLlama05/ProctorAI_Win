import requests
import os
from PIL import Image
import io

def test_api():
    print("Testing ProctorAI API...")
    
    # Take a screenshot (for testing purposes, we'll create a simple image)
    img = Image.new('RGB', (800, 600), color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Test /analyze endpoint
    print("\nTesting /analyze endpoint...")
    files = {
        'screenshot': ('test.png', img_byte_arr, 'image/png'),
    }
    data = {
        'prompt': 'I should be working on coding',
        'model_name': 'claude-3-5-sonnet-20240620',
        'two_tier': 'false',
        'router_model_name': 'llava'
    }
    
    try:
        response = requests.post('http://127.0.0.1:8000/analyze', files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test /handle-procrastination endpoint
    print("\nTesting /handle-procrastination endpoint...")
    data = {
        'user_spec': 'I should be working on coding',
        'user_name': 'Tester',
        'model_name': 'claude-3-5-sonnet-20240620',
        'tts': 'false',
        'voice': 'Patrick',
        'countdown_time': '15'
    }
    
    try:
        response = requests.post('http://127.0.0.1:8000/handle-procrastination', data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_api()
