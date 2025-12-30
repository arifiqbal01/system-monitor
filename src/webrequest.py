import requests
from weburl import web_url

def web_request(websites, interval, timeout):
    request_data = {}
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
    
    for website in websites:
        try:
            r = requests.get(website, timeout=timeout)
            response_time = r.elapsed.total_seconds() * 1000
            status_code = r.status_code
            html = r.text
            is_body_degrade = None
            for k in keywords:
                if k in html and status_code == 200:
                    is_body_degrade = k
                    break
            error_message = None
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
        
        request_data.update({website: (response_time, status_code, error_message, is_body_degrade)})
        html = None
        is_body_degrade = None
        status_code = None
        error_message = None
        response_time = None
        
    return request_data
