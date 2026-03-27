# Q9. Race Condition — Shared Counter Fix 
# Topics: Race Condition, Thread Safety 
# Problem Statement: 
# Create a shared counter starting at 0. Spawn 10 threads, each incrementing the counter 1000 times. First demonstrate the race condition (incorrect final value), then fix it using threading.Lock. 

# Input: 
# # No explicit input — internal simulation 

# Output: 
# Without lock: 8743 (varies, often incorrect) 
# With lock:  10000 (always correct) 

# Constraints: 
# Run the unfixed version multiple times to show inconsistency 
# Use threading.Lock to fix 
# Do NOT use global keyword; pass lock and counter via a mutable container or class 










# import threading


# class Counter:
#     def __init__(self):
#         self.value = 0


# def increment(counter):
#     for _ in range(1000):
#         counter.value += 1   # NOT thread-safe


# def run_without_lock():
#     counter = Counter()
#     threads = []

#     for _ in range(10):
#         t = threading.Thread(target=increment, args=(counter,))
#         threads.append(t)
#         t.start()

#     for t in threads:
#         t.join()

#     print("Without lock:", counter.value)


# # Run multiple times to show inconsistency
# for _ in range(3):
#     run_without_lock()



import threading


class Counter:
    def __init__(self):
        self.value = 0


def increment(counter, lock):
    for _ in range(1000):
        with lock:   # critical section
            counter.value += 1


def run_with_lock():
    counter = Counter()
    lock = threading.Lock()
    threads = []

    for _ in range(10):
        t = threading.Thread(target=increment, args=(counter, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("With lock:", counter.value)


run_with_lock()