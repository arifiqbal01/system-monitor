import requests
from src.helpers.logger import logger
from .model import Website, CheckResult, WebsiteFailureTypes, WebsiteFailure

def observe_website(website, timeout_seconds):
    keywords = [
    "domain has been suspended",
    "account suspended",
    "hosting account suspended",
    "this account has been suspended",
    "contact your hosting provider",
    "payment overdue",
    "billing issue",
    "domain expired",
    "this domain has expired",
    "domain name has expired",
    "renew your domain",
    "domain is not configured",
    "no match for domain",
    "not found in registry",
    "this domain is parked"
    ]
    
    try:
        r = requests.get(website.URL, timeout=timeout_seconds)
        r_time = r.elapsed.total_seconds() * 1000
        html = r.text
        for k in keywords:
            if k in html and r.status_code == 200:
                return CheckResult(
                    website = website,
                    response_time = r_time,
                    status_code = r.status_code,
                    failure = WebsiteFailure(WebsiteFailureTypes.SEMANTIC, k)
                )
                break      
        return CheckResult(
            website = website,
            response_time = r_time,
            status_code = r.status_code,
            failure = WebsiteFailure(WebsiteFailureTypes.NONE)
        )
    except requests.HTTPError as e:
        return CheckResult(
            website = website,
            response_time = None,
            status_code = None,
            failure =  WebsiteFailure(WebsiteFailureTypes.HTTP, e)
        )
    except requests.exceptions.ConnectionError as e:
        return CheckResult(
            website = website,
            response_time = None,
            status_code = None,
            failure =  WebsiteFailure(WebsiteFailureTypes.NETWORK, e)
        )
    except requests.exceptions.Timeout as e:
        return CheckResult(
            website = website,
            response_time = None,
            status_code = None,
            failure =  WebsiteFailure(WebsiteFailureTypes.TIMEOUT, e)
        )
    except requests.RequestException as e:
        return CheckResult(
            website = website,
            response_time = None,
            status_code = None,
            failure =  WebsiteFailure(WebsiteFailureTypes.UNKNOWNP, e)
        )