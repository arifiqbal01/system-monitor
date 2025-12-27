import webrequest

error_message = webrequest.error_message
status_code = webrequest.status_code
web_url = webrequest.web_url
response_time = webrequest.response_time

print("before calling", error_message, status_code, response_time, web_url)

def website_status(web_url, status_code, error_message, response_time):
    status = ("DOWN", "UP", "DEGRADED", "Unknown")
    print(webs_url, status_code, response_time, error_message)

    return
website_status(web_url, status_code, error_message) 