import unittest
from unittest.mock import patch, MagicMock
from unittest.mock import AsyncMock
import benchmark

class TestMockedBenchmarks(unittest.TestCase):

    @patch("benchmark.PackageFactory.get_package")
    def test_run_package_mocked(self, mock_get_package):
        # Create a mocked BenchmarkResult-like object
        mock_result = MagicMock()
        mock_result.requests_per_sec = 100.0
        mock_result.total_time = 2.0
        mock_result.avg_conn_time = 0.02
        mock_result.avg_tls_time = 0.01

        # Create mock package with run_sync and run_async
        mock_package = MagicMock()
        mock_package.run_sync.return_value = mock_result
        mock_package.run_async = AsyncMock(return_value=mock_result)

        mock_get_package.return_value = mock_package

        # Run run_package for both async and sync clients
        import asyncio
        aio_result = asyncio.run(benchmark.run_package("aiohttp"))
        sync_result = asyncio.run(benchmark.run_package("requests"))

        self.assertEqual(aio_result.requests_per_sec, 100.0)
        self.assertEqual(sync_result.avg_tls_time, 0.01)

    @patch("benchmark.run_package")
    @patch("benchmark.PackageFactory.get_package")
    def test_run_benchmarks_mocked(self, mock_get_package, mock_run_package):
        # Setup mock result
        mock_result = MagicMock()
        mock_result.requests_per_sec = 99.0
        mock_result.total_time = 1.5
        mock_result.avg_conn_time = 0.015
        mock_result.avg_tls_time = 0.005

        mock_run_package.return_value = mock_result

        # Patch the range to only loop twice
        with patch("benchmark.range", return_value=range(2)):
            benchmark.run_benchmarks()

        # Ensure mock was used
        self.assertTrue(mock_run_package.called)


if __name__ == "__main__":
    unittest.main()
