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

{'UP': {'total': 1, 'websites': {'website': 'https://google.com', 'response_time': '481ms', 'status_code': '200'}}, 
'DOWN': {'total': 4, 'websites': [
  {'website': 'http://example.com:81', 'response_time': 'None', 'status_code': 'None', 'error_message': 'Hostname name or service not known'}, 
  {'website': 'http://example.com:71', 'response_time': 'None', 'status_code': 'None', 'error_message': 'Hostname name or service not known'}, 
  {'website': 'https://httpstat.us/404', 'response_time': 'None', 'status_code': 'None', 'error_message': 'Connection Refused Error'}, 
  {'website': 'http://httpstat.us/503', 'response_time': 'None', 'status_code': 'None', 'error_message': 'Connection Refused Error'}]}, 
'DEGRADED': {'total': 4, 'websites': [
  {'website': 'https://arif-iqbal.com/account', 'response_time': '532ms', 'status_code': '404', 'error_message': 'None'}, 
  {'website': 'http://www.webartsy.site/', 'response_time': '295ms', 'status_code': '200', 'error_message': 'domain has been suspended'}, 
  {'website': 'http://webartsy.store/', 'response_time': '281ms', 'status_code': '200', 'error_message': 'domain has been suspended'}, 
  {'website': 'http://webartsy.online/', 'response_time': '288ms', 'status_code': '200', 'error_message': 'domain has been suspended'}]}, 
'UNKNOWN': {'total': 0, 'websites': []}}