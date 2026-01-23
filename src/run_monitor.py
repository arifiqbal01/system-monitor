

import asyncio
from src.helpers.retry import retry
from src.services.observe_website import observe_website
from src.services.status_checker import status_checker
from src.domain.model import Config, Website,  WebsiteFailure, WebsiteFailureTypes, CheckResult, WebsiteReport
from src.domain.exceptions import WebsiteError

async def run_monitor(config: Config, websites: Website):
    tasks = []
    for website in websites:
        async def task(w=website):    
            try:
                result = await retry(
                    lambda: (observe_website(w, config)),
                    retries=3,
                    delay=1,
                    backoff=2,
                )
            except WebsiteError as e:
                if e.failure_type == WebsiteFailure(WebsiteFailureTypes.SEMANTIC) or e.failure_type == WebsiteFailure(WebsiteFailureTypes.HTTP):
                    result = CheckResult(
                        website = w,
                        response_time = result.response_time,
                        http_code = result.http_code,
                        failure = WebsiteFailure(
                            type = e.failure_type,
                            message = str(e)
                        )
                    )
                else:
                    result = CheckResult(
                        website = w,
                        response_time = None,
                        http_code = None,
                        failure = WebsiteFailure(
                            type = e.failure_type,
                            message = str(e)
                        )
                    )
            status = status_checker(result)
            return WebsiteReport(
                website = w,
                status = status.name,
                response_time = result.response_time,
                http_code = result.http_code,
                failure = result.failure.type.name
            )
        tasks.append(task())
    return await asyncio.gather(*tasks, return_exceptions=True)
