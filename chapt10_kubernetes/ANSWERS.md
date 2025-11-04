# Chapter 10 - Kubernetes Homework Answers

This file contains your answers to the homework questions. Fill in your answers as you complete each question.

---

## Question 1: Model Probability

**Question:** What is the probability returned by the model when testing locally?

**How to get the answer:**
```bash
# Option 1: Using test script
python test_prediction.py

# Option 2: Using notebook
# Run the "Question 1" section in chapt10_kubernetes_homework.ipynb

# Option 3: Using curl
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{"job": "management", "duration": 400, "poutcome": "success"}'
```

**Your Answer:** ____________

**Available Options:**
- [ ] 0.287
- [ ] 0.530
- [ ] 0.757
- [ ] 0.960

---

## Question 2: Kind Version

**Question:** What is your installed kind version?

**How to get the answer:**
```bash
kind --version
```

**Your Answer:** ____________

**Example:** `kind v0.20.0 go1.20.4 linux/amd64`

---

## Question 3: Kubernetes Concepts

**Question:** What is the smallest deployable unit of computing in Kubernetes?

**Your Answer:** ____________

**Available Options:**
- [ ] Node
- [ ] Pod ✅ (Expected answer)
- [ ] Deployment
- [ ] Service

**Explanation:** A Pod is a group of one or more containers with shared storage and network resources. It's the smallest deployable unit in Kubernetes.

---

## Question 4: Service Types

**Question:** What service type is running after cluster creation (for the default kubernetes service)?

**How to get the answer:**
```bash
kubectl get services --all-namespaces
# Look for the 'kubernetes' service in the 'default' namespace
```

**Your Answer:** ____________

**Available Options:**
- [ ] NodePort
- [ ] ClusterIP ✅ (Expected answer)
- [ ] ExternalName
- [ ] LoadBalancer

---

## Question 5: Load Docker Image

**Question:** What command is used to load a Docker image into the kind cluster?

**How to get the answer:**
```bash
# The command you used or would use:
kind load docker-image zoomcamp-model:3.11.5-hw10 --name ml-zoomcamp-cluster
```

**Your Answer:** ____________

**Expected pattern:** `kind load docker-image`

**Available Options:**
- [ ] `kind create cluster`
- [ ] `kind build node-image`
- [ ] `kind load docker-image` ✅
- [ ] `kubectl apply`

---

## Question 6: Container Port

**Question:** What is the containerPort specified in the deployment?

**How to get the answer:**
```bash
# Option 1: Check the YAML file
cat deployment.yaml | grep containerPort

# Option 2: Describe the deployment
kubectl describe deployment bank-marketing-deployment | grep -i port

# Option 3: Get YAML from cluster
kubectl get deployment bank-marketing-deployment -o yaml | grep containerPort
```

**Your Answer:** ____________

**Expected answer:** `9696`

**YAML path:** `spec.template.spec.containers[0].ports[0].containerPort`

---

## Question 7: Service Selector

**Question:** In the service definition, what value replaces `<???>` in the selector `app: <???>`?

**How to get the answer:**
```bash
# Option 1: Check the YAML file
cat service.yaml | grep -A 2 selector

# Option 2: Describe the service
kubectl describe service bank-marketing-service | grep -i selector

# Option 3: Get YAML from cluster
kubectl get service bank-marketing-service -o yaml | grep -A 2 selector
```

**Your Answer:** ____________

**Expected answer:** `bank-marketing`

**Note:** This selector must match the label in the deployment's pod template.

---

## Question 8: Maximum Replicas (Optional)

**Question:** What is the maximum number of replicas achieved during the load test?

**Prerequisites:**
- HPA must be enabled: `kubectl apply -f hpa.yaml`
- Metrics server must be running
- Port forwarding must be active

**How to get the answer:**
```bash
# Terminal 1: Port forward
kubectl port-forward service/bank-marketing-service 9696:80

# Terminal 2: Run load test
python load_test.py --requests 1000 --workers 10

# Terminal 3: Monitor (during load test)
kubectl get hpa -w
kubectl get pods -w

# After load test: Count pods
kubectl get pods | grep bank-marketing | wc -l
```

**Your Answer:** ____________

**Available Options:**
- [ ] 1
- [ ] 2
- [ ] 3
- [ ] 4

**HPA Configuration:**
- Min Replicas: 1
- Max Replicas: 3
- CPU Threshold: 20%

**Notes:**
- The actual number depends on CPU utilization during the test
- May need to run multiple tests or increase load intensity
- Watch the HPA metrics: `kubectl get hpa`

---

## Summary

| Question | Your Answer | Status |
|----------|-------------|--------|
| Q1       |             | ⬜     |
| Q2       |             | ⬜     |
| Q3       |             | ⬜     |
| Q4       |             | ⬜     |
| Q5       |             | ⬜     |
| Q6       |             | ⬜     |
| Q7       |             | ⬜     |
| Q8       |             | ⬜     |

**Status Legend:**
- ⬜ Not started
- 🔄 In progress
- ✅ Completed

---

## Submission Checklist

Before submitting your homework:

- [ ] All questions answered
- [ ] Tested locally with Docker (Q1)
- [ ] Verified kind version (Q2)
- [ ] Understood Pod concept (Q3)
- [ ] Checked default service type (Q4)
- [ ] Used correct kind command (Q5)
- [ ] Verified deployment containerPort (Q6)
- [ ] Checked service selector (Q7)
- [ ] (Optional) Completed HPA load test (Q8)
- [ ] All screenshots/logs saved (if required)
- [ ] Cleaned up resources after completion

---

## Additional Notes

Add any observations, issues encountered, or learning points here:

```
[Your notes here]
```

---

## Timestamp

- **Started:** ____________
- **Completed:** ____________
- **Total Time:** ____________

---

Good luck! 🚀
