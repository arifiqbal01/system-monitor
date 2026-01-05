line_x = line.strip()
        parts = line_x.split('|')
        parts = [part.strip() for part in parts]
        log_date = parts[0]
        log_time = parts[1]
        log_info = parts[2] + '|' + parts[3] + '|' + parts[4] + '|' + parts[5] + '|' + parts[6] + '|' + parts[7]
        if log_info in seen:
          print("Duplicate log entry found, skipping...", log_info)
          continue
        else:
          print("New log entry found, processing...", log_info)
          seen.append(log_info)
          log_info = log_info.split('|')

        return log_info, line_count
  print(line_count)
  def summary_maker(logline):
    for log_info, line_count in line_normalizer(logfile):
      log_line = log_info
      log_level = log_line[0]
      website = log_line[1] 
      website_status = log_line[2]
      response_time = log_line[3]
      status_code = log_line[4]
      error_message = log_line[5]
      if log_level != "INFO":
        continue
      else:
        if website_status == "UP":
          websites_summary["UP"]["total"] += 1
          websites_summary["UP"]["websites"].append(website)
        elif website_status == "DOWN":
          websites_summary["DOWN"]["total"] += 1
          websites_summary["DOWN"]["websites"].append(website)
          errors.update({website: error_message})
        elif website_status == "DEGRADED":
          websites_summary["DEGRADED"]["total"] += 1
          websites_summary["DEGRADED"]["websites"].append(website)
          errors.update({website: error_message})
        elif website_status == "UNKNOWN":
          websites_summary["UNKNOWN"]["total"] += 1
          websites_summary["UNKNOWN"]["websites"].append(website)
          errors.update({website: error_message})


  
"""

  

  

  report_file = "./reports/report.txt"
  with open(report_file, 'w') as file:

    file.write("Log Summary")
    file.write("\n")
    file.write("----------------------")
    file.write("\n")
    file.write("\n")

    for key, value in websites_summary.items():
      file.write(f"{key}: {value} \n")

    file.write("\n")
    file.write("Websites UP \n")
    for w in websites_up:
        file.write(f"- {w} \n")

    file.write("\n")
    file.write("Websites with Errors \n")
    for w, e in errors.items():
      if e:
        file.write(f"- {w} : {e} \n")
    """