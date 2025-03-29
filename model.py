class BenchmarkResult:
    def __init__(self, requests_per_sec, total_time, avg_conn_time, avg_tls_time=None):
        self.requests_per_sec = requests_per_sec
        self.total_time = total_time
        self.avg_conn_time = avg_conn_time
        self.avg_tls_time = avg_tls_time