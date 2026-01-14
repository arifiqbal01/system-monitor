from urllib.parse import urlparse
from dataclasses import dataclass
from enum import Enum, auto
import socket

@dataclass(frozen=True)
class Website:
  URL: str

def normalize_validate_URL(website):
  p = urlparse(website)
  try:
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
    print(e)
  except socket.gaierror as e:
    print(e)
  return  Website(URL=website)

website = "arif-iqbal.com"
normalize_validate_URL(website)