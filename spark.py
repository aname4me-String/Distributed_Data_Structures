from pyspark import SparkContext, SparkConf
from benchmarker import run_benchmark, save_results


def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))


def find_primes(range_tuple):
    start, end = range_tuple
    return [n for n in range(start, end) if is_prime(n)]


def run_spark(num_workers):
    conf = SparkConf() \
        .setAppName("Benchmark") \
        .set("spark.executor.instances", str(num_workers)) \
        .set("spark.executor.cores", "1")

    sc = SparkContext(conf=conf)

    ranges = [(i, i + 100_000) for i in range(0, 1_000_000, 100_000)]
    rdd = sc.parallelize(ranges, numSlices=num_workers)
    count = rdd.flatMap(find_primes).count()

    sc.stop()
    return count


results = run_benchmark("Spark", [1, 2, 4, 8], run_spark)
save_results(results, "spark_results.csv")