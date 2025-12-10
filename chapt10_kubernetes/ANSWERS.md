# Chapter 10 - Kubernetes Homework Answers

Based on: https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/master/cohorts/2025/10-kubernetes/homework.md

---

## Question 1: Model Probability

**Question:** Run the model locally and get the `conversion_probability` value.

```bash
# Build the image
docker build -f Dockerfile_full -t zoomcamp-model:3.13.10-hw10 .

# Run container
docker run -it --rm -p 9696:9696 zoomcamp-model:3.13.10-hw10

# Test (in another terminal)
python q6_test.py
```

**Your Answer:** ______ (Select: 0.29, 0.49, 0.69, or 0.89)

---

## Question 2: Kind Version

**Question:** What's the version of `kind`?

```bash
kind --version
```

**Your Answer:** ______

---

## Question 3: Smallest Deployable Unit

**Question:** What's the smallest deployable computing unit in Kubernetes?

**✅ Answer: Pod**

Options: Node, Pod, Deployment, Service

---

## Question 4: Default Service Type

**Question:** What's the Type of the kubernetes service already running?

```bash
kubectl get services
```

**✅ Answer: ClusterIP**

Options: NodePort, ClusterIP, ExternalName, LoadBalancer

---

## Question 5: Load Docker Image Command

**Question:** What command to register the image with kind?

**✅ Answer: kind load docker-image**

```bash
kind load docker-image zoomcamp-model:3.13.10-hw10
```

Options: kind create cluster, kind build node-image, kind load docker-image, kubectl apply

---

## Question 6: Container Port

**Question:** What is the value for `<Port>` in the deployment?

**✅ Answer: 9696**

This is the containerPort where Flask listens.

---

## Question 7: Service Selector

**Question:** What to write instead of `<???>` in the service selector `app: <???>`?

**✅ Answer: subscription**

The selector must match the deployment's pod label.

---

## Question 8: Maximum Replicas (Optional)

**Question:** What was the maximum amount of replicas during the load test?

```bash
# Create HPA
kubectl autoscale deployment subscription --name subscription-hpa --cpu-percent=20 --min=1 --max=3

# Monitor
kubectl get hpa subscription-hpa --watch
```

**Your Answer:** ______ (Options: 1, 2, 3, 4)

Expected: 3 (max replicas configured)

---

## Quick Reference

| Q | Answer |
|---|--------|
| 1 | Run test to find probability |
| 2 | `kind --version` output |
| 3 | **Pod** |
| 4 | **ClusterIP** |
| 5 | **kind load docker-image** |
| 6 | **9696** |
| 7 | **subscription** |
| 8 | Likely **3** (max replicas) |

---

## Essential Commands

```bash
# Build & run Docker
docker build -f Dockerfile_full -t zoomcamp-model:3.13.10-hw10 .
docker run -it --rm -p 9696:9696 zoomcamp-model:3.13.10-hw10

# Create cluster
kind create cluster

# Load image
kind load docker-image zoomcamp-model:3.13.10-hw10

# Deploy
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Test service
kubectl port-forward service/subscription 9696:80

# HPA
kubectl autoscale deployment subscription --name subscription-hpa --cpu-percent=20 --min=1 --max=3
kubectl get hpa --watch
```

Submit: https://courses.datatalks.club/ml-zoomcamp-2025/homework/hw10
