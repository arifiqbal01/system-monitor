
from logger import logger
from json import dumps, loads
def analyze_log(logfile):
  websites_summary = {
    "UP": {"total": 0, "websites": []}, 
    "DOWN": {"total": 0, "websites": []}, 
    "DEGRADED": {"total": 0, "websites": []}, 
    "UNKNOWN": {"total": 0, "websites": []}}
  errors = {}
  hourly = {}
  seen = []
  log_lines = []

  def line_normalizer(content):
    if not content:
      return
    for line in content:
      if line in seen:
        continue
      else:
        seen.append(line)
        line = line.strip()
        parts = line.split('|')
        parts = [part.strip() for part in parts]
        yield parts
  
  def summary_maker(content):
    log_lines = []
    for part in line_normalizer(content):
      date = part[0]
      time = part[1]
      log_level = part[2]
      website = part[3]
      website_status = part[4]
      response_time = part[5]
      status_code = part[6]
      error_message = part[7]
      log_lines.append(part)
      if log_level == "INFO":
        if website_status  == "UP":
          websites_summary["UP"]["total"] += 1
          websites_summary["UP"]["websites"].append(website)
        elif website_status  == "DOWN":
          websites_summary["DOWN"]["total"] += 1
          websites_summary["DOWN"]["websites"].append(website)
        elif website_status  == "DEGRADED":
          websites_summary["DEGRADED"]["total"] += 1
          websites_summary["DEGRADED"]["websites"].append(website)
        else:
          websites_summary["UNKNOWN"]["total"] += 1
          websites_summary["UNKNOWN"]["websites"].append(website)
      elif log_level == "ERROR":
        errors.append({
          "website": website,
          "error_message": error_message
        })
    print("log:")
    print(log_lines)
    return websites_summary, log_lines
  
  try:
    with open(logfile, 'r') as config_file:
      try:
        with open("./src/data.json", "rb") as data_file:
          data = loads(data_file.read())
          prev_end_position = data.get("prev_end_position", 0)
          config_file.seek(prev_end_position)
          content = config_file.readlines()
          summary_maker(content)
          tell = config_file.tell
          config_file.seek(0, 2)
          with open("./src/data.json", "w") as data_file:
            data = {"prev_end_position": tell()}
            data_file.write(dumps(data))
      except FileNotFoundError as e:
        logger.warning("Data file not found. Creating a new one.", exc_info=e)
        prev_end_position = 0
        config_file.seek(0)
        content = config_file.readlines()
        summary_maker(content)
        config_file.seek(0,2)
        tell = config_file.tell
        with open("./src/data.json", "w") as data_file:
          data = {"prev_end_position": tell()}
          data_file.write(dumps(data))
  except FileNotFoundError as e:
    logger.error(f"Log file {logfile} not found. Creating a new one.", exc_info=e)

  print("Websites Summary:")
  print(websites_summary)
  
  return