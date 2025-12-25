import json
import requests
import time
import datetime
import socket

config = "./config.json"

def website_analyzer():
  status = ("DOWN", "UP", "DEGRADED", "Unknown")
  website_status = "Unknown"
  response_time = None
  status_code = None
  
  with open(config, 'r') as readFile:
    config_data = json.load(readFile)
    
    interval = config_data.get("interval_minutes", 30)
    timeout = config_data.get("timeout_seconds", 5)
    websites = config_data.get("websites", [])
  
  schemes = ['http://', 'https://']
  for website in websites:
    start_time = datetime.datetime.now()
    
    if website.startswith('http://', 0) or website.startswith('https://', 0) and website.endswith('/', -1):
      website_domain = website.split('//')[1].split('/')[0]
    elif website.startswith('http://', 0) or website.startswith('https://', 0):
      website_domain = website.split('//')[1]
      if '/' in website_domain:
        website_domain = website_domain.split('/')[0]
    elif website.startswith('www.', 0) and website.endswith('/', -1):
      website_domain = website.split('www.')[1].split('/')[0]
    elif website.endswith('/', -1):
      website_domain = website[:-1]
    elif ':' in website:
      website_domain = website.split(':')[0]
    else:
      website_domain = website
    
    try:
      website_ip = socket.getaddrinfo(website_domain, None)
      if website_ip:
        web_url = schemes[1] + website if not website.startswith('http://', 0) and not website.startswith('https://', 0) else website
    except socket.gaierror as e:
      print(f"Hostname name or service not known {website_domain} - {e}")
      continue
    
    try:
      r = requests.get(web_url, timeout=timeout)
      response_time = r.elapsed.total_seconds() * 1000
      status_code = r.status_code if r.status_code else "N/A"
    
    except requests.exceptions.ConnectionError as e:
      print(f"Connection Refused Error {web_url} : - {e}")
    except requests.HTTPError as e:
      print(f"An HTTP error occurred. {web_url} : {r.status_code} - {e}")
    except requests.exceptions.Timeout as e:
      print(f"Request timed out {web_url} - {e}")
    except requests.exceptions.JSONDecodeError as e:
      print(f"Couldn’t decode the text into json {web_url} - {e}")
    except requests.RequestException as e:
      print(f"An error occurred while handiling the request {web_url} - {e}")
    
    response_time_display = round(response_time, 2) if response_time else "N/A"
    end_time = datetime.datetime.now()
    print(f"{datetime.datetime.now()} {web_url} {website_status} {response_time_display} {status_code}")

  return
website_analyzer()

