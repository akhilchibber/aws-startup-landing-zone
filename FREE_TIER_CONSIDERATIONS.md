# AWS Free Tier Considerations for Account Factory

**Account Type:** AWS Free Tier  
**Date:** February 26, 2026  
**Status:** Active Constraints

---

## Overview

This document outlines the AWS Free Tier limitations and how they impact the Account Factory implementation. It provides strategies for cost-effective testing and deployment within free tier constraints.

---

## AWS Free Tier Limits (Relevant to Account Factory)

### Compute & Networking

| Service | Free Tier Limit | Current Usage | Notes |
|---------|----------------|---------------|-------|
| **Elastic IPs** | 1 EIP (when attached) | 1 in use | ⚠️ Additional EIPs cost $3.50/month each |
| **NAT Gateway** | Not included | 1 active | 💰 $45/month per NAT Gateway |
| **VPC** | Unlimited | 1 VPC | ✅ Free |
| **Subnets** | Unlimited | 4 subnets | ✅ Free |
| **Internet Gateway** | Unlimited | 1 IGW | ✅ Free |
| **Route Tables** | Unlimited | 4 tables | ✅ Free |
| **VPC Flow Logs** | Not included | 1 active | 💰 ~$1-5/month |
| **Data Transfer** | 100 GB/month out | Variable | ⚠️ $0.09/GB after limit |

### Storage

| Service | Free Tier Limit | Current Usage | Notes |
|---------|----------------|---------------|-------|
| **S3 Storage** | 5 GB | <1 GB | ✅ Within limit |
| **S3 Requests** | 20,000 GET, 2,000 PUT | Low | ✅ Within limit |
| **DynamoDB** | 25 GB storage | <1 MB | ✅ Within limit |

### Organizations & Management

| Service | Free Tier Limit | Current Usage | Notes |
|---------|----------------|---------------|-------|
| **AWS Organizations** | Free | 1 org | ✅ Free |
| **Account Creation** | Free | Multiple accounts | ✅ Free |
| **CloudWatch Logs** | 5 GB ingestion | <1 GB | ✅ Within limit |
| **Budget Alerts** | 2 budgets free | 1 per account | ⚠️ $0.02/day per budget after 2 |

---

## Current Cost Analysis

### Monthly Costs (Current Setup)

| Component | Quantity | Monthly Cost | Free Tier | Actual Cost |
|-----------|----------|--------------|-----------|-------------|
| NAT Gateway | 1 | $45.00 | $0 | **$45.00** |
| Elastic IP (in use) | 1 | $0 | $0 | $0 |
| VPC Flow Logs | 1 | $1-5 | $0 | **$1-5** |
| S3 Storage | <1 GB | $0.023/GB | 5 GB free | $0 |
| DynamoDB | <1 MB | $0 | 25 GB free | $0 |
| Data Transfer | <10 GB | $0.09/GB | 100 GB free | $0 |
| **TOTAL** | | | | **~$46-50/month** |

### Cost Drivers

1. **NAT Gateway** - $45/month (96% of total cost)
2. **VPC Flow Logs** - $1-5/month (4% of total cost)

---

## Cost Optimization Strategies

### Strategy 1: Remove NAT Gateway (Recommended for Free Tier)

**Impact:** Eliminates 96% of monthly costs

**Trade-offs:**
- Private subnets cannot access internet
- Applications in private subnets cannot download packages, call APIs, etc.
- Suitable for: Static applications, applications that don't need internet access

**Implementation:**
```hcl
# In modules/environment/main.tf
# Comment out or remove:
# - aws_eip.nat
# - aws_nat_gateway.environment
# - Private route table route to NAT Gateway

# Update private route table to only have local route
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.environment.id
  
  # Only local route, no internet access
  tags = merge(
    var.common_tags,
    {
      Name = "${var.team_name}-${var.environment}-private-rt"
    }
  )
}
```

**Monthly Cost After:** ~$1-5 (VPC Flow Logs only)

### Strategy 2: Use Public Subnets Only

**Impact:** Eliminates NAT Gateway cost, simplifies architecture

**Trade-offs:**
- All resources have public IPs (less secure)
- No network isolation
- Suitable for: Development/testing only, non-sensitive workloads

**Implementation:**
```hcl
# Deploy all resources in public subnets
# Remove private subnets entirely
# All resources route through Internet Gateway
```

**Monthly Cost After:** ~$1-5 (VPC Flow Logs only)

### Strategy 3: Disable VPC Flow Logs

