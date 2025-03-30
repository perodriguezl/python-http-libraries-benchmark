import asyncio
import csv
import random
import os
from datetime import datetime
from factory import PackageFactory

CSV_FILE = "benchmark_results.csv"
NUM_REQUESTS_PER_PACKAGE_RUN = 20

async def run_package(package_name):
    package = PackageFactory.get_package(package_name)
    if package_name in ["aiohttp", "httpx"]:
        return await package.run_async()
    else:
        return package.run_sync()

def run_benchmarks():
    packages = ["aiohttp", "httpx", "pycurl", "requests", "urllib3"]
    metrics = ["req_sec", "total", "conn_avg", "tls_avg"]

    fieldnames = ["start_time", "end_time", "num_requests"] + [f"{metric}_{pkg}" for metric in metrics for pkg in packages]

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for run in range(11):
            print(f"Benchmark run: {run + 1}")
            random.shuffle(packages)

            start_time = datetime.now().isoformat()

            results = {}

            for pkg_name in packages:
                result = asyncio.run(run_package(pkg_name))
                results[f"req_sec_{pkg_name}"] = f"{result.requests_per_sec:.2f}"
                results[f"total_{pkg_name}"] = f"{result.total_time:.2f}"
                results[f"conn_avg_{pkg_name}"] = f"{result.avg_conn_time:.4f}"
                results[f"tls_avg_{pkg_name}"] = f"{result.avg_tls_time:.4f}" if result.avg_tls_time is not None else "N/A"

            end_time = datetime.now().isoformat()

            if run == 0:
                continue

            results["start_time"] = start_time
            results["end_time"] = end_time
            results["num_requests"] = NUM_REQUESTS_PER_PACKAGE_RUN

            writer.writerow(results)

            print("Benchmark Results:")
            for key, value in results.items():
                print(f"{key}: {value}")
            print("-" * 40)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    run_benchmarks()