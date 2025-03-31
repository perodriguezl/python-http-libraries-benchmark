import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("benchmark_results.csv")

# List of packages
packages = ["aiohttp", "httpx", "pycurl", "requests", "urllib3"]

# Plot configuration
metrics_info = {
    "req_sec": ("Mean Requests per Second Across Runs", "Mean Requests/sec", "mean_requests_per_second.png"),
    "total": ("Mean Total Response Time Across Runs", "Mean Total Time (s)", "mean_total_response_time.png"),
    "conn_avg": ("Mean Connection Time Across Runs", "Mean Connection Time (s)", "mean_connection_time.png"),
    "tls_avg": ("Mean TLS Handshake Time Across Runs", "Mean TLS Time (s)", "mean_tls_handshake_time.png"),
}


def plot_metric(metric_key, title, ylabel, filename):
    plt.figure(figsize=(10, 6))
    for pkg in packages:
        col_name = f"{metric_key}_{pkg}"
        series = df[col_name]
        if metric_key == "tls_avg":
            series = series[series != "N/A"]  # Remove non-numeric
        series = series.astype(float)
        mean_value = series.expanding().mean()
        sns.lineplot(x=mean_value.index, y=mean_value, label=pkg)
    plt.title(title)
    plt.xlabel("Run #")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


# Generate all plots
for metric_key, (title, ylabel, filename) in metrics_info.items():
    plot_metric(metric_key, title, ylabel, filename)

