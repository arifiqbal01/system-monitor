from logger import logger

def  web_status(website, status_code, error_message, response_time):
    status = ("DOWN", "UP", "DEGRADED", "Unknown")
    website_status = None

    if error_message and status_code is None:
         website_status = status[0]
    elif status_code and error_message or status_code in range(400, 600):
         website_status = status[2]
    elif status_code in range(200, 400) and error_message is None:
         website_status = status[1]
    else:
         website_status = status[3]
    
    return website_status