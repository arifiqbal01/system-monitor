import json
import requests

config = "./config.json"

def runTimeInputs():
  websites = []

  web_urls = input("Input your comma seprated URls to be tested: ").strip()
  parts = web_urls.split(',')
  for part in range(len(parts)):
    web_url = parts[part].strip()
    websites.append(web_url)
  
  interval_minutes = int(input("Set interval-time in minutes or use default 30 mintues: ")) or 30
  timeout_seconds = int(input("Set timeout-seconds or use default 5 seconds: ")) or 5
  
  return

def website_analyzer():
  up_state = "UP"
  down_state = "DOWN"
  with open(config, 'r') as readFile:
    config_data = json.load(readFile)
    
    interval = config_data.get("interval_minutes", 30)
    timeout = config_data.get("timeout_seconds", 5)
    websites = config_data.get("websites", [])
  
  schemes = ['http://', 'https://']
  for website in websites:
    web_url = schemes[1] + website if not website.startswith('http://', 0) and not website.startswith('https://', 0) else website
    try:
      r = requests.get(web_url, timeout=timeout)
      if r.status_code == 200:
        print(r.final_url)
    except requests.exceptions.JSONDecodeError as e:
      print(f"Error accessing web url {web_url} : {r.status_code} - {e}")

  return
website_analyzer()

def analyze_log(filePath):
  summary = {"INFO": 0, "ERROR": 0, "WARNING": 0}
  errors = []
  hourly = {}

  with open(filePath) as file:
    for line in file:
      
      if not line:
        continue
      
      lines_x = line.strip()
      parts = lines_x.split(maxsplit=3)

      if len(parts) < 4:
        continue
        
      date, time, log_level, message = parts
      hour = time[:2]

      if log_level in summary:
        summary[log_level] += 1

      if log_level == "ERROR":
        errors.append(message)

      hourly[hour] = hourly.get(hour, 0) + 1

  new_file_path = "./report.txt"

  with open(new_file_path, 'w') as file:

    file.write("Log Summary")
    file.write("\n")
    file.write("----------------------")
    file.write("\n")
    file.write("\n")

    for key, value in summary.items():
      file.write(f"{key}: {value} \n")

    file.write("\n")
    file.write("Error Details \n")
    for e in errors:
      file.write(f"- {e} \n")

    return


file_path = "logs/monitor.log"
analyze_log(file_path)
