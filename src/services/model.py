from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

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

@dataclass
class WebReport:
    datetime: 
    website: Website
    status: str
    response_time: Optional[int]
    http_code: Optional[int]
    failure: WebsiteFailure