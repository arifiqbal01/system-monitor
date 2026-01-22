from urllib.parse import urlparse
import socket
from ..domain.model import Website, SystemFailure, WebsiteFailure, WebsiteFailureTypes, SystemFailureTypes
from .logger import logger

def normalize_url(website):
  try:
    logger.info(f"Initalizing normalization of website(s)")
    p = urlparse(website)
    logger.info(f"Parsing successful for {website}")
    if p.scheme and p.netloc and not p.path:
      socket.getaddrinfo(p.netloc, None)
      website = f"{p.scheme}://{p.netloc}"

    elif p.path and not p.scheme and not p.netloc:
      socket.getaddrinfo(p.path, None)
      website = f"https://{p.path}"

    elif p.netloc and not p.scheme:
      socket.getaddrinfo(p.netloc, None)
      website = f"https://{p.netloc}"

    elif p.scheme and p.netloc and p.path:
      socket.getaddrinfo(p.netloc, None)
      website = f"{p.scheme}://{p.netloc}{p.path}"  
  except ValueError as e:
    SystemFailure(type=SystemFailureTypes.InvalidURL, message=e)
    logger.warning(f"Parsing failed for {website}. Reason: {e}")
  except socket.gaierror as e:
    WebsiteFailure(type=WebsiteFailureTypes.DNS, message=e)
    logger.warning(f"Parsing failed for {website}. Reason: {e}")
  
  return  Website(URL=website)