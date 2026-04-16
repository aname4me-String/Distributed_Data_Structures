import ray
from benchmarker import run_benchmark, save_results


@ray.remote
def find_primes_task(start, end):
    return [n for n in range(start, end)
            if n >= 2 and all(n % i != 0
                              for i in range(2, int(n ** 0.5) + 1))]


def run_ray(num_workers):
    ray.init(num_cpus=num_workers, ignore_reinit_error=True)

    chunk = 1_000_000 // num_workers
    futures = [
        find_primes_task.remote(i, i + chunk)
        for i in range(0, 1_000_000, chunk)
    ]
    results = ray.get(futures)
    ray.shutdown()
    return sum(len(r) for r in results)


results = run_benchmark("Ray", [1, 2, 4, 8], run_ray)
save_results(results, "ray_results.csv")