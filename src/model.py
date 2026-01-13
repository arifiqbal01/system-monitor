from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
import json
from urllib.parse import urlparse
import socket

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
    failure: Failure

class WebStatus(Enum):
    UP = auto()
    DOWN = auto()
    DEGRADED = auto()
    UNKNOWN = auto()


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
                error_message = None
                address_info = None
                try:
                    parsed_url = urlparse(website)
                    netlocation = parsed_url[1] if not parsed_url[2] == website else website
                    
                except AttributeError as e:
                    return Failure(type=FailureTypes.INVALID_URL, message="URL syntax error: missing scheme")
            
    except FileNotFoundError:
        print("file not found!")
loader()

def dns():
    try:
        address_info = socket.getaddrinfo(netlocation, None)
        if parsed_url[0]:
            website = parsed_url[0] + "://" + netlocation + parsed_url[2]
            return Website(URL=website)
        else:
            website = "https://" + netlocation 
            return Website(URL=website)
    except socket.gaierror as e:
        return Failure(type=FailureTypes.DNS, message="Hostname name or service not known")