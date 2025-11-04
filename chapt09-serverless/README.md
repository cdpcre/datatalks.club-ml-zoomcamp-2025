# Chapter 9 - Serverless Deep Learning Homework

This directory contains the solution to the ML Zoomcamp Serverless homework, which involves deploying a hair type classification model (Straight vs Curly) to AWS Lambda.

## Contents

- `homework.ipynb` - Jupyter notebook with all homework questions and solutions
- `homework_reference.md` - Original homework assignment
- `q1_convert_model.py` - Script for Question 1: Convert Keras to TF-Lite
- `q2_model_info.py` - Script for Question 2: Get model output index
- `q3_preprocess_image.py` - Script for Question 3: Image preprocessing
- `q4_inference.py` - Script for Question 4: Model inference
- `lambda_function.py` - AWS Lambda handler for Question 6
- `Dockerfile` - Docker image definition for Question 6
- `test_lambda_local.py` - Local testing script for Lambda function
- `requirements.txt` - Python dependencies

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Download the Model

The model will be downloaded automatically when running the scripts, or you can download it manually:

```bash
wget https://github.com/alexeygrigorev/large-datasets/releases/download/hairstyle/model_2024_hairstyle.keras
```

## Running the Homework

### Option 1: Jupyter Notebook (Recommended for Exploration)

```bash
jupyter notebook homework.ipynb
```

Run all cells to see the complete homework solution. The notebook is designed to be easily modifiable for future updates.

### Option 2: Python Scripts (Modular Approach)

Run each question individually:

```bash
# Question 1: Convert model to TF-Lite
python q1_convert_model.py

# Question 2: Get model output index
python q2_model_info.py

# Question 3: Preprocess image and check first pixel
python q3_preprocess_image.py

# Question 4: Run inference
python q4_inference.py
```

## Questions Overview

### Question 1: Model Conversion
Convert the Keras model to TF-Lite format and report the file size.

**Options:** 27 Mb, 43 Mb, 77 Mb, 127 Mb

### Question 2: Output Index
Identify the output tensor index for the TF-Lite model.

**Options:** 3, 7, 13, 24

### Question 3: First Pixel Value
After preprocessing the test image, determine the R channel value of the first pixel.

**Test Image:** https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg

**Options:** 0.24, 0.44, 0.64, 0.84

### Question 4: Model Output
Apply the model to the preprocessed image and report the output value.

**Options:** 0.293, 0.493, 0.693, 0.893

### Question 5: Docker Base Image Size
Pull the Docker base image and check its size.

**Base Image:** `agrigorev/model-2024-hairstyle:v3`

```bash
docker pull agrigorev/model-2024-hairstyle:v3
docker images agrigorev/model-2024-hairstyle:v3
```

**Options:** 182 Mb, 382 Mb, 582 Mb, 782 Mb

### Question 6: Lambda Container
Build and test the Lambda container with TF-Lite runtime.

**Steps:**

1. Build the Docker image:
```bash
docker build -t hairstyle-lambda .
```

2. Run the container locally:
```bash
docker run -p 8080:8080 hairstyle-lambda
```

3. Test with curl (in another terminal):
```bash
curl -X POST http://localhost:8080/2015-03-31/functions/function/invocations \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"}'
```

**Options:** 0.229, 0.429, 0.629, 0.829

## Docker Deployment

### Local Testing

The `test_lambda_local.py` script allows testing the Lambda function without Docker (requires TF-Lite runtime installed):

```bash
python test_lambda_local.py
```

### Building and Running with Docker

```bash
# Build the image
docker build -t hairstyle-lambda .

# Run locally
docker run -p 8080:8080 hairstyle-lambda

# Test (in another terminal)
curl -X POST http://localhost:8080/2015-03-31/functions/function/invocations \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"}'
```

### Deploying to AWS Lambda (Optional)

1. **Push to ECR:**
```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repository
aws ecr create-repository --repository-name hairstyle-lambda --region us-east-1

# Tag image
docker tag hairstyle-lambda:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/hairstyle-lambda:latest

# Push image
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/hairstyle-lambda:latest
```

2. **Create Lambda Function:**
- Go to AWS Lambda Console
- Create function from container image
- Select the ECR image
- Set memory to at least 512 MB
- Set timeout to at least 30 seconds

3. **Test Lambda:**
Use the test event:
```json
{
  "url": "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
}
```

4. **Expose with API Gateway (Optional):**
- Create REST API
- Create resource and method (POST)
- Connect to Lambda function
- Deploy API

## Technical Details

### Model Information
- **Model Type:** Keras Sequential
- **Input Shape:** (200, 200, 3)
- **Output:** Binary classification (Straight vs Curly)
- **Preprocessing:** Resize to 200x200, rescale to [0, 1]

### Dependencies
- **Python:** 3.10
- **TensorFlow:** 2.14.0+ (for model conversion)
- **TF-Lite Runtime:** 2.14.0 (for Lambda)
- **NumPy:** 1.23.1+
- **Pillow:** Latest

### Lambda Configuration
- **Runtime:** Python 3.10 (AWS Lambda base image)
- **Memory:** 512 MB minimum
- **Timeout:** 30 seconds minimum
- **Handler:** `lambda_function.lambda_handler`

## Project Structure

```
chapt09-serverless/
├── README.md                    # This file
├── homework.ipynb              # Complete homework notebook
├── homework_reference.md       # Original assignment
├── requirements.txt            # Python dependencies
├── q1_convert_model.py         # Question 1 script
├── q2_model_info.py           # Question 2 script
├── q3_preprocess_image.py     # Question 3 script
├── q4_inference.py            # Question 4 script
├── lambda_function.py         # Lambda handler
├── Dockerfile                 # Docker image definition
└── test_lambda_local.py       # Local Lambda test
```

## Notes

- The base Docker image (`agrigorev/model-2024-hairstyle:v3`) already contains the model file `model_2024_hairstyle_v2.tflite`
- TensorFlow 2.14.0 is required due to compatibility with Python 3.10 in AWS Lambda
- The model uses the same preprocessing as homework 8: resize to 200x200 and rescale to [0, 1]
- For production, consider adding error handling, logging, and monitoring

## Troubleshooting

### Model Download Issues
If the model download fails, try downloading manually:
```bash
wget https://github.com/alexeygrigorev/large-datasets/releases/download/hairstyle/model_2024_hairstyle.keras
```

### Docker Build Issues
Make sure Docker is installed and running:
```bash
docker --version
docker ps
```

### Lambda Test Issues
Check that the container is running:
```bash
docker ps
docker logs <container-id>
```

## References

- [ML Zoomcamp Course](https://github.com/DataTalksClub/machine-learning-zoomcamp)
- [Original Homework](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/master/cohorts/2025/09-serverless/homework.md)
- [AWS Lambda Container Images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- [TensorFlow Lite](https://www.tensorflow.org/lite)
