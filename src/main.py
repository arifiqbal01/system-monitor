from src.helpers.loader import loader
from src.services.request import web_request
from src.services.status import web_status
from src.services.report import analyze_log
from src.helpers.retry import retry
from time import time

data = loader()
print(data)

for website in websites:
    result = web_url(website)
    website = result[0]
    if result[1]:
        error_message = result[1]
        response_time = None
        status_code = None
        retry(website, error_message, status_code, timeout)
    else:
        single_request = web_request(website, timeout)
        response_time = single_request[1]
        status_code = single_request[2]
        error_message = single_request[3]
        retry(website, error_message, status_code, timeout)
    
    website_status = web_status(website, status_code, error_message, response_time)
    response_time = f"{response_time:.0f}ms" if response_time else response_time
    logger.info(f"{website} | {website_status} | {response_time} | {status_code} | {error_message}")

logfile = "./logs/monitor.log"
analyze_log(logfile)
time.sleep(interval)