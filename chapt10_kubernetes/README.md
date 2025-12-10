# Chapter 10 - Kubernetes Homework

This directory contains all resources needed to complete the Machine Learning Zoomcamp Chapter 10 homework on Kubernetes deployment.

## 📁 Directory Structure

```
chapt10_kubernetes/
├── README.md                              # This file
├── chapt10_kubernetes_homework.ipynb      # Interactive Jupyter notebook
├── config.yaml                            # Centralized configuration
├── test_prediction.py                     # Test script for Q1 and Q6
├── load_test.py                           # Load testing script for Q8
├── deployment.yaml                        # Kubernetes Deployment
├── service.yaml                           # Kubernetes Service
├── hpa.yaml                               # Horizontal Pod Autoscaler
├── setup_cluster.sh                       # Automated cluster setup
├── deploy_all.sh                          # Deploy all resources
└── cleanup.sh                             # Cleanup resources
```

## 🎯 Homework Overview

**Model:** Bank Marketing Prediction
**Objective:** Deploy an ML model to Kubernetes using Docker and kind
**Topics Covered:**
- Docker containerization
- Kubernetes deployments and services
- Resource management
- Horizontal Pod Autoscaling
- Load balancing

## 📋 Prerequisites

### Required Software

1. **Docker** - Container runtime
   ```bash
   docker --version
   ```
   Installation: https://docs.docker.com/get-docker/

2. **kubectl** - Kubernetes CLI
   ```bash
   kubectl version --client
   ```
   Installation: https://kubernetes.io/docs/tasks/tools/

3. **kind** - Kubernetes in Docker
   ```bash
   kind --version
   ```
   Installation: https://kind.sigs.k8s.io/docs/user/quick-start/#installation

4. **Python 3.x** - For testing scripts
   ```bash
   python --version
   pip install requests
   ```

5. **Jupyter** (Optional) - For interactive notebook
   ```bash
   pip install jupyter
   ```

## 🚀 Quick Start

### Option 1: Using Automation Scripts (Recommended)

```bash
# 1. Setup cluster and load image
./setup_cluster.sh ml-zoomcamp-cluster

# 2. Deploy all resources (without HPA)
./deploy_all.sh

# 3. Deploy with HPA for Question 8
./deploy_all.sh --with-hpa

# 4. In a separate terminal, start port forwarding
kubectl port-forward service/bank-marketing-service 9696:80

# 5. Test the deployment
python test_prediction.py

# 6. Run load test (if HPA is enabled)
python load_test.py --requests 1000

# 7. Cleanup when done
./cleanup.sh                    # Keep cluster
./cleanup.sh --delete-cluster   # Remove everything
```

### Option 2: Using Jupyter Notebook (Interactive)

```bash
# Start Jupyter
jupyter notebook chapt10_kubernetes_homework.ipynb

# Follow the notebook cells step by step
# All configuration is at the top and easily modifiable
```

### Option 3: Manual Setup

```bash
# 1. Pull/build Docker image
docker pull svizor/zoomcamp-model:3.11.5-hw10
docker tag svizor/zoomcamp-model:3.11.5-hw10 zoomcamp-model:3.11.5-hw10

# 2. Create kind cluster
kind create cluster --name ml-zoomcamp-cluster

# 3. Load image into cluster
kind load docker-image zoomcamp-model:3.11.5-hw10 --name ml-zoomcamp-cluster

# 4. Install metrics-server (for HPA)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl patch deployment metrics-server -n kube-system --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'

# 5. Deploy resources
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml  # Optional, for Q8

# 6. Port forward
kubectl port-forward service/bank-marketing-service 9696:80

# 7. Test
python test_prediction.py
```

## 📝 Homework Questions

### Question 1: Local Docker Testing

**What is the probability value returned by the model?**

```bash
# Method 1: Using script
python test_prediction.py

# Method 2: Using curl
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{"job": "management", "duration": 400, "poutcome": "success"}'

# Method 3: In notebook
# Run the "Question 1" section
```

**Expected Output:** A probability value between 0 and 1
**Answer Options:** 0.287, 0.530, 0.757, 0.960

---

### Question 2: Kind Version

**What is your installed kind version?**

```bash
kind --version
```

**Expected Output:** `kind v0.x.x go1.x.x linux/amd64` (or similar)

---

### Question 3: Kubernetes Concepts

