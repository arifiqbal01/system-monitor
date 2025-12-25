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