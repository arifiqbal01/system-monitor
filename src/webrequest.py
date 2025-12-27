import requests
import time
import datetime
from weburl import web_url

data = web_url()
websites = data[0]
interval = data[1]
timeout = data[2]

def web_request(websites, interval, timeout):
    request_data = {}
    response_time = None
    status_code = None
    errror_message = None
    
    for website in websites:
        try:
            r = requests.get(website, timeout=timeout)
            response_time = r.elapsed.total_seconds() * 1000
            status_code = r.status_code
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
    print(request_data)
    return request_data

web_request(websites, interval, timeout)