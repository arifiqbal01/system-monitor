from src.helpers.logger import logger
from src.domain.model import WebStatus, Website, CheckResult, WebsiteFailureTypes, WebsiteFailure

def  status_checker(result):
     logger.info(f"Initalizing status check for {result.website.URL}")
     if result.http_code in range(200, 400) and result.failure.type == WebsiteFailureTypes.NONE:
          logger.info(f"{result.website.URL} status is {WebStatus.UP}")
          return WebStatus.UP
     elif result.failure.type == WebsiteFailureTypes.SEMANTIC or result.failure.type == WebsiteFailureTypes.HTTP:
          logger.info(f"{result.website.URL} status is {WebStatus.DEGRADED}")
          return WebStatus.DEGRADED
     elif result.failure.type != WebsiteFailureTypes.NONE and result.http_code == None:
          logger.info(f"{result.website.URL} status is {WebStatus.DOWN}")
          return WebStatus.DOWN
     else:
          logger.info(f"{result.website.URL} status is {WebStatus.UNKNOWN}")
          return WebStatus.UNKNOWN