**What is the smallest deployable unit in Kubernetes?**

**Answer Options:**
- Node
- **Pod** ✅
- Deployment
- Service

**Explanation:** A Pod is a group of one or more containers and is the atomic unit of scheduling in Kubernetes.

---

### Question 4: Service Types

**What service type is running after cluster creation?**

```bash
kubectl get services --all-namespaces
```

Look at the `TYPE` column for the `kubernetes` service in the `default` namespace.

**Answer Options:**
- NodePort
- **ClusterIP** ✅
- ExternalName
- LoadBalancer

---

### Question 5: Load Docker Image

**What command loads a Docker image into kind?**

```bash
kind load docker-image zoomcamp-model:3.11.5-hw10 --name ml-zoomcamp-cluster
```

**Answer Options:** Look for `kind load docker-image`

---

### Question 6: Deployment Configuration

**What is the containerPort in the deployment?**

```bash
# Check the deployment
kubectl describe deployment bank-marketing-deployment | grep -i port

# Or view the YAML
cat deployment.yaml | grep containerPort
```

**Answer:** Found in `deployment.yaml` under `spec.template.spec.containers[0].ports[0].containerPort`
**Expected Value:** `9696`

---

### Question 7: Service Selector

**What replaces `<???>` in the service selector?**

```bash
# Check the service
kubectl describe service bank-marketing-service | grep -i selector

# Or view the YAML
cat service.yaml | grep -A 2 selector
```

**Answer:** Found in `service.yaml` under `spec.selector.app`
**Expected Value:** `bank-marketing`

---

### Question 8: Horizontal Pod Autoscaler (Optional)

**What is the maximum number of replicas during load testing?**

```bash
# Terminal 1: Port forward
kubectl port-forward service/bank-marketing-service 9696:80

# Terminal 2: Run load test
python load_test.py --requests 1000 --workers 10

# Terminal 3: Monitor
kubectl get hpa -w
kubectl get pods -w

# Count the maximum number of pods
kubectl get pods | grep bank-marketing | wc -l
```

**Answer Options:** 1, 2, 3, 4

**Configuration:**
- Min Replicas: 1
- Max Replicas: 3
- CPU Threshold: 20%

---

## 🔧 Configuration

All configuration is centralized and easy to modify:

### In Jupyter Notebook
Edit the "Configuration Section" at the top of `chapt10_kubernetes_homework.ipynb`

### In Python Scripts
Edit the constants at the top of each script:
- `test_prediction.py` - Test data and URL
- `load_test.py` - Load test parameters

### In YAML Files
Each YAML file has extensive comments explaining all configuration options:
- `deployment.yaml` - Image, ports, resources
- `service.yaml` - Service type, ports, selectors
- `hpa.yaml` - Scaling parameters

### In Shell Scripts
Edit variables at the top of each script:
- `setup_cluster.sh` - Cluster name, image name
- `deploy_all.sh` - Resource names
- `cleanup.sh` - Cleanup options

## 🛠️ Useful Commands

### Cluster Management
```bash
# List clusters
kind get clusters

# View cluster info
kubectl cluster-info

# Check cluster context
kubectl config current-context
```

### Resource Management
```bash
# View all resources
kubectl get all

# View specific resources
kubectl get deployments
kubectl get services
kubectl get pods
kubectl get hpa

# Describe resource (detailed info)
kubectl describe deployment bank-marketing-deployment
kubectl describe service bank-marketing-service
kubectl describe pod <pod-name>

# View logs
kubectl logs deployment/bank-marketing-deployment
kubectl logs <pod-name>

# Follow logs in real-time
kubectl logs -f deployment/bank-marketing-deployment
```

### Scaling
```bash
# Manual scaling
kubectl scale deployment bank-marketing-deployment --replicas=3

# Check HPA status
kubectl get hpa
kubectl describe hpa bank-marketing-hpa

# Watch HPA (updates every 2 seconds)
kubectl get hpa -w
```

### Debugging
```bash
# Get pod details
kubectl get pods -o wide

# Check pod events
kubectl get events --sort-by=.metadata.creationTimestamp

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash

# Check resource usage (requires metrics-server)
kubectl top nodes
kubectl top pods
```

## 🧪 Testing Scenarios

### Test 1: Basic Prediction
```bash
python test_prediction.py
```

