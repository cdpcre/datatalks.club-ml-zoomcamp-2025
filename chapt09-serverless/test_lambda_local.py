#!/usr/bin/env python3
"""
Script to test the Lambda function locally (without Docker).

This script simulates a Lambda invocation for testing purposes.
"""

import json


def test_lambda_function():
    """Test the lambda function locally"""
    # Import the lambda function
    from lambda_function import lambda_handler

    # Create a test event
    test_event = {
        "url": "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
    }

    print("Testing Lambda function with event:")
    print(json.dumps(test_event, indent=2))
    print("\n" + "="*50)

    # Invoke the handler
    result = lambda_handler(test_event, None)

    print("\nResult:")
    print(json.dumps(result, indent=2))

    # Extract prediction for Q6
    if result['statusCode'] == 200:
        prediction = result['body']['prediction']
        print("\n" + "="*50)
        print(f"✓ ANSWER Q6: {prediction:.3f}")
        print("="*50)


if __name__ == "__main__":
    test_lambda_function()
