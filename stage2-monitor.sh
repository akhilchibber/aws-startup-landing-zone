#!/bin/bash
# Stage 2 Monitoring Script
# Tracks resources, costs, and capacity for pilot team onboarding

set -e

REGION="eu-north-1"
ACCOUNT_ID="066036524935"

echo "=========================================="
echo "AWS Account Factory - Stage 2 Monitor"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# Check EIP usage
echo "📍 Elastic IP Usage:"
EIP_COUNT=$(aws ec2 describe-addresses --region $REGION --query 'length(Addresses)' --output text)
echo "   Used: $EIP_COUNT/5"
echo "   Available: $((5 - EIP_COUNT))"
echo ""

# List EIPs with details
echo "📋 Elastic IP Details:"
aws ec2 describe-addresses --region $REGION \
  --query 'Addresses[*].[AllocationId,PublicIp,AssociationId,Tags[?Key==`Name`].Value|[0]]' \
  --output table
echo ""

# Check NAT Gateway usage
echo "🌐 NAT Gateway Usage:"
NAT_COUNT=$(aws ec2 describe-nat-gateways --region $REGION \
  --filter "Name=state,Values=available" \
  --query 'length(NatGateways)' --output text)
echo "   Active: $NAT_COUNT"
echo "   Monthly Cost: \$$(($NAT_COUNT * 45))"
echo ""

# List NAT Gateways
echo "📋 NAT Gateway Details:"
aws ec2 describe-nat-gateways --region $REGION \
  --filter "Name=state,Values=available" \
  --query 'NatGateways[*].[NatGatewayId,VpcId,SubnetId,Tags[?Key==`Name`].Value|[0]]' \
  --output table
echo ""

# Check VPC count
echo "🏗️  VPC Usage:"
VPC_COUNT=$(aws ec2 describe-vpcs --region $REGION --query 'length(Vpcs)' --output text)
echo "   Total VPCs: $VPC_COUNT"
echo ""

# Check AWS Organizations accounts
echo "👥 AWS Accounts:"
ACCOUNT_COUNT=$(aws organizations list-accounts --query 'length(Accounts)' --output text 2>/dev/null || echo "N/A")
if [ "$ACCOUNT_COUNT" != "N/A" ]; then
  echo "   Total Accounts: $ACCOUNT_COUNT"
  aws organizations list-accounts \
    --query 'Accounts[*].[Id,Name,Email,Status]' \
    --output table
else
  echo "   Unable to list accounts (may need Organizations permissions)"
fi
echo ""

# Calculate capacity
echo "📊 Capacity Analysis:"
AVAILABLE_EIPS=$((5 - EIP_COUNT))
echo "   Can provision: $AVAILABLE_EIPS more accounts"
echo "   Current monthly cost: \$$(($NAT_COUNT * 45 + 5))"
echo "   After 1 pilot: \$$(( ($NAT_COUNT + 1) * 45 + 5))"
echo "   After 2 pilots: \$$(( ($NAT_COUNT + 2) * 45 + 5))"
echo "   Budget: \$150/month"
echo ""

# Check recent costs (current month)
echo "💰 Current Month Costs:"
START_DATE=$(date -u +%Y-%m-01)
END_DATE=$(date -u +%Y-%m-%d)

aws ce get-cost-and-usage \
  --time-period Start=$START_DATE,End=$END_DATE \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --query 'ResultsByTime[0].Total.BlendedCost.Amount' \
  --output text 2>/dev/null | xargs printf "   Total: \$%.2f\n" || echo "   Unable to fetch cost data"

echo ""

# Check for recent GitHub workflow runs
echo "🔄 Recent Workflow Runs:"
if command -v gh &> /dev/null; then
  gh run list --limit 5 --json conclusion,createdAt,name,displayTitle \
    --jq '.[] | "\(.createdAt | split("T")[0]) - \(.displayTitle) - \(.conclusion)"' 2>/dev/null || echo "   No recent runs or gh CLI not configured"
else
  echo "   GitHub CLI not installed (install with: brew install gh)"
fi
echo ""

# Summary
echo "=========================================="
echo "Summary:"
echo "=========================================="
echo "✅ EIPs Available: $AVAILABLE_EIPS"
echo "✅ Monthly Cost: \$$(($NAT_COUNT * 45 + 5))"
echo "✅ Can Onboard: $AVAILABLE_EIPS pilot teams"
if [ $AVAILABLE_EIPS -ge 2 ]; then
  echo "✅ Status: Ready for 2 pilot teams"
elif [ $AVAILABLE_EIPS -eq 1 ]; then
  echo "⚠️  Status: Ready for 1 pilot team only"
else
  echo "❌ Status: At capacity - cleanup needed"
fi
echo "=========================================="
