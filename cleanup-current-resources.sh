#!/bin/bash
# Cleanup script for AWS Free Tier cost optimization
# This will remove NAT Gateways and unused resources to achieve $0/month cost

set -e

REGION="eu-north-1"

echo "=========================================="
echo "AWS Free Tier Cleanup Script"
echo "=========================================="
echo ""
echo "This script will:"
echo "1. Delete NAT Gateways (saves $45/month each)"
echo "2. Release unused Elastic IPs (saves $3.50/month each)"
echo "3. Show VPCs for manual cleanup decision"
echo ""
echo "Current estimated monthly cost: ~$90"
echo "After cleanup estimated cost: $0"
echo ""
read -p "Do you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "Step 1: Deleting NAT Gateways..."
echo "=================================="

# Get all available NAT Gateways
NAT_GATEWAYS=$(aws ec2 describe-nat-gateways \
    --region $REGION \
    --filter "Name=state,Values=available" \
    --query 'NatGateways[*].NatGatewayId' \
    --output text)

if [ -z "$NAT_GATEWAYS" ]; then
    echo "No NAT Gateways to delete."
else
    for nat_id in $NAT_GATEWAYS; do
        echo "Deleting NAT Gateway: $nat_id"
        aws ec2 delete-nat-gateway --nat-gateway-id $nat_id --region $REGION
        echo "✓ Deleted $nat_id (saves $45/month)"
    done
    
    echo ""
    echo "Waiting 60 seconds for NAT Gateways to delete..."
    sleep 60
fi

echo ""
echo "Step 2: Releasing Elastic IPs..."
echo "=================================="

# Get all Elastic IPs
EIPS=$(aws ec2 describe-addresses \
    --region $REGION \
    --query 'Addresses[*].[AllocationId,AssociationId]' \
    --output text)

if [ -z "$EIPS" ]; then
    echo "No Elastic IPs found."
else
    echo "$EIPS" | while read alloc_id assoc_id; do
        if [ -z "$assoc_id" ] || [ "$assoc_id" == "None" ]; then
            echo "Releasing unassociated EIP: $alloc_id"
            aws ec2 release-address --allocation-id $alloc_id --region $REGION
            echo "✓ Released $alloc_id (saves $3.50/month if unused)"
        else
            echo "Skipping EIP $alloc_id (still associated with $assoc_id)"
        fi
    done
fi

echo ""
echo "Step 3: VPC Information"
echo "=================================="
echo "Current VPCs in your account:"
aws ec2 describe-vpcs --region $REGION \
    --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0]]' \
    --output table

echo ""
echo "=========================================="
echo "Cleanup Summary"
echo "=========================================="
echo ""
echo "✓ NAT Gateways deleted"
echo "✓ Unused Elastic IPs released"
echo ""
echo "Next Steps:"
echo "1. Wait 2-3 minutes for resources to fully delete"
echo "2. Verify in AWS Console that NAT Gateways are gone"
echo "3. Check billing dashboard in 24 hours"
echo ""
echo "To delete VPCs and all resources:"
echo "  Option A: Use Terraform destroy"
echo "  Option B: Delete manually in AWS Console"
echo ""
echo "Estimated monthly savings: $90+"
echo ""
