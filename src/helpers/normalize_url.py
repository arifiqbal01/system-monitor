from urllib.parse import urlparse
import socket
from ..services.model import Website, SystemFailure, WebsiteFailure, WebsiteFailureTypes, SystemFailureTypes

def normalize_url(website):
  try:
    p = urlparse(website)
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
  except socket.gaierror as e:
    WebsiteFailure(type=WebsiteFailureTypes.DNS, message=e)
  
  return  Website(URL=website)