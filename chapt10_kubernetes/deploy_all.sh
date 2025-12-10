#!/bin/bash

# =============================================================================
# Deploy All Resources Script
# =============================================================================
# This script deploys all Kubernetes resources for the homework
#
# Usage: ./deploy_all.sh [--with-hpa]
# =============================================================================

set -e  # Exit on error

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
WITH_HPA=false

# Parse arguments
if [[ "$1" == "--with-hpa" ]]; then
    WITH_HPA=true
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Deploying Bank Marketing Application${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# =============================================================================
# Step 1: Deploy Application
# =============================================================================
echo -e "${YELLOW}[1/3]${NC} Deploying application..."

kubectl apply -f deployment.yaml

echo -e "  ${GREEN}✓${NC} Deployment created/updated"

# Wait for deployment to be ready
echo -e "  Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=60s deployment/${DEPLOYMENT_NAME}

echo -e "  ${GREEN}✓${NC} Deployment is ready"

# Show deployment status
kubectl get deployment ${DEPLOYMENT_NAME}

# =============================================================================
# Step 2: Create Service
# =============================================================================
echo -e "\n${YELLOW}[2/3]${NC} Creating service..."

kubectl apply -f service.yaml

echo -e "  ${GREEN}✓${NC} Service created/updated"

# Show service status
kubectl get service ${SERVICE_NAME}

# =============================================================================
# Step 3: Create HPA (Optional)
# =============================================================================
if [ "${WITH_HPA}" = true ]; then
    echo -e "\n${YELLOW}[3/3]${NC} Creating Horizontal Pod Autoscaler..."

    kubectl apply -f hpa.yaml

    echo -e "  ${GREEN}✓${NC} HPA created/updated"

    # Show HPA status
    sleep 2  # Give metrics a moment to populate
    kubectl get hpa ${HPA_NAME}
else
    echo -e "\n${YELLOW}[3/3]${NC} Skipping HPA (use --with-hpa to enable)"
fi

# =============================================================================
# Summary
# =============================================================================
echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Show all resources
echo -e "${BLUE}Resources:${NC}"
kubectl get deployments,services,pods,hpa 2>/dev/null | grep -E "NAME|bank-marketing"

echo ""
echo -e "${BLUE}Testing the Service:${NC}"
echo -e "  1. Start port forwarding (in another terminal):"
echo -e "     ${GREEN}kubectl port-forward service/${SERVICE_NAME} 9696:80${NC}"
echo ""
echo -e "  2. Test the prediction endpoint:"
echo -e "     ${GREEN}python test_prediction.py${NC}"
echo ""
echo -e "  3. Run load test (if HPA is enabled):"
echo -e "     ${GREEN}python load_test.py --requests 1000${NC}"
echo ""

if [ "${WITH_HPA}" = true ]; then
    echo -e "${BLUE}Monitoring Autoscaling:${NC}"
    echo -e "  Watch HPA: ${GREEN}kubectl get hpa -w${NC}"
    echo -e "  Watch pods: ${GREEN}kubectl get pods -w${NC}"
    echo ""
fi

echo -e "${BLUE}Logs and Debugging:${NC}"
echo -e "  View logs: ${GREEN}kubectl logs deployment/${DEPLOYMENT_NAME}${NC}"
echo -e "  Describe deployment: ${GREEN}kubectl describe deployment ${DEPLOYMENT_NAME}${NC}"
echo -e "  Describe service: ${GREEN}kubectl describe service ${SERVICE_NAME}${NC}"
echo ""

echo -e "${BLUE}Cleanup:${NC}"
echo -e "  Delete all: ${GREEN}./cleanup.sh${NC}"
echo ""
