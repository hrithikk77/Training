import time
import logging
import functools

# Configure logger for this file
logger = logging.getLogger("timer_logger")

def timer(func):
    """Decorator that logs the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start the clock
        
        result = func(*args, **kwargs)    # Execute the actual function
        
        end_time = time.perf_counter()    # Stop the clock
        duration = end_time - start_time
        
        # Log the result to logs/app.log
        logging.info(f"Function '{func.__name__}' executed in {duration:.4f} seconds")
        return result
        
    return wrapper