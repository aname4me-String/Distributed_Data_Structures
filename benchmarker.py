import time
import csv

def run_benchmark(system_name, worker_counts, run_function):
    results = []
    for workers in worker_counts:
        print(f"\n[{system_name}] Starts with {workers} Workers")

        start = time.perf_counter()
        prime_count = run_function(workers)
        elapsed = time.perf_counter() - start

        results.append({
            "system": system_name,
            "workers": workers,
            "time_seconds": round(elapsed, 3),
            "primes_found": prime_count
        })
        print(f"  → {elapsed:.3f}s | {prime_count} Primes found)")

    return results


def save_results(results, filename="benchmark_results.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f,
                                fieldnames=["system", "workers", "time_seconds", "primes_found"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\nErgebnisse gespeichert in {filename}")