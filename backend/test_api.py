import requests
import json

url = "http://localhost:5000/api/evaluate"
payload = {"github_url": "https://github.com/octocat/Spoon-Knife"}
headers = {"Content-Type": "application/json"}

try:
    print("Testing API with Spoon-Knife...")
    response = requests.post(url, json=payload, headers=headers, timeout=300)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)[:500]}...")
except Exception as e:
    print(f"Request failed: {e}")
