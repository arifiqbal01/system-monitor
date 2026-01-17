from src.helpers.logger import logger
from .model import WebStatus, Website, CheckResult, WebsiteFailureTypes, WebsiteFailure

def  status_checker(result):
     if result.status_code in range(200, 400) and result.failure.type == WebsiteFailureTypes.NONE:
          return WebStatus.UP
     elif result.failure.type != WebsiteFailureTypes.NONE and result.status_code == None:
          return WebStatus.DOWN
     elif result.status_code and result.failure.type != WebsiteFailureTypes.NONE or result.status_code in range(400, 600):
          return WebStatus.DEGRADED
     else:
          return WebStatus.UNKNOWN