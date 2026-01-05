
from urllib.parse import urlparse
import socket
from logger import logger

def web_url(website):
    error_message = None
    address_info = None
    try:
        parsed_url = urlparse(website)
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

