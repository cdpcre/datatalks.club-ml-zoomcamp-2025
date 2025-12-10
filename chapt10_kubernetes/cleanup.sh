#!/bin/bash

# =============================================================================
# Cleanup Script
# =============================================================================
# This script removes all Kubernetes resources created for the homework
#
# Usage: ./cleanup.sh [--delete-cluster]
# =============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEPLOYMENT_NAME="bank-marketing-deployment"
SERVICE_NAME="bank-marketing-service"
HPA_NAME="bank-marketing-hpa"
CLUSTER_NAME="ml-zoomcamp-cluster"
DELETE_CLUSTER=false

# Parse arguments
if [[ "$1" == "--delete-cluster" ]]; then
    DELETE_CLUSTER=true
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Cleanup Kubernetes Resources${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# =============================================================================
# Step 1: Delete HPA
# =============================================================================
echo -e "${YELLOW}[1/4]${NC} Deleting Horizontal Pod Autoscaler..."

if kubectl get hpa ${HPA_NAME} &> /dev/null; then
    kubectl delete hpa ${HPA_NAME}
    echo -e "  ${GREEN}✓${NC} HPA deleted"
else
    echo -e "  ${BLUE}ℹ${NC}  HPA not found (may not have been created)"
fi

# =============================================================================
# Step 2: Delete Service
# =============================================================================
echo -e "\n${YELLOW}[2/4]${NC} Deleting service..."

if kubectl get service ${SERVICE_NAME} &> /dev/null; then
    kubectl delete service ${SERVICE_NAME}
    echo -e "  ${GREEN}✓${NC} Service deleted"
else
    echo -e "  ${BLUE}ℹ${NC}  Service not found"
fi

# =============================================================================
# Step 3: Delete Deployment
# =============================================================================
echo -e "\n${YELLOW}[3/4]${NC} Deleting deployment..."

if kubectl get deployment ${DEPLOYMENT_NAME} &> /dev/null; then
    kubectl delete deployment ${DEPLOYMENT_NAME}
    echo -e "  ${GREEN}✓${NC} Deployment deleted"
else
    echo -e "  ${BLUE}ℹ${NC}  Deployment not found"
fi

# Wait for pods to terminate
echo -e "  Waiting for pods to terminate..."
kubectl wait --for=delete pod -l app=bank-marketing --timeout=60s 2>/dev/null || true

# =============================================================================
# Step 4: Delete Cluster (Optional)
# =============================================================================
if [ "${DELETE_CLUSTER}" = true ]; then
    echo -e "\n${YELLOW}[4/4]${NC} Deleting kind cluster..."

    if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
        kind delete cluster --name ${CLUSTER_NAME}
        echo -e "  ${GREEN}✓${NC} Cluster deleted"
    else
        echo -e "  ${BLUE}ℹ${NC}  Cluster not found"
    fi
else
    echo -e "\n${YELLOW}[4/4]${NC} Skipping cluster deletion"
    echo -e "  ${BLUE}ℹ${NC}  Use --delete-cluster to remove the entire cluster"
fi

# =============================================================================
# Summary
# =============================================================================
echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Cleanup Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Show remaining resources
echo -e "${BLUE}Remaining resources:${NC}"
kubectl get all --selector=app=bank-marketing 2>/dev/null || echo "  No resources found"

echo ""
if [ "${DELETE_CLUSTER}" != true ]; then
    echo -e "${BLUE}Note:${NC} The kind cluster is still running."
    echo -e "To delete the cluster completely:"
    echo -e "  ${GREEN}./cleanup.sh --delete-cluster${NC}"
    echo -e "  or"
    echo -e "  ${GREEN}kind delete cluster --name ${CLUSTER_NAME}${NC}"
    echo ""
fi
