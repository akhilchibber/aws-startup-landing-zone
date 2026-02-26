#!/bin/bash
# Cleanup Script for AWS Free Tier Cost Optimization
# This script helps identify and remove costly resources
# Run with: bash cleanup-free-tier.sh

set -e

REGION="eu-north-1"
echo "=========================================="
echo "AWS Free Tier Cleanup Script"
echo "Region: $REGION"
echo "=========================================="
echo ""

# Check AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first."
    exit 1
fi

echo "✅ AWS CLI found"
echo ""

# Function to confirm action
confirm() {
    read -p "$1 (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        return 1
    fi
    return 0
}

# 1. List NAT Gateways
echo "=========================================="
echo "1. Checking NAT Gateways (Cost: \$45/month each)"
echo "=========================================="
NAT_GATEWAYS=$(aws ec2 describe-nat-gateways --region $REGION --query 'NatGateways[?State==`available`].[NatGatewayId,PublicIp,State]' --output table)

if [ -z "$NAT_GATEWAYS" ] || [ "$NAT_GATEWAYS" == "None" ]; then
    echo "✅ No active NAT Gateways found"
else
    echo "$NAT_GATEWAYS"
    echo ""
    
    # Get NAT Gateway IDs
    NAT_IDS=$(aws ec2 describe-nat-gateways --region $REGION --query 'NatGateways[?State==`available`].NatGatewayId' --output text)
    
    for NAT_ID in $NAT_IDS; do
        if confirm "Delete NAT Gateway $NAT_ID? (Saves \$45/month)"; then
            echo "Deleting NAT Gateway $NAT_ID..."
            aws ec2 delete-nat-gateway --nat-gateway-id $NAT_ID --region $REGION
            echo "✅ NAT Gateway $NAT_ID deletion initiated (takes a few minutes)"
        else
            echo "⏭️  Skipped NAT Gateway $NAT_ID"
        fi
    done
fi
echo ""

# 2. List Elastic IPs
echo "=========================================="
echo "2. Checking Elastic IPs (Cost: \$3.50/month if unused)"
echo "=========================================="
EIPS=$(aws ec2 describe-addresses --region $REGION --query 'Addresses[?AssociationId==null].[AllocationId,PublicIp]' --output table)

if [ -z "$EIPS" ] || [ "$EIPS" == "None" ]; then
    echo "✅ No unused Elastic IPs found"
else
    echo "Unused Elastic IPs (not attached to resources):"
    echo "$EIPS"
    echo ""
    
    # Get EIP allocation IDs
    EIP_IDS=$(aws ec2 describe-addresses --region $REGION --query 'Addresses[?AssociationId==null].AllocationId' --output text)
    
    for EIP_ID in $EIP_IDS; do
        EIP_IP=$(aws ec2 describe-addresses --region $REGION --allocation-ids $EIP_ID --query 'Addresses[0].PublicIp' --output text)
        if confirm "Release Elastic IP $EIP_IP ($EIP_ID)? (Saves \$3.50/month)"; then
            echo "Releasing Elastic IP $EIP_ID..."
            aws ec2 release-address --allocation-id $EIP_ID --region $REGION
            echo "✅ Elastic IP $EIP_ID released"
        else
            echo "⏭️  Skipped Elastic IP $EIP_ID"
        fi
    done
fi
echo ""

# 3. List VPC Flow Logs
echo "=========================================="
echo "3. Checking VPC Flow Logs (Cost: \$1-5/month)"
echo "=========================================="
FLOW_LOGS=$(aws ec2 describe-flow-logs --region $REGION --query 'FlowLogs[?FlowLogStatus==`ACTIVE`].[FlowLogId,ResourceId,FlowLogStatus]' --output table)

if [ -z "$FLOW_LOGS" ] || [ "$FLOW_LOGS" == "None" ]; then
    echo "✅ No active VPC Flow Logs found"
else
    echo "$FLOW_LOGS"
    echo ""
    echo "⚠️  VPC Flow Logs cost \$1-5/month"
    echo "💡 To delete, use Terraform or AWS Console"
    echo "   (Requires deleting CloudWatch Log Groups and IAM roles)"
fi
echo ""

# 4. List AWS Organizations Accounts
echo "=========================================="
echo "4. Checking AWS Organizations Accounts"
echo "=========================================="
ACCOUNTS=$(aws organizations list-accounts --query 'Accounts[?Status==`ACTIVE`].[Id,Name,Email]' --output table 2>/dev/null || echo "Not available (requires Organizations permissions)")

if [ "$ACCOUNTS" == "Not available (requires Organizations permissions)" ]; then
    echo "⚠️  Cannot list accounts (requires AWS Organizations permissions)"
else
    echo "$ACCOUNTS"
    echo ""
    echo "💡 Test accounts (cloud-team-*) can be deleted if no longer needed"
    echo "   Use AWS Console → Organizations → Accounts to delete"
fi
echo ""

# 5. Cost Summary
echo "=========================================="
echo "5. Estimated Monthly Cost Savings"
echo "=========================================="

# Count resources
NAT_COUNT=$(aws ec2 describe-nat-gateways --region $REGION --query 'NatGateways[?State==`available`]' --output json | grep -c "NatGatewayId" || echo "0")
EIP_COUNT=$(aws ec2 describe-addresses --region $REGION --query 'Addresses[?AssociationId==null]' --output json | grep -c "AllocationId" || echo "0")
FLOW_COUNT=$(aws ec2 describe-flow-logs --region $REGION --query 'FlowLogs[?FlowLogStatus==`ACTIVE`]' --output json | grep -c "FlowLogId" || echo "0")

NAT_COST=$((NAT_COUNT * 45))
EIP_COST=$((EIP_COUNT * 4))  # Rounded up from $3.50
FLOW_COST=$((FLOW_COUNT * 3))  # Average $3/month

TOTAL_COST=$((NAT_COST + EIP_COST + FLOW_COST))

echo "Current estimated monthly costs:"
echo "  - NAT Gateways: $NAT_COUNT × \$45 = \$$NAT_COST"
echo "  - Unused EIPs: $EIP_COUNT × \$4 = \$$EIP_COST"
echo "  - VPC Flow Logs: $FLOW_COUNT × \$3 = \$$FLOW_COST"
echo "  ─────────────────────────────"
echo "  Total: ~\$$TOTAL_COST/month"
echo ""

if [ $TOTAL_COST -gt 0 ]; then
    echo "💰 Potential savings by removing all: ~\$$TOTAL_COST/month (\$$(($TOTAL_COST * 12))/year)"
else
    echo "✅ No costly resources found! You're optimized for free tier."
fi
echo ""

# 6. Recommendations
echo "=========================================="
echo "6. Recommendations"
echo "=========================================="
echo ""
echo "For AWS Free Tier accounts, we recommend:"
echo ""
echo "1. ✅ Remove NAT Gateways (saves \$45/month each)"
echo "   - Use public subnets only"
echo "   - Or use NAT instance (\$3-5/month) if needed"
echo ""
echo "2. ✅ Release unused Elastic IPs (saves \$3.50/month each)"
echo "   - Keep only what's actively used"
echo ""
echo "3. ⚠️  Consider disabling VPC Flow Logs (saves \$1-5/month)"
echo "   - Only if not needed for monitoring"
echo ""
echo "4. 📚 See FREE_TIER_CONSIDERATIONS.md for:"
echo "   - Detailed cost analysis"
echo "   - Alternative architectures"
echo "   - Free tier optimization strategies"
echo ""
echo "=========================================="
echo "Cleanup Complete!"
echo "=========================================="
