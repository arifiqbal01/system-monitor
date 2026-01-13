
from urllib.parse import urlparse
import socket
from logger import logger
import model

config = "./config.json"
try:
    with open(config, 'r') as readFile:
        config_data = json.load(readFile)
        interval = config_data.get("interval_minutes", 30)
        timeout = config_data.get("timeout_seconds", 5)
        websites = config_data.get("websites", [])
        for website in websites:
            result = web_url(website)
            website = result[0]

            def web_url():
                error_message = None
                address_info = None
                retry = 3
                try:
                    parsed_url = urlparse(website)
                    return Website(
                        URL=parsed_url
                    )
                    netlocation = parsed_url[1] if not parsed_url[2] == website else website
                    try:
                        address_info = socket.getaddrinfo(netlocation, None)
                        if parsed_url[0]:
                            website = parsed_url[0] + "://" + netlocation + parsed_url[2]
                        else:
                            website = "https://" + netlocation
                    except socket.gaierror as e:
                        error_message = "Hostname name or service not known"
                except AttributeError as e:
                    error_message = "Invalid domain"

                return website, error_message

