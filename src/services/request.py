import requests
from . import logger

def web_request(website, timeout):
    response_time = None
    status_code = None
    errror_message = None
    html = None
    
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
        r = requests.get(website, timeout=timeout)
        response_time = r.elapsed.total_seconds() * 1000
        status_code = r.status_code
        html = r.text
        error_message = None
        for k in keywords:
            if k in html and status_code == 200:
                error_message = k
                break      
        error_message = error_message
    except requests.HTTPError as e:
        error_message = "An HTTP error occurred"
    except requests.exceptions.ConnectionError as e:
        error_message = "Connection Refused Error"
    except requests.exceptions.Timeout as e:
        error_message = "Request timed out"
    except requests.exceptions.JSONDecodeError as e:
        error_message = "Couldn’t decode the text into json"
    except requests.RequestException as e:
        error_message = "An error occurred while handiling the request"
    
    return website, response_time, status_code, error_message
