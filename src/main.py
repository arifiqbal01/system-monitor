from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

@dataclass
class Website(fronzen=True):
    url: str

class FailureTypes(Enum):
    NONE = auto()
    DNS = auto()
    NETWORK = auto()
    TIMEOUT = auto()
    HTTP = auto()
    SEMANTIC = auto()
    UNKNOWN = auto()

@dataclass
class Failure:
    type = FailureType
    message = Optional(str) = None

@dataclass
class CheckResult:
    website = Website
    response_time = Optional[int]
    status_code = Optional[int]
    failure = Failure

class WebStatus(Enum):
    UP = auto()
    DOWN = auto()
    DEGRADED = auto()
    UNKOWN = auto()
