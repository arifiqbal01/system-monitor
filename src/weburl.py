import json
from urllib.parse import urlparse
import socket

config = "./config.json"

def web_url():
    with open(config, 'r') as readFile:
        config_data = json.load(readFile)
        interval = config_data.get("interval_minutes", 30)
        timeout = config_data.get("timeout_seconds", 5)
        websites = config_data.get("websites", [])
    
    url_pass = {"websites": [], "interval": interval, "timeout": timeout}
    url_fail = {}
    error_message = None
    address_info = None
    for website in websites:
        try:
            parsed_url = urlparse(website)
            netlocation = parsed_url[1] if not parsed_url[2] == website else website
            try:
                address_info = socket.getaddrinfo(netlocation, None)
                if parsed_url[0]:
                    web_url = parsed_url[0] + "://" + netlocation + parsed_url[2]
                else:
                    web_url = "https://" + netlocation
                url_pass["websites"].append(web_url)
            except socket.gaierror as e:
                error_message = "Hostname name or service not known"
                url_fail.update({website: error_message})
        except AttributeError:
            error_message = "Invalid domain"
            url_fail.update({website: error_message})
    return url_pass, url_fail
web_url()