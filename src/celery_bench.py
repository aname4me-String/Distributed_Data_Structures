from celery import group
from tasks import app, find_primes_task
from benchmarker import run_benchmark, save_results


def run_celery(num_workers):
    chunk = 100_000_000 // num_workers
    task_group = group(
        find_primes_task.s(i, i + chunk)
        for i in range(0, 100_000_000, chunk)
    )
    results = task_group.apply_async().get(timeout=3600)
    return sum(len(r) for r in results)


results = run_benchmark("Celery", [1, 2, 4, 8], run_celery)
save_results(results, "celery_100m_results.csv")