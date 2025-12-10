# Serverless Homework 2025 Answers

## Question 1
**Answer:** `output`

## Question 2
**Answer:** `200x200`

## Question 3
**Answer:** `-1.073`

## Question 4
**Answer:** `0.09`

## Question 5
**Answer:** `608 Mb`

Commands used:
```bash
docker pull agrigorev/model-2025-hairstyle:v1
docker images | grep agrigorev/model-2025-hairstyle
```

## Question 6
**Answer:** `-0.10`

Commands used:
```bash
docker build -t hairstyle-model .
docker run -it --rm -p 8080:8080 hairstyle-model
python test_lambda_local.py
```
