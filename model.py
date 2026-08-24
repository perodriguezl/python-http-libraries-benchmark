PACKAGES = ["aiohttp", "httpx", "httpx2", "pycurl", "requests", "urllib3"]
METRICS = ["req_sec", "total", "conn_avg", "tls_avg"]
CSV_METADATA = ["start_time", "end_time", "num_requests"]


class BenchmarkResult:
    def __init__(self, requests_per_sec, total_time, avg_conn_time, avg_tls_time=None):
        self.requests_per_sec = requests_per_sec
        self.total_time = total_time
        self.avg_conn_time = avg_conn_time
        self.avg_tls_time = avg_tls_time


def csv_fieldnames():
    return CSV_METADATA + [f"{metric}_{pkg}" for metric in METRICS for pkg in PACKAGES]
