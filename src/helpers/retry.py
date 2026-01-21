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
            operation()
        except Exception as e:
            print(f"attempt {attempt} failed for {e}")
            if attempt == retries:
                raise
            print(f"Trying in {delay} seconds")
            time.sleep(2)