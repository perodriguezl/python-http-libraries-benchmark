# factory.py
import asyncio
import time
import requests
import httpx
import aiohttp
import urllib3
import pycurl
from io import BytesIO
from model import BenchmarkResult

TEST_URL = "https://postman-echo.com/get"
NUM_REQUESTS_PER_PACKAGE_RUN = 50
CONCURRENT_REQUESTS = 10

class Package:
    async def run_async(self):
        pass

    def run_sync(self):
        pass

class AiohttpPackage(Package):
    async def run_async(self):
        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
        conn_times = []

        async def fetch(session, url):
            async with semaphore:
                start_conn = time.time()
                async with session.get(url) as response:
                    await response.read()
                    conn_time = time.time() - start_conn
                    conn_times.append(conn_time)

        async with aiohttp.ClientSession() as session:
            start_total = time.time()
            tasks = [fetch(session, TEST_URL) for _ in range(NUM_REQUESTS_PER_PACKAGE_RUN)]
            await asyncio.gather(*tasks)
            duration = time.time() - start_total

        return BenchmarkResult(NUM_REQUESTS_PER_PACKAGE_RUN / duration, duration, sum(conn_times) / NUM_REQUESTS_PER_PACKAGE_RUN, avg_tls_time=None)

class HttpxPackage(Package):
    async def run_async(self):
        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
        conn_times = []

        async def fetch(client, url):
            async with semaphore:
                start_conn = time.time()
                response = await client.get(url)
                conn_time = time.time() - start_conn
                conn_times.append(conn_time)

        async with httpx.AsyncClient() as client:
            start_total = time.time()
            tasks = [fetch(client, TEST_URL) for _ in range(NUM_REQUESTS_PER_PACKAGE_RUN)]
            await asyncio.gather(*tasks)
            duration = time.time() - start_total

        return BenchmarkResult(NUM_REQUESTS_PER_PACKAGE_RUN / duration, duration, sum(conn_times) / NUM_REQUESTS_PER_PACKAGE_RUN, avg_tls_time=None)

class PycurlPackage(Package):
    def run_sync(self):
        total_conn_time = 0
        total_tls_time = 0

        start_total = time.time()
        for _ in range(NUM_REQUESTS_PER_PACKAGE_RUN):
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, TEST_URL)
            c.setopt(c.WRITEDATA, buffer)

            start_conn = time.time()
            c.perform()
            conn_time = time.time() - start_conn
            total_conn_time += conn_time

            tls_time = c.getinfo(pycurl.APPCONNECT_TIME)
            total_tls_time += tls_time
            c.close()

        duration = time.time() - start_total

        return BenchmarkResult(NUM_REQUESTS_PER_PACKAGE_RUN / duration, duration, total_conn_time / NUM_REQUESTS_PER_PACKAGE_RUN, total_tls_time / NUM_REQUESTS_PER_PACKAGE_RUN)

class RequestsPackage(Package):
    def run_sync(self):
        total_conn_time = 0
        total_tls_time = 0

        start_total = time.time()
        for _ in range(NUM_REQUESTS_PER_PACKAGE_RUN):
            start_conn = time.time()
            response = requests.get(TEST_URL, stream=True, timeout=(2.0, 5.0))
            conn_time = time.time() - start_conn
            total_conn_time += conn_time
            total_tls_time += response.elapsed.total_seconds()

        duration = time.time() - start_total

        return BenchmarkResult(NUM_REQUESTS_PER_PACKAGE_RUN / duration, duration, total_conn_time / NUM_REQUESTS_PER_PACKAGE_RUN, total_tls_time / NUM_REQUESTS_PER_PACKAGE_RUN)

class Urllib3Package(Package):
    def run_sync(self):
        http = urllib3.PoolManager()
        total_conn_time = 0

        start_total = time.time()
        for _ in range(NUM_REQUESTS_PER_PACKAGE_RUN):
            start_conn = time.time()
            response = http.request('GET', TEST_URL, preload_content=False, timeout=urllib3.Timeout(connect=2.0, read=5.0))
            conn_time = time.time() - start_conn
            total_conn_time += conn_time

        duration = time.time() - start_total

        return BenchmarkResult(NUM_REQUESTS_PER_PACKAGE_RUN / duration, duration, total_conn_time / NUM_REQUESTS_PER_PACKAGE_RUN, avg_tls_time=None)

class PackageFactory:
    @staticmethod
    def get_package(package_name):
        if package_name == "aiohttp":
            return AiohttpPackage()
        elif package_name == "httpx":
            return HttpxPackage()
        elif package_name == "pycurl":
            return PycurlPackage()
        elif package_name == "requests":
            return RequestsPackage()
        elif package_name == "urllib3":
            return Urllib3Package()