### Test 2: Custom Data
```bash
python test_prediction.py \
  --job "technician" \
  --duration 300 \
  --poutcome "failure"
```

### Test 3: Custom JSON
```bash
python test_prediction.py \
  --json '{"job": "student", "duration": 100, "poutcome": "unknown"}'
```

### Test 4: Different URLs
```bash
# Test local Docker
python test_prediction.py --url http://localhost:9696/predict

# Test Kubernetes (with port-forward)
python test_prediction.py --url http://localhost:9696/predict
```

### Test 5: Load Testing
```bash
# Light load
python load_test.py --requests 100 --workers 5

# Heavy load
python load_test.py --requests 1000 --workers 20 --delay 0.01

# Stress test
python load_test.py --requests 5000 --workers 50 --delay 0
```

## 📊 Monitoring HPA

To monitor autoscaling behavior:

```bash
# Terminal 1: Watch HPA
watch kubectl get hpa

# Terminal 2: Watch pods
watch kubectl get pods

# Terminal 3: Watch metrics
watch kubectl top pods

# Terminal 4: Run load test
python load_test.py --requests 1000
```

## 🐛 Troubleshooting

### Issue: Cannot connect to service

**Symptom:** `Connection refused` when testing

**Solutions:**
1. Check if port-forward is running:
   ```bash
   ps aux | grep port-forward
   ```

2. Restart port-forward:
   ```bash
   kubectl port-forward service/bank-marketing-service 9696:80
   ```

3. Check if pods are running:
   ```bash
   kubectl get pods
   ```

### Issue: Pods not starting

**Symptom:** Pods stuck in `Pending` or `ImagePullBackOff`

**Solutions:**
1. Check pod status:
   ```bash
   kubectl describe pod <pod-name>
   ```

2. Verify image was loaded:
   ```bash
   docker exec -it ml-zoomcamp-cluster-control-plane crictl images | grep zoomcamp
   ```

3. Reload image:
   ```bash
   kind load docker-image zoomcamp-model:3.11.5-hw10 --name ml-zoomcamp-cluster
   ```

### Issue: HPA not scaling

**Symptom:** HPA shows `<unknown>` for CPU or doesn't scale

**Solutions:**
1. Check metrics-server:
   ```bash
   kubectl get deployment metrics-server -n kube-system
   kubectl top nodes
   ```

2. Reinstall metrics-server:
   ```bash
   kubectl delete deployment metrics-server -n kube-system
   # Then run setup_cluster.sh again
   ```

3. Increase load:
   ```bash
   python load_test.py --requests 2000 --workers 20 --delay 0
   ```

### Issue: Cluster won't start

**Symptom:** `kind create cluster` fails

**Solutions:**
1. Delete existing cluster:
   ```bash
   kind delete cluster --name ml-zoomcamp-cluster
   ```

2. Check Docker:
   ```bash
   docker ps
   docker info
   ```

3. Restart Docker and try again

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kind Documentation](https://kind.sigs.k8s.io/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [ML Zoomcamp Course](https://github.com/DataTalksClub/machine-learning-zoomcamp)

## 🎓 Learning Objectives

By completing this homework, you will learn:

1. ✅ Docker image management and tagging
2. ✅ Creating and managing Kubernetes clusters with kind
3. ✅ Kubernetes Deployments and resource management
4. ✅ Kubernetes Services and load balancing
5. ✅ Port forwarding for local testing
6. ✅ Horizontal Pod Autoscaling based on CPU metrics
7. ✅ Load testing and monitoring
8. ✅ Debugging Kubernetes applications

## 📞 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the inline comments in YAML files
3. Run `kubectl describe` on failing resources
4. Check pod logs with `kubectl logs`
5. Ask in the ML Zoomcamp Slack channel

## 🧹 Cleanup

### Remove Kubernetes resources only
```bash
./cleanup.sh
```

### Remove everything (including cluster)
```bash
./cleanup.sh --delete-cluster
```

### Manual cleanup
```bash
# Delete resources
kubectl delete hpa bank-marketing-hpa
kubectl delete service bank-marketing-service
kubectl delete deployment bank-marketing-deployment

# Delete cluster
kind delete cluster --name ml-zoomcamp-cluster

# Remove Docker container (if testing locally)
docker stop zoomcamp-test
docker rm zoomcamp-test
```

---

**Good luck with the homework! 🚀**
