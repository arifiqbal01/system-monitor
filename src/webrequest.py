import requests
import time
import datetime
from weburl import web_url

def web_request(websites, interval, timeout):
    request_data = {}
    response_time = None
    status_code = None
    errror_message = None
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
    
    for website in websites:
        try:
            r = requests.get(website, timeout=timeout)
            response_time = r.elapsed.total_seconds() * 1000
            status_code = r.status_code
            html = r.text
            for k in keywords:
                if k in html:
                    is_degrade = True
            error_message = None
        except requests.HTTPError as e:
            status_code = None
            error_message = "An HTTP error occurred"
        except requests.exceptions.ConnectionError as e:
            status_code = None
            error_message = "Connection Refused Error"
        except requests.exceptions.Timeout as e:
            status_code = None
            error_message = "Request timed out"
        except requests.exceptions.JSONDecodeError as e:
            status_code = None
            error_message = "Couldn’t decode the text into json"
        except requests.RequestException as e:
            status_code = None
            error_message = "An error occurred while handiling the request"
    
        request_data.update({website: (response_time, status_code, error_message)})
    
    return request_data