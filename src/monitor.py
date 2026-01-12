import json
from url import web_url
import time
from request import web_request
from status import web_status
from report import analyze_log
from logger import logger
from helpers.retry import retry

config = "./config.json"
while True:
    try:
        with open(config, 'r') as readFile:
            config_data = json.load(readFile)
            interval = config_data.get("interval_minutes", 30)
            timeout = config_data.get("timeout_seconds", 5)
            websites = config_data.get("websites", [])
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
    except FileNotFoundError as e:
        logger.error(f"Configuration file {config} not found.", exc_info=e)
        with open("./logs/monitor.log", 'w') as config_file:
            config_file.write("")
    
    logfile = "./logs/monitor.log"
    analyze_log(logfile)
    time.sleep(interval)


