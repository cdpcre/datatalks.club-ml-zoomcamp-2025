#!/usr/bin/env python3
"""
Test script for Bank Marketing model prediction
Used for Question 1 and Question 6 of the Kubernetes homework
"""

import requests
import json
import sys
import argparse


# ==================== CONFIGURATION ====================
# Modify these values as needed

DEFAULT_URL = "http://localhost:9696/predict"

DEFAULT_CLIENT_DATA = {
    "job": "management",
    "duration": 400,
    "poutcome": "success"
}

# ==================== END CONFIGURATION ====================


def test_prediction(url=DEFAULT_URL, client_data=None):
    """
    Test the prediction endpoint

    Args:
        url: URL of the prediction service
        client_data: Dictionary with client data

    Returns:
        dict: Prediction result or None if error
    """
    if client_data is None:
        client_data = DEFAULT_CLIENT_DATA

    print(f"Testing prediction endpoint: {url}")
    print(f"Client data: {json.dumps(client_data, indent=2)}\n")

    try:
        response = requests.post(url, json=client_data, timeout=10)
        response.raise_for_status()

        result = response.json()

        print("=" * 60)
        print("✅ SUCCESS - Prediction Result")
        print("=" * 60)
        print(json.dumps(result, indent=2))

        if 'subscription_probability' in result:
            prob = result['subscription_probability']
            subscription = result.get('subscription', False)

            print("\n" + "=" * 60)
            print(f"Subscription Probability: {prob:.3f}")
            print(f"Subscription Decision: {subscription}")
            print("=" * 60)

            # Show closest answer options
            print("\nClosest answer options:")
            options = [0.287, 0.530, 0.757, 0.960]
            for opt in options:
                diff = abs(prob - opt)
                marker = "👉" if diff < 0.1 else "  "
                print(f"{marker} {opt:.3f} (difference: {diff:.3f})")

        return result

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to service")
        print(f"   Make sure the service is running at {url}")
        print("\n   For local Docker testing:")
        print(f"   docker run -d -p 9696:9696 zoomcamp-model:3.11.5-hw10")
        print("\n   For Kubernetes testing:")
        print(f"   kubectl port-forward service/bank-marketing-service 9696:80")
        return None

    except requests.exceptions.Timeout:
        print(f"❌ ERROR: Request timeout after 10 seconds")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"❌ ERROR: HTTP {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        return None

    except json.JSONDecodeError:
        print(f"❌ ERROR: Invalid JSON response")
        print(f"   Response: {response.text}")
        return None

    except Exception as e:
        print(f"❌ ERROR: Unexpected error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Test Bank Marketing model prediction endpoint'
    )
    parser.add_argument(
        '--url',
        type=str,
        default=DEFAULT_URL,
        help=f'Prediction endpoint URL (default: {DEFAULT_URL})'
    )
    parser.add_argument(
        '--job',
        type=str,
        help='Client job (overrides default)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        help='Call duration in seconds (overrides default)'
    )
    parser.add_argument(
        '--poutcome',
        type=str,
        help='Previous outcome (overrides default)'
    )
    parser.add_argument(
        '--json',
        type=str,
        help='Full JSON data as string (overrides all other data options)'
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
        client_data = DEFAULT_CLIENT_DATA.copy()
        if args.job:
            client_data['job'] = args.job
        if args.duration:
            client_data['duration'] = args.duration
        if args.poutcome:
            client_data['poutcome'] = args.poutcome

    # Run test
    result = test_prediction(args.url, client_data)

    # Exit with appropriate code
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
