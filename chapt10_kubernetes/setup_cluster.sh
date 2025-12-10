#!/bin/bash

# =============================================================================
# Kubernetes Cluster Setup Script
# =============================================================================
# This script automates the setup of a kind cluster for the ML Zoomcamp homework
#
# Usage: ./setup_cluster.sh [cluster-name]
# Default cluster name: ml-zoomcamp-cluster
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLUSTER_NAME="${1:-ml-zoomcamp-cluster}"
DOCKER_IMAGE="zoomcamp-model:3.11.5-hw10"
DOCKER_HUB_IMAGE="svizor/zoomcamp-model:3.11.5-hw10"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Kubernetes Cluster Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Cluster Name: ${GREEN}${CLUSTER_NAME}${NC}"
echo -e "Docker Image: ${GREEN}${DOCKER_IMAGE}${NC}"
echo ""

# =============================================================================
# Step 1: Check Prerequisites
# =============================================================================
echo -e "${YELLOW}[1/7]${NC} Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found!${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Docker installed: $(docker --version)"

# Check kind
if ! command -v kind &> /dev/null; then
    echo -e "${RED}❌ kind not found!${NC}"
    echo "Please install kind: https://kind.sigs.k8s.io/docs/user/quick-start/#installation"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} kind installed: $(kind --version)"

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found!${NC}"
    echo "Please install kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} kubectl installed: $(kubectl version --client --short 2>/dev/null || echo 'kubectl installed')"

# =============================================================================
# Step 2: Prepare Docker Image
# =============================================================================
echo -e "\n${YELLOW}[2/7]${NC} Preparing Docker image..."

# Check if image exists locally
if docker image inspect ${DOCKER_IMAGE} &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Docker image already exists locally"
else
    echo -e "  ${YELLOW}⚠${NC}  Docker image not found locally, pulling from Docker Hub..."
    docker pull ${DOCKER_HUB_IMAGE}
    docker tag ${DOCKER_HUB_IMAGE} ${DOCKER_IMAGE}
    echo -e "  ${GREEN}✓${NC} Docker image pulled and tagged"
fi

# =============================================================================
# Step 3: Delete Existing Cluster (if exists)
# =============================================================================
echo -e "\n${YELLOW}[3/7]${NC} Checking for existing cluster..."

if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
    echo -e "  ${YELLOW}⚠${NC}  Cluster '${CLUSTER_NAME}' already exists"
    read -p "  Delete existing cluster? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "  ${YELLOW}⚠${NC}  Deleting cluster..."
        kind delete cluster --name ${CLUSTER_NAME}
        echo -e "  ${GREEN}✓${NC} Cluster deleted"
    else
        echo -e "  ${BLUE}ℹ${NC}  Using existing cluster"
        CLUSTER_EXISTS=true
    fi
else
    echo -e "  ${GREEN}✓${NC} No existing cluster found"
fi

# =============================================================================
# Step 4: Create Cluster
# =============================================================================
if [ "${CLUSTER_EXISTS}" != "true" ]; then
    echo -e "\n${YELLOW}[4/7]${NC} Creating kind cluster..."
    kind create cluster --name ${CLUSTER_NAME}
    echo -e "  ${GREEN}✓${NC} Cluster created"
else
    echo -e "\n${YELLOW}[4/7]${NC} Skipping cluster creation (using existing)"
fi

# =============================================================================
# Step 5: Verify Cluster
# =============================================================================
echo -e "\n${YELLOW}[5/7]${NC} Verifying cluster..."

# Set kubectl context
kubectl cluster-info --context kind-${CLUSTER_NAME}
echo -e "  ${GREEN}✓${NC} Cluster is running"

# Check nodes
echo -e "\n  Nodes:"
kubectl get nodes

# =============================================================================
# Step 6: Load Docker Image to kind
# =============================================================================
echo -e "\n${YELLOW}[6/7]${NC} Loading Docker image into kind cluster..."

kind load docker-image ${DOCKER_IMAGE} --name ${CLUSTER_NAME}
echo -e "  ${GREEN}✓${NC} Docker image loaded"

# =============================================================================
# Step 7: Install Metrics Server (for HPA)
# =============================================================================
echo -e "\n${YELLOW}[7/7]${NC} Installing metrics-server for HPA..."

# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Patch for kind (insecure TLS)
kubectl patch deployment metrics-server -n kube-system --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'

echo -e "  ${GREEN}✓${NC} Metrics server installed (may take a minute to be ready)"

# =============================================================================
# Summary
# =============================================================================
echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Cluster Name: ${GREEN}${CLUSTER_NAME}${NC}"
echo -e "Context: ${GREEN}kind-${CLUSTER_NAME}${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Deploy the application:"
echo "     kubectl apply -f deployment.yaml"
echo ""
echo "  2. Create the service:"
echo "     kubectl apply -f service.yaml"
echo ""
echo "  3. (Optional) Enable autoscaling:"
echo "     kubectl apply -f hpa.yaml"
echo ""
echo "  4. Test the deployment:"
echo "     kubectl port-forward service/bank-marketing-service 9696:80"
echo "     python test_prediction.py"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "  kubectl get all                  # View all resources"
echo "  kubectl get pods                 # View pods"
echo "  kubectl get services             # View services"
echo "  kubectl get hpa                  # View autoscaler"
echo "  kubectl logs <pod-name>          # View pod logs"
echo "  kubectl describe pod <pod-name>  # Pod details"
echo ""
echo -e "${BLUE}Cleanup:${NC}"
echo "  kind delete cluster --name ${CLUSTER_NAME}"
echo ""
