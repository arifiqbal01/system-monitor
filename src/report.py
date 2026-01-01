def analyze_log(logfile):
  summary = {"INFO": 0, "ERROR": 0, "WARNING": 0}
  errors = []
  hourly = {}

  with open(logfile) as file:
    for line in file:
      if not line:
        continue
      lines_x = line.strip()
      parts = lines_x.split('|')
      if len(parts) < 8:
        continue
      
      date, time, log_level, website, website_status, response_time, status_code, error_message = parts
      print(parts)
      hour = time[:2]

      if log_level in summary:
        summary[log_level] += 1

      if log_level == "ERROR":
        errors.append(message)

      hourly[hour] = hourly.get(hour, 0) + 1

  report_file = "./reports/report.txt"
  print(summary, errors, hourly)
  with open(report_file, 'w') as file:

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