#!/usr/bin/env python3
"""
Load testing script for Question 8 (HPA testing)
Sends multiple requests to trigger autoscaling
"""

import requests
import json
import time
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


# ==================== CONFIGURATION ====================
# Modify these values as needed

DEFAULT_URL = "http://localhost:9696/predict"
DEFAULT_REQUESTS = 1000
DEFAULT_WORKERS = 10  # Number of concurrent threads
DEFAULT_DELAY = 0.01  # Delay between requests (seconds)

DEFAULT_CLIENT_DATA = {
    "job": "management",
    "duration": 400,
    "poutcome": "success"
}

# ==================== END CONFIGURATION ====================


class LoadTester:
    def __init__(self, url, client_data, num_requests, workers, delay):
        self.url = url
        self.client_data = client_data
        self.num_requests = num_requests
        self.workers = workers
        self.delay = delay

        self.successful = 0
        self.failed = 0
        self.total_time = 0
        self.errors = {}

    def make_request(self, request_id):
        """Make a single prediction request"""
        try:
            start_time = time.time()
            response = requests.post(
                self.url,
                json=self.client_data,
                timeout=10
            )
            elapsed = time.time() - start_time

            if response.status_code == 200:
                return {
                    'success': True,
                    'time': elapsed,
                    'id': request_id
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'time': elapsed,
                    'id': request_id
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'time': 0,
                'id': request_id
            }

    def run(self):
        """Run the load test"""
        print("=" * 70)
        print("🚀 LOAD TEST STARTING")
        print("=" * 70)
        print(f"Target URL: {self.url}")
        print(f"Total Requests: {self.num_requests}")
        print(f"Concurrent Workers: {self.workers}")
        print(f"Delay between batches: {self.delay}s")
        print(f"Test data: {json.dumps(self.client_data, indent=2)}")
        print("=" * 70)
        print()

        start_time = datetime.now()

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = []

            for i in range(self.num_requests):
                future = executor.submit(self.make_request, i)
                futures.append(future)
                time.sleep(self.delay)

                # Progress update every 100 requests
                if (i + 1) % 100 == 0:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    rate = (i + 1) / elapsed if elapsed > 0 else 0
                    print(f"Progress: {i + 1}/{self.num_requests} requests sent "
                          f"({rate:.1f} req/s)")

            # Collect results
            print("\nWaiting for all requests to complete...\n")

            for future in as_completed(futures):
                result = future.result()

                if result['success']:
                    self.successful += 1
                    self.total_time += result['time']
                else:
                    self.failed += 1
                    error = result['error']
                    self.errors[error] = self.errors.get(error, 0) + 1

        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()

        # Print results
        self.print_results(total_duration)

    def print_results(self, total_duration):
        """Print test results"""
        print("\n" + "=" * 70)
        print("📊 LOAD TEST RESULTS")
        print("=" * 70)
        print(f"Total Duration: {total_duration:.2f} seconds")
        print(f"Total Requests: {self.num_requests}")
        print(f"Successful: {self.successful} ({self.successful/self.num_requests*100:.1f}%)")
        print(f"Failed: {self.failed} ({self.failed/self.num_requests*100:.1f}%)")

        if self.successful > 0:
            avg_time = self.total_time / self.successful
            throughput = self.num_requests / total_duration
            print(f"\nAverage Response Time: {avg_time:.3f} seconds")
            print(f"Throughput: {throughput:.2f} requests/second")

        if self.errors:
            print("\nErrors:")
            for error, count in sorted(self.errors.items(),
                                      key=lambda x: x[1],
                                      reverse=True):
                print(f"  - {error}: {count} times")

        print("=" * 70)

        # Reminder for Question 8
        print("\n" + "=" * 70)
        print("🎯 FOR QUESTION 8:")
        print("=" * 70)
        print("Now check the number of pods that were created:")
        print("  kubectl get pods")
        print("  kubectl get hpa")
        print("\nThe maximum number of pods is your answer for Question 8!")
        print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Load test the Bank Marketing prediction service'
    )
    parser.add_argument(
        '--url',
        type=str,
        default=DEFAULT_URL,
        help=f'Prediction endpoint URL (default: {DEFAULT_URL})'
    )
    parser.add_argument(
        '--requests',
        type=int,
        default=DEFAULT_REQUESTS,
        help=f'Number of requests to send (default: {DEFAULT_REQUESTS})'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=DEFAULT_WORKERS,
        help=f'Number of concurrent workers (default: {DEFAULT_WORKERS})'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=DEFAULT_DELAY,
        help=f'Delay between requests in seconds (default: {DEFAULT_DELAY})'
    )
    parser.add_argument(
        '--json',
        type=str,
        help='Custom JSON data as string'
    )

    args = parser.parse_args()

    # Prepare client data
    if args.json:
        try:
            client_data = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"❌ ERROR: Invalid JSON: {e}")
            sys.exit(1)
    else:
        client_data = DEFAULT_CLIENT_DATA

    # Create and run load tester
    tester = LoadTester(
        url=args.url,
        client_data=client_data,
        num_requests=args.requests,
        workers=args.workers,
        delay=args.delay
    )

    try:
        tester.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Load test interrupted by user")
        sys.exit(1)

    sys.exit(0 if tester.failed == 0 else 1)


if __name__ == "__main__":
    main()
