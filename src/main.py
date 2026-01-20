from time import time
from src.helpers.loader import loader
from src.services.observe_website import observe_website
from src.services.status_checker import status_checker
from src.services.summary_maker import summary_maker
from src.services.model import Config, Website, CheckResult, WebsiteReport
from src.services.observe_website import observe_website

data = loader()
cfg = data[1]
websites = data[0]

def recorder(config: Config, websites: Website):
    for website in websites:
        result = observe_website(website, cfg)
        status = status_checker(result)
        yield WebsiteReport(
            website = website,
            status = status.name,
            response_time = result.response_time,
            http_code = result.http_code,
            failure = result.failure.type.name
        )

def main():
    reports = []
    for report in recorder(cfg, websites):
        reports.append(report)
    summary_maker(reports)
main()

"""
logger.info(f"{website} | {website_status} | {response_time} | {http_code} | {error_message}")
time.sleep(interval)
"""