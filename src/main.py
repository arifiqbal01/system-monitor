from time import time
from src.helpers.loader import loader
from src.helpers.retry import retry
from src.services.observe_website import observe_website
from src.services.status_checker import status_checker
from src.services.summary_maker import summary_maker
from src.domain.model import Config, Website,  WebsiteFailure, WebsiteFailureTypes, CheckResult, WebsiteReport
from src.domain.exceptions import WebsiteError

data = loader()
cfg = data[1]
websites = data[0]

def recorder(config: Config, websites: Website):
    for website in websites:
        print("retry started as lambda")
        try:
            result = retry(lambda: observe_website(website, cfg))
        except WebsiteError as e:
            if e.failure_type == WebsiteFailure(WebsiteFailureTypes.SEMANTIC):
                result = CheckResult(
                    website = website,
                    response_time = result.response_time,
                    http_code = result.http_code,
                    failure = WebsiteFailure(
                        type = e.failure_type,
                        message = str(e)
                    )
                )
            else:
                result = CheckResult(
                    website = website,
                    response_time = result.response_time,
                    http_code = None,
                    failure = WebsiteFailure(
                        type = e.failure_type,
                        message = str(e)
                    )
                )
            print("******", result)
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

time.sleep(interval)
"""