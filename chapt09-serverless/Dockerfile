# Dockerfile for AWS Lambda hair type classification
# Question 6: Extended Docker image with TF-Lite runtime

FROM agrigorev/model-2024-hairstyle:v3

# Install TF-Lite runtime wheel for Python 3.10
RUN pip install https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.14.0-cp310-cp310-linux_x86_64.whl

# Install Pillow for image processing
RUN pip install pillow

# Copy Lambda function code
COPY lambda_function.py .

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]
