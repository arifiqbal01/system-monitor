from weburl import web_url
from webrequest import web_request
from weblogger import logger

data = web_url()
websites = data[0]["websites"]
interval = data[0]["interval"]
timeout = data[0]["timeout"]
failed = data[1]
data2 = web_request(websites, interval, timeout)

def web_status():
    status = ("DOWN", "UP", "DEGRADED", "Unknown")
    web_status = {}

    if failed:
        for f in failed.items():
            website = f[0]
            error_message = f[1]
            web_status.update({website: (status[0], error_message)})
            logger.error(f"{status[0]} : {error_message}")
    else:
        pass
        
    for d in data2.items():
        website = d[0]
        response_time = d[1][0]
        status_code = d[1][1]
        error_message = d[1][2]
        is_body_degrade = d[1][3]
        if error_message:
            web_status.update({website: (status[0], response_time, status_code, error_message)})
            logger.error(f"{website} : {status[0]} : {error_message}")
        elif status_code and is_body_degrade or status_code in range(400, 600):
            web_status.update({website: (status[2], response_time, status_code, is_body_degrade)})
            logger.warning(f"{website} : {status[2]} : {response_time} : {status_code} : {is_body_degrade}")
        elif status_code in range(200, 400) and is_body_degrade is None:
            web_status.update({website: (status[1], response_time, status_code, error_message)})
            logger.info(f"{website} : {status[1]} : {response_time} : {status_code}")
        else:
            web_status.update({website: (status[3], response_time, status_code, error_message)})
            logger.error(f"{website} : {status[3]} : {response_time} : {status_code} : {error_message}")
    
    return web_status
web_status()