**Impact:** Eliminates remaining costs

**Trade-offs:**
- No network traffic monitoring
- Harder to troubleshoot connectivity issues
- Not suitable for production or compliance requirements

**Implementation:**
```hcl
# In modules/environment/main.tf
# Comment out or remove:
# - aws_cloudwatch_log_group.environment
# - aws_iam_role.flowlog
# - aws_iam_role_policy.flowlog
# - aws_flow_log.environment
```

**Monthly Cost After:** $0 (completely free!)

### Strategy 4: Minimal Testing Setup (Recommended)

**Configuration:**
- 1 VPC
- 2 public subnets (multi-AZ)
- 1 Internet Gateway
- No NAT Gateway
- No VPC Flow Logs
- No private subnets

**Monthly Cost:** $0 (completely free!)

**Suitable for:**
- Testing the account factory workflow
- Validating GitHub Actions integration
- Learning and experimentation
- Non-production workloads

---

## Recommended Implementation Plan for Free Tier

### Phase 1: Minimal Testing (Current - Free)

**Goal:** Validate account factory workflow without costs

**Configuration:**
```
VPC (10.0.0.0/16)
├── Public Subnet 1a (10.0.0.0/24)
├── Public Subnet 1b (10.0.1.0/24)
└── Internet Gateway
```

**What to test:**
- GitHub issue workflow
- Account creation
- Basic infrastructure deployment
- Terraform state management

**Monthly Cost:** $0

### Phase 2: Add Private Subnets (Still Free)

**Goal:** Test network segmentation without NAT Gateway

**Configuration:**
```
VPC (10.0.0.0/16)
├── Public Subnet 1a (10.0.0.0/24)
├── Public Subnet 1b (10.0.1.0/24)
├── Private Subnet 1a (10.0.32.0/19) - No internet access
├── Private Subnet 1b (10.0.64.0/19) - No internet access
└── Internet Gateway
```

**What to test:**
- Network isolation
- Security group rules
- VPC peering (if needed)

**Monthly Cost:** $0

### Phase 3: Add NAT Gateway (When Budget Allows)

**Goal:** Enable private subnet internet access

**Configuration:**
```
VPC (10.0.0.0/16)
├── Public Subnet 1a (10.0.0.0/24)
│   └── NAT Gateway ($45/month)
├── Public Subnet 1b (10.0.1.0/24)
├── Private Subnet 1a (10.0.32.0/19) → NAT Gateway
└── Private Subnet 1b (10.0.64.0/19) → NAT Gateway
```

**Monthly Cost:** ~$45-50

---

## Free Tier Friendly Next Steps

### Immediate Actions (This Week - $0 Cost)

1. **Clean Up Test Resources**
   ```bash
   # Keep only one test account
   # Delete others to avoid confusion
   
   # Release unused Elastic IPs
   aws ec2 describe-addresses --region eu-north-1
   aws ec2 release-address --allocation-id eipalloc-XXXXX
   
   # Delete old NAT Gateways (saves $45/month each)
   aws ec2 delete-nat-gateway --nat-gateway-id nat-XXXXX
   ```

2. **Simplify Current Infrastructure**
   - Remove NAT Gateway from dev environment
   - Remove VPC Flow Logs
   - Keep only public subnets
   - Update Terraform configuration

3. **Update Documentation**
   - Mark as "Free Tier Configuration"
   - Document limitations
   - Provide upgrade path

### Limited Launch with Free Tier (1-2 Weeks - $0 Cost)

**Approach:** Use simplified architecture for pilot teams

**Configuration:**
- Public subnets only
- No NAT Gateway
- No VPC Flow Logs
- Basic security groups

**Pilot Team Selection:**
- Choose teams with non-sensitive workloads
- Teams comfortable with public subnet deployment
- Teams that understand free tier limitations

**What Pilot Teams Get:**
- AWS Organizations account
- VPC with public subnets
- Internet Gateway
- Basic security groups
- Budget alerts (first 2 free)

**What They Don't Get:**
- Private subnets with internet access
- NAT Gateway
- VPC Flow Logs
- Advanced monitoring

### Gradual Rollout (When Budget Allows)

**Option 1: Stay Free Tier**
- Continue with public subnet architecture
- Suitable for: Development, testing, learning

**Option 2: Upgrade to Paid**
- Add NAT Gateway when budget allows
- Add VPC Flow Logs for monitoring
- Implement full architecture

---

## Alternative Solutions for Free Tier

### Option 1: NAT Instance (Instead of NAT Gateway)

