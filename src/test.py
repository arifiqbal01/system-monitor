import requests

response = requests.get("http://httpstat.us")
print(f"Response Status Code: {response.status_code}")