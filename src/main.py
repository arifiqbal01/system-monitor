from time import time
from src.helpers.loader import loader
from src.services.observe_website import observe_website
from src.services.status_checker import status_checker
from src.services.report_maker import report_maker
from src.services.model import Config, Website, CheckResult
from src.services.observe_website import observe_website

data = loader()
cfg = data[1]
websites = data[0]

def main(config: Config, websites: Website):
    monitor_result = []
    for website in websites:
        result = observe_website(website, cfg)
        status = status_checker(result)
        monitor_result.append({
            "website": website.URL,
            "status": str(status.name),
            "response_time": result.response_time,
            "http_code": result.status_code,
            "failure": str(result.failure.type.name)
        })
    report_maker(monitor_result)
    return monitor_result
main(cfg, websites)

"""
logger.info(f"{website} | {website_status} | {response_time} | {status_code} | {error_message}")

logfile = "./logs/monitor.log"

time.sleep(interval)
"""