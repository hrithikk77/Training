import time
from multiprocessing import Pool, cpu_count


#  CPU-heavy function
def compute_squares(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total


#  Sequential execution
def run_sequential(values):
    start = time.time()

    results = []
    for v in values:
        result = compute_squares(v)
        results.append(result)
        print(f"Result for {v}: {result}")

    end = time.time()
    print(f"\nSequential time: {round(end - start, 2)}s\n")


#  Multiprocessing execution
def run_multiprocessing(values):
    start = time.time()

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(compute_squares, values)

    for v, r in zip(values, results):
        print(f"Result for {v}: {r}")

    end = time.time()
    print(f"\nMultiprocessing time: {round(end - start, 2)}s\n")


values = [10_000_000, 20_000_000, 15_000_000, 25_000_000]

if __name__ == "__main__":
    run_sequential(values)
    print("=" * 40)
    run_multiprocessing(values)