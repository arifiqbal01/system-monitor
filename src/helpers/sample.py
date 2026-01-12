from dataclasses import dataclass
from enum import Enum, auto
from time import time
from typing import Optional


# =========================
# 1. DOMAIN MODEL (INVARIANTS)
# =========================

@dataclass(frozen=True)
class Website:
    """
    Invariant:
    - Identity is stable
    - Never depends on network, DNS, or retries
    """
    url: str


# =========================
# 2. ERROR & FAILURE MODEL
# =========================

class FailureType(Enum):
    NONE = auto()
    DNS = auto()
    NETWORK = auto()
    TIMEOUT = auto()
    HTTP = auto()
    SEMANTIC = auto()
    UNKNOWN = auto()


@dataclass
class Failure:
    """
    Explicit failure signal.
    No strings used for control flow.
    """
    type: FailureType
    message: Optional[str] = None


# =========================
# 3. OBSERVATION RESULT
# =========================

@dataclass
class CheckResult:
    website: Website
    response_time_ms: Optional[int]
    status_code: Optional[int]
    failure: Failure


# =========================
# 4. OBSERVATION LAYER (IO ONLY)
# =========================

def observe(website: Website, timeout: int) -> CheckResult:
    """
    Responsibility:
    - Perform observation
    - Report facts
    - NO decisions
    """
    start = time()

    try:
        # imagine HTTP request here
        elapsed = int((time() - start) * 1000)
        return CheckResult(
            website=website,
            response_time_ms=elapsed,
            status_code=200,
            failure=Failure(FailureType.NONE)
        )

    except TimeoutError:
        return CheckResult(
            website=website,         
            response_time_ms=None,
            status_code=None,
            failure=Failure(FailureType.TIMEOUT, "request timed out")
        )


# =========================
# 5. DECISION LAYER (PURE LOGIC)
# =========================

class WebsiteStatus(Enum):
    UP = auto()
    DOWN = auto()
    DEGRADED = auto()
    UNKNOWN = auto()


def classify(result: CheckResult) -> WebsiteStatus:
    """
    Responsibility:
    - Convert signals into meaning
    - No IO
    - No logging
    """
    if result.failure.type == FailureType.NONE and result.status_code in range(200, 400):
        return WebsiteStatus.UP

    if result.failure.type in {FailureType.DNS, FailureType.NETWORK, FailureType.TIMEOUT}:
        return WebsiteStatus.DOWN

    if result.status_code and result.status_code >= 500:
        return WebsiteStatus.DEGRADED

    return WebsiteStatus.UNKNOWN


# =========================
# 6. RETRY POLICY (CONTROL, NOT IO)
# =========================

def should_retry(result: CheckResult) -> bool:
    """
    Explicit retry policy.
    No strings. No side effects.
    """
    return result.failure.type in {
        FailureType.TIMEOUT,
        FailureType.NETWORK
    }


# =========================
# 7. ORCHESTRATION (GLUE ONLY)
# =========================

def run_check(website: Website, timeout: int, max_retries: int = 3):
    """
    Responsibility:
    - Coordinate layers
    - No business logic
    """
    for attempt in range(1, max_retries + 1):
        result = observe(website, timeout)

        if not should_retry(result):
            break

    status = classify(result)
    return status, result
