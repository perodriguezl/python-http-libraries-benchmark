# 🐍 python-http-libraries-benchmark

This project benchmarks popular Python HTTP libraries to compare their performance across core networking metrics. The goal is to offer insights on how each library performs under real-world request loads.

---

## 📦 HTTP Libraries Benchmarked
This benchmark includes five widely-used Python HTTP libraries—requests, urllib3, httpx, aiohttp, and pycurl—chosen for their relevance, diversity, and real-world usage. requests is the most popular and beginner-friendly library, while urllib3 offers low-level control and powers requests internally. httpx and aiohttp provide modern asynchronous support for high-concurrency applications. Finally, pycurl wraps the high-performance C-based libcurl library, often used in system-level or legacy environments. Together, they represent a broad spectrum of HTTP client capabilities in Python, from ease of use to advanced performance tuning.

- [`aiohttp`](https://docs.aiohttp.org/)
- [`httpx`](https://www.python-httpx.org/)
- [`requests`](https://docs.python-requests.org/)
- [`urllib3`](https://urllib3.readthedocs.io/)
- [`pycurl`](http://pycurl.io/)

---

## 📊 Metrics Captured

Each library is evaluated using the following metrics:

- **Requests per Second (`req/sec`)**: Measures throughput. A higher number indicates the library handles more traffic efficiently.
- **Total Time**: Measures how long the library takes to complete a full batch of requests.
- **Average Connection Time**: Indicates the average time spent on establishing connections for each request.

These metrics are chosen to reflect practical usage in applications such as REST APIs, microservices, and integrations.

---

## 🎯 Benchmarking Strategy

To ensure fair and unbiased comparisons:

- Each run sends a fixed number of requests (`NUM_REQUESTS = 100`) to a local HTTP server (`http://localhost` by default).
- The script performs **101 complete benchmark runs**, where the first is used as warm-up and excluded from the CSV output.
- **Randomized Execution Order**: For every run, the order in which HTTP libraries are tested is randomized. This prevents any one library from benefiting from system or network caching effects due to consistent positioning.

---

## 📁 Output

Benchmark results are stored in `benchmark_results.csv`. Each row represents one full benchmarking round and includes:

- Start and end timestamps
- Requests per second, total duration, and average connection time for each library
- Number of requests executed

---

## ▶️ How to Run

1. **Install requirements:**

```bash
pip install -r requirements.txt
```

2. **Start a local HTTP server** (in a separate terminal):

```bash
python -m http.server 8080
```

3. **Run the benchmark:**

```bash
BENCHMARK_URL=http://localhost:8080 python benchmark.py
```

4. **Generate charts:**

```bash
python benchmark_analytics.py
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BENCHMARK_URL` | `http://localhost` | Target URL for requests |
| `BENCHMARK_RUNS` | `101` | Total number of runs (first is warm-up) |

Example with custom values:
```bash
BENCHMARK_URL=http://localhost:8080 BENCHMARK_RUNS=11 python benchmark.py
```

---

## ⚙️ CI

A GitHub Actions workflow runs the benchmark automatically every Sunday and commits updated results and charts back to the repository. It can also be triggered manually via the **Actions** tab, with optional inputs for Python version and number of runs.

## Results

### Environment:
OS: Windows 11 Home

Processor: Intel(R) Core(TM) i5-10400 CPU @ 2.90GHz   2.90 GHz

RAM: 12.0 GB

Location Type: Localhost


![Mean Connection Time](mean_connection_time.png)
![Mean Req/Sec ](mean_requests_per_second.png)
![Mean TLS handshake time](mean_tls_handshake_time.png)
![Mean Total Response times](mean_total_response_time.png)