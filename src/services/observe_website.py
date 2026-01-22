import requests
from src.helpers.logger import logger
from src.domain.model import Config, Website, CheckResult, WebsiteFailureTypes, WebsiteFailure
from src.domain.exceptions import WebsiteError, SemanticError, DnsError, HttpError, NetworkError, TimeoutError, InvalidUrlError


def observe_website(website, cfg):
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
        logger.info(f"Initalizing http request for {website.URL}")
        r = requests.get(website.URL, timeout=cfg.timeout_seconds)
        logger.info(f"Successful http request for {website.URL}")
        r_time = r.elapsed.total_seconds() * 1000
        for k in keywords:
            if k in r.text and r.status_code == 200:
                logger.warning(f"{website.URL}: {k}")
                raise SemanticError(k)
                break
        return CheckResult(
            website = website,
            response_time = r_time,
            http_code = r.status_code,
            failure = WebsiteFailure(WebsiteFailureTypes.NONE)
        )      
    except requests.HTTPError as e:
        logger.warning(f"Http request failed for {website.URL}. Reason: {e}")
        raise HttpError(r.status_code)
    
    except requests.exceptions.ConnectionError as e:
        logger.warning(f"Http request failed for {website.URL}. Reason: {e}")
        raise NetworkError

    except requests.exceptions.Timeout as e:
        logger.warning(f"Http request failed for {website.URL}. Reason: {e}")
        raise TimeoutError

    except requests.RequestException as e:
        logger.warning(f"Http request failed for {website.URL}. Reason: {e}")
        raise WebsiteError

    