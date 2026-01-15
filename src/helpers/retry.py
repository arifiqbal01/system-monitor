from ..services.request import web_request
from .logger import logger

def retry(website, error_message, status_code, timeout):
    max_retries = 3
    for attempt in range(max_retries):
        if error_message and error_message == "Hostname name or service not known":
            logger.warning(f"{website} | Retrying!")
            result = web_url(website)
            if not result[1]:
                website = result[0]
                error_message = result[1]
                response_time = None
                status_code = None
                logger.info(f"{website} | Retry Succeeded!")
                break
        
        elif error_message and (
            error_message == "Connection Refused Error" or 
            error_message == "Request timed out" or 
            error_message == "An error occurred while handiling the request"):
            logger.warning(f"{website} | Retrying!")
            single_request = web_request(website, timeout)
            if not single_request[3]:
                website = single_request[0]
                response_time = single_request[1]
                status_code = single_request[2]
                error_message = single_request[3]
                logger.info(f"{website} | Retry Succeeded!")
                break

        elif status_code == 408 or status_code == 429 or status_code in range(500, 600):
            logger.warning(f"{website} | Retrying!")
            single_request = web_request(website, timeout)
            if not single_request[3]:
                website = single_request[0]
                response_time = single_request[1]
                status_code = single_request[2]
                error_message = single_request[3]
                logger.info(f"{website} | Retry Succeeded!")
                break
                
