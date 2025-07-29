import sys
import logging
import json
import time
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer
import pytest

# Prometheus imports
from prometheus_client import start_http_server, Counter, Histogram, generate_latest

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('fibonacci_requests_total', 'Total Fibonacci requests')
REQUEST_LATENCY = Histogram(
    'fibonacci_request_latency_seconds', 'Fibonacci request latency in seconds')
REQUEST_ERRORS = Counter('fibonacci_request_errors_total',
                         'Total Fibonacci request errors')


def fibonacci(n: int):
    """Return the first `n` Fibonacci numbers."""

    if n < 0:
        raise ValueError("n must be non-negative")

    # Limit to prevent excessive memory usage and computation time
    if n > 1000:
        raise ValueError("n must be <= 1000 to prevent excessive computation")

    if n == 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    # Generate Fibonacci sequence efficiently
    fibs = [0, 1]
    for i in range(2, n):
        fibs.append(fibs[i-1] + fibs[i-2])

    return fibs


class GetFibs(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"Received GET request: path={self.path}")

        # Prometheus metrics endpoint
        if self.path.startswith('/metrics'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4')
            self.end_headers()
            self.wfile.write(generate_latest())
            return

        start_time = time.time()
        REQUEST_COUNT.inc()

        query = urlparse(self.path).query
        params = parse_qs(query)

        if "n" not in params:
            logger.warning("Missing 'n' parameter")
            REQUEST_ERRORS.inc()
            self.send_response(422)
            self.end_headers()
            self.wfile.write(b"Missing 'n' parameter")
            return

        try:
            key = int(params["n"][0])
            logger.info(f"Parsed n={key}")
        except (IndexError, ValueError):
            logger.warning(f"Invalid 'n' parameter: {params.get('n')}")
            REQUEST_ERRORS.inc()
            self.send_response(422)
            self.end_headers()
            self.wfile.write(b"Invalid 'n' parameter")
            return

        try:
            nums = fibonacci(key)
            logger.info(f"Generated Fibonacci sequence of length={len(nums)}")
        except Exception as e:
            logger.error(f"Error generating Fibonacci sequence: {e}")
            REQUEST_ERRORS.inc()
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal server error")
            return

        str_nums = [str(n) for n in nums]
        final_nums = ", ".join(str_nums)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(final_nums, "UTF-8"))
        logger.info(f"Response sent: {final_nums}")

        REQUEST_LATENCY.observe(time.time() - start_time)
        return


if __name__ == "__main__":
    # Start Prometheus metrics server on port 8001 (recommended for production)
    start_http_server(8001)

    server_address = ("0.0.0.0", 8000)
    httpd = HTTPServer(server_address, GetFibs)
    logger.info("Starting server on port 8000...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
