import time
from functools import wraps
import logging

# Set up a basic logger for the retry decorator
logger = logging.getLogger(__name__)

def retry(max_attempts=3, delay=1):
    """
    A basic retry decorator.
    Retries matter for automation scripts hitting real network calls because
    networks are inherently unreliable (e.g., transient timeouts, temporary server errors).
    Retrying helps prevent flaky tests caused by temporary environmental issues.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(f"Attempt {attempts}/{max_attempts} failed for {func.__name__}: {e}")
                    if attempts >= max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
