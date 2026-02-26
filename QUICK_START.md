# AWS Hospital Landing Zone - Quick Start Guide

**Get up and running in 5 minutes**

---

## What You're Getting

A production-ready AWS network for hospital teams with:
- 1 VPC (10.0.0.0/16) - Hospital network
- 2 Public Subnets (DMZ layer) - Load balancers, API gateways
- 2 Private Subnets (Application layer) - EHR, telemedicine, lab systems
- 2 NAT Gateways (High availability) - Secure outbound access
- 1 Internet Gateway - Internet connectivity
- VPC Flow Logs (Monitoring) - HIPAA audit trails

**Cost:** ~$73-81/month  
**Deployment Time:** 2-3 hours  
**Status:** ✅ Production Ready

---

## Prerequisites

### AWS Account Setup
```bash
# 1. Create S3 bucket for Terraform state
aws s3api create-bucket \
  --bucket hospital-landing-zone-terraform \
  --region eu-north-1 \
  --create-bucket-configuration LocationConstraint=eu-north-1

# 2. Enable versioning
aws s3api put-bucket-versioning \
  --bucket hospital-landing-zone-terraform \
  --versioning-configuration Status=Enabled

# 3. Enable encryption
aws s3api put-bucket-encryption \
  --bucket hospital-landing-zone-terraform \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# 4. Allocate 2 Elastic IPs
aws ec2 allocate-address --region eu-north-1
aws ec2 allocate-address --region eu-north-1
# Note the allocation IDs (eipalloc-xxxxx)

# 5. Create DynamoDB lock table
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-north-1
```

### Local Setup
```bash
# Install Terraform (if not already installed)
# macOS
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_linux_amd64.zip
unzip terraform_1.0.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform version
```

---

## Configuration

### Step 1: Update S3 Bucket Name

Edit `environments/development/main.tf`:
```hcl
terraform {
  backend "s3" {
    bucket         = "hospital-landing-zone-terraform"  # ← Your bucket name
    key            = "network/dev"
    region         = "eu-north-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Step 2: Update Elastic IP IDs

Edit `environments/development/terraform.tfvars`:
```hcl
aws_region                    = "eu-north-1"
aws_elastic_ip_allocation_ids = ["eipalloc-xxxxx", "eipalloc-yyyyy"]  # ← Your allocation IDs
product                       = "startup"
environment                   = "d"
```

---

## Deployment

### Step 1: Initialize Terraform
```bash
cd environments/development
terraform init
```

**Expected Output:**
```
Terraform has been successfully configured!
```

### Step 2: Review Plan
```bash
terraform plan -out=tfplan
```

**Expected Output:**
```
Plan: 25 to add, 0 to change, 0 to destroy.
```

### Step 3: Deploy
```bash
terraform apply tfplan
```

**Expected Output:**
```
Apply complete! Resources: 25 added, 0 changed, 0 destroyed.
```

---

## Verification

### View Outputs
```bash
terraform output
```

**Expected Output:**
```
vpc_id = "vpc-022a72811066aa870"
vpc_cidr = "10.0.0.0/16"
internet_gateway_id = "igw-01a55c30c9fde14b2"
public_subnets = {...}
private_subnets = {...}
nat_gateways = {...}
```

### Verify in AWS Console
```bash
# Check VPC
aws ec2 describe-vpcs --region eu-north-1 --query 'Vpcs[0].[VpcId,CidrBlock,State]' --output table

# Check Subnets
aws ec2 describe-subnets --region eu-north-1 --query 'Subnets[*].[SubnetId,CidrBlock,State]' --output table

# Check NAT Gateways
aws ec2 describe-nat-gateways --region eu-north-1 --query 'NatGateways[*].[NatGatewayId,State,PublicIp]' --output table
```

---

## What's Next?

### Immediate
1. ✅ Review deployment outputs
2. ✅ Verify resources in AWS Console
3. ✅ Test network connectivity

### Short-term (This Week)
1. Create Security Groups
2. Deploy EC2 instances
3. Configure monitoring

### Medium-term (Next Week)
1. Create staging environment
2. Set up load balancers
3. Configure auto-scaling

### Long-term
1. Deploy production environment
2. Set up VPC Endpoints
3. Implement monitoring and alerts

---

## Useful Commands

### View Infrastructure
```bash
# View all outputs
terraform output

