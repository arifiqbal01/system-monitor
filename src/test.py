from weburl import web_url
from webrequest import web_request

logging.basicConfig(
    filename="logs/monitor.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} : {levelname} : {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)

data = web_url()
websites = data[0]["websites"]
interval = data[0]["interval"]
timeout = data[0]["timeout"]
failed = data[1]
data2 = web_request(websites, interval, timeout)

def web_status(website, status_code, error_message, response_time, is_body_degrade):
    status = ("DOWN", "UP", "DEGRADED", "Unknown")
    web_status = {}

    if error_message:
        web_status.update({website: (status[0], response_time, status_code, error_message)})
    elif status_code and is_body_degrade or status_code in range(400, 600):
        web_status.update({website: (status[2], response_time, status_code, error_message)})
    elif status_code in range(200, 400) and is_body_degrade is None:
        web_status.update({website: (status[1], response_time, status_code, error_message)})
    else:
        web_status.update({website: (status[3], response_time, status_code, error_message)})
    print(web_status)
    return web_status

for f in failed.items():
    website = f[0]
    error_message = f[1]
    status_code = None
    response_time = None
    is_body_degrade = None
    web_status(website, status_code, error_message, response_time, is_body_degrade)

for d in data2.items():
    website = d[0]
    response_time = d[1][0]
    status_code = d[1][1]
    error_message = d[1][2]
    is_body_degrade = d[1][3]
    web_status(website, status_code, error_message, response_time, is_body_degrade)