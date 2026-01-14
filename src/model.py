from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
import json
from urllib.parse import urlparse
import socket
import time

@dataclass(frozen=True)
class Website:
    URL: str

@dataclass(frozen=True)
class Config:
    interval_minutes: int
    timeout_seconds: int
    retries: int

class WebsiteEvents(Enum):
    CHECK_STARTED = auto()
    CHECK_SUCCEEDED = auto()
    DNS_FAILURE = auto()
    TIMEOUT = auto()
    HTTP_ERROR = auto()
    RECOVERED = auto()

@dataclass
class WebsiteEvent:
    type: WebsiteEvents
    subject: str
    time: str
    source: str
    message: Optional[str] = None

class SystemEvents(Enum):
    CONFIG_LOADED = auto()
    CONFIG_FILE_MISSING = auto()
    INVALID_URL_IN_CONFIG = auto()
    JSON_PARSE_ERROR = auto()
    INTERNAL_ERROR = auto()

@dataclass
class SystemEvent:
    type: SystemEvents
    subject: str
    time: str
    source: str
    message: Optional[str] = None

class WebsiteFailureTypes(Enum):
    NONE = auto()
    DNS = auto()
    NETWORK = auto()
    TIMEOUT = auto()
    HTTP = auto()
    SEMANTIC = auto()
    INVALID_URL = auto()
    UNKNOWN = auto()

class SystemFailureTypes(Enum):
    NONE = auto()
    InvalidConfig = auto()
    InvalidURL = auto()
    ConfigNotFound = auto()
    ParseError = auto()
    InternalError = auto()
    Misconfiguration = auto()

@dataclass
class WebsiteFailure:
    type: WebsiteFailureTypes
    message: Optional[str] = None

@dataclass
class SystemFailure:
    type: SystemFailureTypes
    message: Optional[str] = None

@dataclass
class CheckResult:
    website: Website
    response_time: Optional[int]
    status_code: Optional[int]
    failure: WebsiteFailure

class WebStatus(Enum):
    UP = auto()
    DOWN = auto()
    DEGRADED = auto()
    UNKNOWN = auto()

def now():
  current_time = time.time()

def normalize_validate_URL(website):
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


config_path = "./config.json"

def loader():
    try:
        with open(config_path, 'r') as readFile:
            data = json.load(readFile)
            config = Config(
                interval_minutes = data.get("interval_minutes", 30),
                timeout_seconds = data.get("timeout_seconds", 5),
                retries = data.get("retries", 3),
            )
            websites = data.get("websites", [])
            for website in websites:
                website = website
                normalize_validate_URL(website)
    except FileNotFoundError:
        print("file not found!")
loader()