**Cost:** ~$3-5/month (t3.nano instance)

**Pros:**
- Much cheaper than NAT Gateway ($45/month)
- Provides internet access for private subnets
- Can be stopped when not needed

**Cons:**
- Requires management (patching, monitoring)
- Single point of failure
- Lower bandwidth than NAT Gateway
- Not recommended for production

**Implementation:**
```hcl
# Launch t3.nano instance in public subnet
# Configure as NAT instance
# Update private route table to point to NAT instance
```

### Option 2: VPC Endpoints (For AWS Services)

**Cost:** $0.01/hour per endpoint (~$7/month)

**Pros:**
- Private subnet resources can access AWS services
- No NAT Gateway needed for AWS API calls
- More secure than internet access

**Cons:**
- Only works for AWS services (S3, DynamoDB, etc.)
- Doesn't provide general internet access
- Still need NAT for external APIs

**Implementation:**
```hcl
# Create VPC endpoints for S3, DynamoDB, etc.
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.environment.id
  service_name = "com.amazonaws.eu-north-1.s3"
}
```

### Option 3: Hybrid Approach

**Configuration:**
- Public subnets for web-facing resources
- Private subnets for databases (no internet needed)
- VPC endpoints for AWS service access
- No NAT Gateway

**Cost:** ~$7/month (VPC endpoints only)

**Suitable for:**
- Applications that only need AWS services
- Databases that don't need internet
- Cost-conscious deployments

---

## Monitoring Free Tier Usage

### Set Up Billing Alerts

```bash
# Create budget alert for $10/month
aws budgets create-budget \
  --account-id YOUR_ACCOUNT_ID \
  --budget file://budget.json
```

**budget.json:**
```json
{
  "BudgetName": "Monthly-Budget-Alert",
  "BudgetLimit": {
    "Amount": "10",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST"
}
```

### Track Free Tier Usage

1. **AWS Console:**
   - Billing Dashboard → Free Tier
   - Shows usage vs. limits

2. **AWS CLI:**
   ```bash
   aws ce get-cost-and-usage \
     --time-period Start=2026-02-01,End=2026-02-28 \
     --granularity MONTHLY \
     --metrics BlendedCost
   ```

3. **Cost Explorer:**
   - Filter by service
   - Track trends
   - Identify cost drivers

---

## Recommendations for Your Account

### Immediate (Today)

1. **Delete Old NAT Gateways**
   - You have NAT Gateways from previous tests
   - Each costs $45/month
   - Keep only one if needed, or delete all

2. **Release Unused Elastic IPs**
   - Unused EIPs cost $3.50/month
   - Keep only what's needed

3. **Disable VPC Flow Logs (Optional)**
   - Saves $1-5/month
   - Can re-enable when needed

### Short-term (This Week)

4. **Simplify Architecture**
   - Update Terraform to remove NAT Gateway
   - Use public subnets only
   - Document as "Free Tier Configuration"

5. **Update Account Factory**
   - Modify environment module
   - Remove NAT Gateway creation
   - Update documentation

### Long-term (When Budget Allows)

6. **Upgrade Path**
   - Add NAT Gateway when budget allows
   - Add VPC Flow Logs for monitoring
   - Implement full production architecture

---

## Cost Comparison

### Current Setup (With NAT Gateway)
- Monthly Cost: ~$46-50
- Annual Cost: ~$552-600

### Free Tier Setup (No NAT Gateway)
- Monthly Cost: $0
- Annual Cost: $0
- **Savings: $552-600/year**

### Minimal Paid Setup (NAT Instance)
- Monthly Cost: ~$3-8
- Annual Cost: ~$36-96
- **Savings: $456-564/year vs NAT Gateway**

---

## Conclusion

For AWS Free Tier accounts, the recommended approach is:

1. **Immediate:** Remove NAT Gateway and VPC Flow Logs (saves $46-50/month)
2. **Testing:** Use public subnets only for account factory testing
3. **Limited Launch:** Deploy pilot teams with simplified architecture
4. **Future:** Add NAT Gateway when budget allows or when moving to production

This approach allows you to:
- ✅ Test the account factory workflow completely free
- ✅ Validate GitHub Actions integration
- ✅ Onboard pilot teams without costs
- ✅ Learn and experiment without budget concerns
- ✅ Upgrade to full architecture when ready

---

**Free Tier Considerations**  
**Date:** February 26, 2026  
**Version:** 1.0  
**Recommended:** Remove NAT Gateway for $0/month operation
