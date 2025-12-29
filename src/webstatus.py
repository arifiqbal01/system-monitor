from weburl import web_url
from webrequest import web_request

data = web_url()
websites = data[0]["websites"]
interval = data[0]["interval"]
timeout = data[0]["timeout"]
failed = data[1]
data2 = web_request(websites, interval, timeout)

def web_status(website, error_message, status_code=None, response_time=None, is_body_degrade=False):
    status = ("DOWN", "UP", "DEGRADED", "Unknown")
    """print(website, status_code, response_time, error_message, is_body_degrade)"""
    return

if failed:
    for f in failed.items():
        website = f[0]
        error_message = f[1]
        web_status(website, error_message)
else:
    pass

for d in data2.items():
    website = d[0]
    response_time = d[1][0]
    status_code = d[1][1]
    error_message = d[1][2]
    is_body_degrade = d[1][3]
    web_status(website, status_code, error_message, response_time, is_body_degrade)