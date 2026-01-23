import asyncio
from .logger import logger
from typing import Callable, TypeVar
import time
from ..domain.model import WebsiteFailureTypes

T = TypeVar("T")

async def retry(
operation: Callable[[], T], 
retries: int= 3, 
delay: float = 1.0, 
backoff: float= 2.0
) -> T:
    for attempt in range(1, retries + 1):
        try:
            return await operation()
        except asyncio.CancelledError as e:
            raise
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed!")
            if attempt == retries or e.failure_type == WebsiteFailureTypes.SEMANTIC:
                if attempt == retries:
                    logger.warning(f"All {attempt} attempts exhausted.")
                else:
                    logger.warning(f"Non-Retryable!")
                raise 
            logger.warning(f"Trying in {delay} seconds!")
            await asyncio.sleep(delay)
            delay *= backoff