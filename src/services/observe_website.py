import aiohttp
import asyncio
from src.helpers.logger import logger
from src.domain.model import Config, Website, CheckResult, WebsiteFailureTypes, WebsiteFailure
from src.domain.exceptions import WebsiteError, SemanticError, DnsError, HttpError, NetworkError, TimeoutError, InvalidUrlError


async def observe_website(website, config): 
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
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=config.timeout_seconds)
        ) as session:
            async with session.get(website.URL) as r:
                logger.info(f"Successful http request for {website.URL}")
                
                r_time = r.elapsed.total_seconds() * 1000 if hasattr(r, "elapsed") else None
                text = await r.text()
                http_code = r.status
                for k in keywords:
                    if k in text and http_code == 200:
                        logger.warning(f"{website.URL}: {k}")
                        raise SemanticError(k)
                        break
                
                if http_code in range(400, 600):
                    logger.warning(f"Server or client Error {website.URL}")
                    raise HttpError(http_code)
                
                return CheckResult(
                    website = website,
                    response_time = r_time,
                    http_code = http_code,
                    failure = WebsiteFailure(WebsiteFailureTypes.NONE)
                )      
    except aiohttp.ClientResponseError as e:
        logger.warning(f"Http request failed for {website.URL}. Reason: {e}")
        raise HttpError(http_code)
    
    except aiohttp.ClientConnectorError as e:
        logger.warning(f"Http request failed for {website.URL}. Reason: {e}")
        raise NetworkError

    except asyncio.TimeoutError as e:
        logger.warning(f"Http request failed for {website.URL}. Reason: {e}")
        raise TimeoutError

    except aiohttp.ClientError as e:
        logger.warning(f"Http request failed for {website.URL}. Reason: {e}")
        raise WebsiteError