from weburl import web_url
from webrequest import web_request

data = web_url()
websites = data[0]["websites"]
interval = data[0]["interval"]
timeout = data[0]["timeout"]
failed = data[1]

data2 = web_request(websites, interval, timeout)
print(data2)
error_message = webrequest.error_message
status_code = webrequest.status_code
web_url = webrequest.web_url
response_time = webrequest.response_time

print("before calling", error_message, status_code, response_time, web_url)

def web_status(web_url, status_code, error_message, response_time):
    status = ("DOWN", "UP", "DEGRADED", "Unknown")
    print(webs_url, status_code, response_time, error_message)

    return
website_status(web_url, status_code, error_message) 