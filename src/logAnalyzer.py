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