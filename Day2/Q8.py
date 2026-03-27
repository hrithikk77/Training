# Q8. Thread vs Sequential — IO Simulation 
# Topics: Threading, IO-bound 
# Problem Statement: 
# Create a function fetch_data(source, delay) that simulates an API call using time.sleep(delay). Run 5 calls sequentially and then using threading. Print the total execution time for each approach. 

# Input: 
# sources = [("users", 2), ("orders", 3), ("products", 1), ("reviews", 2), ("inventory", 1)] 

# Output: 
# Sequential time: ~9.0s 
# Threaded time:   ~3.0s 

# Constraints: 
# Use threading.Thread or concurrent.futures.ThreadPoolExecutor 
# Print start and end log for each source 
# Measure time using time.time() 



import time
import threading
from concurrent.futures import ThreadPoolExecutor


# Simulated API call
def fetch_data(source, delay):
    print(f"Start fetching {source}")
    time.sleep(delay)
    print(f"Finished fetching {source}")


#  Sequential Execution
def run_sequential(sources):
    start = time.time()

    for source, delay in sources:
        fetch_data(source, delay)

    end = time.time()
    print(f"\nSequential time: {round(end - start, 2)}s")


#  Threaded Execution (using ThreadPoolExecutor)
def run_threaded(sources):
    start = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        for source, delay in sources:
            executor.submit(fetch_data, source, delay)

    end = time.time()
    print(f"\nThreaded time: {round(end - start, 2)}s")



sources = [
    ("users", 2),
    ("orders", 3),
    ("products", 1),
    ("reviews", 2),
    ("inventory", 1)
]



run_sequential(sources)
print("\n" + "="*40 + "\n")
run_threaded(sources)