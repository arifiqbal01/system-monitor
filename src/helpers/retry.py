from .logger import logger
from typing import Callable, TypeVar
import time

T = TypeVar("T")

def retry(
operation: Callable[[], T], 
retries: int= 3, 
delay: float = 1.0, 
backoff: float= 2.0
) -> T:
    for attempt in range(1, retries + 1):
        try:
            return operation()
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed!")
            if attempt == retries:
                raise
            logger.warning(f"Trying in {delay} seconds!")
            time.sleep(delay)