# View specific output
terraform output vpc_id

# View state
terraform state list
terraform state show aws_vpc.main
```

### Manage Infrastructure
```bash
# Refresh state
terraform refresh

# Plan changes
terraform plan

# Apply changes
terraform apply

# Destroy infrastructure
terraform destroy
```

### AWS CLI Commands
```bash
# List VPCs
aws ec2 describe-vpcs --region eu-north-1

# List Subnets
aws ec2 describe-subnets --region eu-north-1

# List NAT Gateways
aws ec2 describe-nat-gateways --region eu-north-1

# List Route Tables
aws ec2 describe-route-tables --region eu-north-1

# List VPC Flow Logs
aws ec2 describe-flow-logs --region eu-north-1
```

---

## Troubleshooting

### Terraform Init Fails
```
Error: Error acquiring the state lock
```
**Solution:**
1. Check S3 bucket exists: `aws s3 ls | grep startup-landing-zone-terraform`
2. Check DynamoDB table: `aws dynamodb describe-table --table-name terraform-locks --region eu-north-1`
3. Check AWS credentials: `aws sts get-caller-identity`

### NAT Gateway Creation Fails
```
Error: InvalidAllocationID.NotFound
```
**Solution:**
1. Verify Elastic IP IDs: `aws ec2 describe-addresses --region eu-north-1`
2. Check IDs in terraform.tfvars match
3. Ensure IDs are not already in use

### Private Subnet Can't Reach Internet
```
No route to host
```
**Solution:**
1. Check NAT Gateway status: `aws ec2 describe-nat-gateways --region eu-north-1`
2. Verify route table: `aws ec2 describe-route-tables --region eu-north-1`
3. Check security groups allow outbound traffic

---

## Architecture Overview

```
Internet
    ↓
Internet Gateway (igw-01a55c30c9fde14b2)
    ↓
Public Subnets (10.0.0.0/24, 10.0.1.0/24)
    ↓
NAT Gateways (13.51.99.77, 13.63.12.180)
    ↓
Private Subnets (10.0.32.0/19, 10.0.64.0/19)
    ↓
Your Applications
```

---

## Cost Breakdown

| Component | Cost |
|-----------|------|
| NAT Gateways (2) | $64/month |
| Elastic IPs (2) | $7/month |
| VPC Flow Logs | $1-5/month |
| S3 Storage | $1-5/month |
| **Total** | **$73-81/month** |

---

## Key Resources

| Resource | ID |
|----------|-----|
| VPC | vpc-022a72811066aa870 |
| Internet Gateway | igw-01a55c30c9fde14b2 |
| Public Subnet 1a | subnet-05e35cee7e7de19d7 |
| Public Subnet 1b | subnet-0d9d470d83efbf855 |
| Private Subnet 1a | subnet-08f0a3f1ccb9c2a12 |
| Private Subnet 1b | subnet-036bd6a7cdd325d1f |
| NAT Gateway 1a | nat-0305d5f4eb1a16ce4 |
| NAT Gateway 1b | nat-08175d6ee16966cc1 |
| VPC Flow Logs | fl-04d77d17928eaa754 |

---

## Documentation

- **README.md** - Complete technical guide with architecture details
- **BUSINESS_GUIDE.md** - Non-technical guide for business stakeholders
- **QUICK_START.md** - This file (quick reference)
- **generated-diagrams/** - Architecture diagrams

---

## Support

### AWS Documentation
- [AWS VPC](https://docs.aws.amazon.com/vpc/)
- [AWS NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

### GitHub Repository
- **URL:** https://github.com/akhilchibber/aws-startup-landing-zone
- **Branch:** main

---

**Status:** ✅ Ready to Deploy  
**Time to Deploy:** 2 hours  
**Cost:** $73-81/month

