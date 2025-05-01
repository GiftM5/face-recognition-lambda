import json
from Lambda_function import lambda_handler  # Import your lambda function

def test_lambda():
    # Simulate the S3 event
    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": "your-bucket-name"},
                "object": {"key": "path/to/your/image.jpg"}
            }
        }]
    }

    context = None  # Context is not required for local tests, but can be mocked if needed

    # Call the lambda_handler function with the simulated event
    response = lambda_handler(event, context)

    # Print the response to see if it works
    print("Lambda Response:", response)

# Run the test
test_lambda()
