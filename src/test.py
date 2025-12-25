import requests

response = requests.get("https://httpstat.us/500")
print(f"Response Status Code: {response.status_code}")