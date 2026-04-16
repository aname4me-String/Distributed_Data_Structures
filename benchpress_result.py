import csv
import glob

all_results = []
for file in glob.glob("*_results.csv"):
    with open(file) as f:
        all_results.extend(csv.DictReader(f))

baseline = {}
for row in all_results:
    if int(row["workers"]) == 1:
        baseline[row["system"]] = float(row["time_seconds"])

print(f"\n{'System':<10} {'Workers':<10} {'Zeit (s)':<12} {'Speedup':<10}")
print("-" * 45)
for row in sorted(all_results, key=lambda x: (x["system"], int(x["workers"]))):
    base = baseline[row["system"]]
    speedup = base / float(row["time_seconds"])
    print(f"{row['system']:<10} {row['workers']:<10} "
          f"{row['time_seconds']:<12} {speedup:.2f}x")