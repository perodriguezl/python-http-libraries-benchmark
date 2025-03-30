import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("benchmark_results.csv")

# List of packages
packages = ["aiohttp", "httpx", "pycurl", "requests", "urllib3"]

# --- Plot 1: Requests per Second ---
plt.figure(figsize=(10, 6))
for pkg in packages:
    series = df[f"req_sec_{pkg}"].astype(float)
    mean_value = series.expanding().mean()
    sns.lineplot(x=mean_value.index, y=mean_value, label=pkg)
plt.title("Mean Requests per Second Across Runs")
plt.xlabel("Run #")
plt.ylabel("Mean Requests/sec")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot 2: Total Time ---
plt.figure(figsize=(10, 6))
for pkg in packages:
    series = df[f"total_{pkg}"].astype(float)
    mean_value = series.expanding().mean()
    sns.lineplot(x=mean_value.index, y=mean_value, label=pkg)
plt.title("Mean Total Response Time Across Runs")
plt.xlabel("Run #")
plt.ylabel("Mean Total Time (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot 3: Mean Connection Time ---
plt.figure(figsize=(10, 6))
for pkg in packages:
    series = df[f"conn_Mean_{pkg}"].astype(float)
    mean_value = series.expanding().mean()
    sns.lineplot(x=mean_value.index, y=mean_value, label=pkg)
plt.title("Mean Connection Time Across Runs")
plt.xlabel("Run #")
plt.ylabel("Mean Connection Time (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot 4: Mean TLS Time (exclude N/A) ---
plt.figure(figsize=(10, 6))
for pkg in packages:
    tls_col = df[f"tls_Mean_{pkg}"]
    tls_filtered = tls_col[tls_col != "N/A"].astype(float)
    mean_value = tls_filtered.expanding().mean()
    sns.lineplot(x=mean_value.index, y=mean_value, label=pkg)
plt.title("Mean TLS Handshake Time Across Runs")
plt.xlabel("Run #")
plt.ylabel("Mean TLS Time (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
