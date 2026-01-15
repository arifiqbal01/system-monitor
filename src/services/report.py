
from . import logger
from json import dumps, loads
def analyze_log(logfile):
  websites_summary = {
    "UP": {"total": 0, "websites": []}, 
    "DOWN": {"total": 0, "websites": []}, 
    "DEGRADED": {"total": 0, "websites": []}, 
    "UNKNOWN": {"total": 0, "websites": []}}
  system_summary = {
    "errors": [],
    "warning": [],
    "info": [],
  }
  errors = []
  warning = []
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
      if len(part) == 8:
        date = part[0]
        time = part[1]
        log_level = part[2]
        website = part[3]
        website_status = part[4]
        response_time = part[5]
        status_code = part[6]
        error_message = part[7]
        log_lines.append(part)
      else:
        date = part[0]
        time = part[1]
        log_level = part[2]
        website = part[3]
        message = part[4]
      if log_level == "INFO":
        if website_status  == "UP" and website not in [item['website'] for item in websites_summary["UP"]["websites"]]:
          websites_summary["UP"]["total"] += 1
          websites_summary["UP"]["websites"].append({
            "website": website,
            "response_time": response_time,
            "status_code": status_code
          })
        elif website_status  == "DOWN" and website not in [item['website'] for item in websites_summary["DOWN"]["websites"]]:
          websites_summary["DOWN"]["total"] += 1
          websites_summary["DOWN"]["websites"].append({
            "website": website, 
            "response_time": response_time, 
            "status_code": status_code, 
            "error_message": error_message})
        elif website_status  == "DEGRADED" and website not in [item['website'] for item in websites_summary["DEGRADED"]["websites"]]:
          websites_summary["DEGRADED"]["total"] += 1
          websites_summary["DEGRADED"]["websites"].append({
            "website": website,
            "response_time": response_time,
            "status_code": status_code,
            "error_message": error_message
          })
        else:
          if website not in [item['website'] for item in websites_summary["UNKNOWN"]["websites"]]:
            websites_summary["UNKNOWN"]["total"] += 1
            websites_summary["UNKNOWN"]["websites"].append({
              "website": website,
              "response_time": response_time,
              "status_code": status_code,
              "error_message": error_message
            })
      elif log_level == "INFO" and len(parts) < 8:
        system_summary["info"].append({
          "website": website,
          "message": message
        })
      elif log_level == "ERROR":
        system_summary["error"].append({
          "website": website,
          "message": message
        })
      elif log_level == "WARNING":
        system_summary["warning"].append({
          "website": website,
          "message": message
        })
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

  report_file = "./reports/report.txt"
  with open(report_file, 'w') as file:
    file.write("Log Summary")
    file.write("\n")
    file.write("----------------------")
    file.write("\n")
    file.write("\n")

    for key, value in websites_summary.items():
      file.write(f"{key}: {value['total']} \n")
    
    if websites_summary['UP']['total'] == 0:
      file.write("\n")
    else:
      file.write("\n")
      file.write("Websites UP\n")
      for websites in websites_summary["UP"]["websites"]:
        file.write(f"- {websites['website']} \n")
    
    if websites_summary['DOWN']['total'] == 0:
      file.write("\n")
    else:
      file.write("\n")
      file.write("Websites DOWN\n")
      for websites in websites_summary["DOWN"]["websites"]:
        file.write(f"- {websites['website']} error: {websites.get('error_message', 'None')} \n")
    
    if websites_summary['DEGRADED']['total'] == 0:
      file.write("\n")
    else:
      file.write("\n")
      file.write("Websites DEGRADED\n")
      for websites in websites_summary["DEGRADED"]["websites"]:
        file.write(f"- {websites['website']} error: {websites.get('error_message', 'None')} \n")

    if websites_summary['UNKNOWN']['total'] == 0:
      file.write("\n")
    else:
      file.write("\n")
      file.write("Websites UNKNOWN\n")
      for websites in websites_summary["UNKNOWN"]["websites"]:
        file.write(f"- {websites['website']} error: {websites.get('error_message', 'None')} \n")
    
    if not errors:
      file.write("\n")
      file.write("No system errors found. \n")
      file.write("\n")
    else:
      file.write("\n")
      file.write("System Errors \n")
      for e in system_summary["errors"]:
        if e["message"]:
          file.write(f"- {e['website']} : {e['message']} \n")
    if not warning:
      file.write("\n")
      file.write("No system warning found. \n")
      file.write("\n")
    else:
      file.write("\n")
      file.write("System Warnings \n")
      for w in system_summary["warning"]:
        if w["message"]:
          file.write(f"- {w['website']} : {w['message']} \n")
  return