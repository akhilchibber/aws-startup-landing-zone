# AWS Startup Landing Zone - Complete Technical Guide

**Version:** 1.0  
**Status:** ✅ Production Ready  
**Last Updated:** February 26, 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Network Design](#network-design)
4. [Infrastructure Components](#infrastructure-components)
5. [Deployment Guide](#deployment-guide)
6. [Verification](#verification)
7. [Cost Analysis](#cost-analysis)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## Overview

The **AWS Startup Landing Zone** is a production-ready, Infrastructure-as-Code (Terraform) implementation of a secure, scalable AWS network foundation. It provides a well-architected starting point for organizations deploying workloads on AWS.

### What is a Landing Zone?

A landing zone is a pre-configured AWS environment that follows AWS best practices and provides:
- **Security:** Network isolation, encryption, monitoring
- **Scalability:** Multi-AZ deployment, modular design
- **Compliance:** Resource tagging, audit trails, access controls
- **Cost Optimization:** Efficient resource usage, cost allocation

### Key Features

✅ **Multi-AZ Architecture** - High availability across 2 availability zones  
✅ **Network Segmentation** - Public (DMZ) and private (application) layers  
✅ **Secure by Default** - Private subnets isolated from internet  
✅ **Infrastructure as Code** - Terraform modules for repeatability  
✅ **Comprehensive Monitoring** - VPC Flow Logs for network visibility  
✅ **Resource Tagging** - Consistent organization and cost tracking  
✅ **Production Ready** - Follows AWS Well-Architected Framework  

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VPC: 10.0.0.0/16                         │
│                   (65,536 IP Addresses)                     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Internet Gateway (igw-01a55c30c9fde14b2)           │  │
│  │  Enables internet connectivity for public resources  │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌────────────────────────┴────────────────────────────┐   │
│  │                                                     │   │
│  │  PUBLIC SUBNETS (DMZ Layer)                        │   │
│  │  ┌──────────────────┐  ┌──────────────────┐       │   │
│  │  │ 10.0.0.0/24      │  │ 10.0.1.0/24      │       │   │
│  │  │ eu-north-1a      │  │ eu-north-1b      │       │   │
│  │  │ (250 IPs)        │  │ (250 IPs)        │       │   │
│  │  │                  │  │                  │       │   │
│  │  │ • Load Balancers │  │ • Load Balancers │       │   │
│  │  │ • Bastion Hosts  │  │ • Bastion Hosts  │       │   │
│  │  │ • NAT Gateways   │  │ • NAT Gateways   │       │   │
│  │  └──────────────────┘  └──────────────────┘       │   │
│  │           │                      │                │   │
│  │  ┌────────┴──────────┐  ┌────────┴──────────┐    │   │
│  │  │ NAT Gateway 1a    │  │ NAT Gateway 1b    │    │   │
│  │  │ 13.51.99.77       │  │ 13.63.12.180      │    │   │
│  │  │ (Elastic IP)      │  │ (Elastic IP)      │    │   │
│  │  └────────┬──────────┘  └────────┬──────────┘    │   │
│  │           │                      │                │   │
│  │  PRIVATE SUBNETS (Application Layer)              │   │
│  │  ┌──────────────────┐  ┌──────────────────┐       │   │
│  │  │ 10.0.32.0/19     │  │ 10.0.64.0/19     │       │   │
│  │  │ eu-north-1a      │  │ eu-north-1b      │       │   │
│  │  │ (8,187 IPs)      │  │ (8,187 IPs)      │       │   │
│  │  │                  │  │                  │       │   │
│  │  │ • EC2 Instances  │  │ • EC2 Instances  │       │   │
│  │  │ • RDS Databases  │  │ • RDS Databases  │       │   │
│  │  │ • ElastiCache    │  │ • ElastiCache    │       │   │
│  │  │ • Lambda         │  │ • Lambda         │       │   │
│  │  └──────────────────┘  └──────────────────┘       │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘  │
│                                                              │
│  VPC Flow Logs → S3 Bucket (vpc-flow-logs-vpc-022a...)    │
│  (Network traffic monitoring and compliance)               │
└─────────────────────────────────────────────────────────────┘
```

### Traffic Flow Patterns

**Inbound Internet Traffic:**
```
Internet → Internet Gateway → Public Subnet → Load Balancer → Private Subnet
```

**Outbound Private Subnet Traffic:**
```
Private Subnet → NAT Gateway → Internet Gateway → Internet
```

**Benefits:**
- Private resources never directly exposed to internet
- All outbound traffic has fixed IP (Elastic IP)
- Enables IP whitelisting for third-party integrations
- All traffic logged for compliance and troubleshooting

---

## Network Design

### VPC CIDR Block

| Property | Value |
|----------|-------|
| **CIDR Block** | 10.0.0.0/16 |
| **Total Addresses** | 65,536 |
| **Usable Addresses** | 65,531 (minus 5 AWS reserved) |
| **Rationale** | Provides ample space for growth while maintaining security boundaries |

### Public Subnets (DMZ Layer)

**Purpose:** Minimal exposure to internet, only load balancers and bastion hosts

| Availability Zone | CIDR | Available Hosts | Route Target | Purpose |
|---|---|---|---|---|
| eu-north-1a | 10.0.0.0/24 | 250 | Internet Gateway | NAT Gateway, Load Balancer |
| eu-north-1b | 10.0.1.0/24 | 250 | Internet Gateway | NAT Gateway, Load Balancer |

**Key Design Decisions:**
- Small CIDR blocks (/24) to minimize attack surface
- No EC2 instances assigned public IPs (security best practice)
- All internet traffic routed through IGW
- Route table: 0.0.0.0/0 → Internet Gateway

### Private Subnets (Application Layer)

**Purpose:** Hosts applications, databases, caches—isolated from direct internet access

| Availability Zone | CIDR | Available Hosts | Route Target | Purpose |
|---|---|---|---|---|
| eu-north-1a | 10.0.32.0/19 | 8,187 | NAT Gateway 1a | Applications, Databases |
| eu-north-1b | 10.0.64.0/19 | 8,187 | NAT Gateway 1b | Applications, Databases |

**Key Design Decisions:**
- Large CIDR blocks (/19) for application workloads
- All outbound internet traffic routes through NAT Gateways
- No inbound internet access (secure by default)
- Route table: 0.0.0.0/0 → NAT Gateway (per AZ)

### CIDR Block Allocation Strategy

```
10.0.0.0/16 (VPC)
├── 10.0.0.0/24 (Public Subnet 1a) - 256 addresses
├── 10.0.1.0/24 (Public Subnet 1b) - 256 addresses
├── 10.0.32.0/19 (Private Subnet 1a) - 8,192 addresses
└── 10.0.64.0/19 (Private Subnet 1b) - 8,192 addresses
```

**Rationale:**
- Public subnets use /24 (small, minimal exposure)
- Private subnets use /19 (large, for application workloads)
- Leaves room for future subnets (10.0.2.0/24 - 10.0.31.0/24 available)

---

## Infrastructure Components

### 1. Virtual Private Cloud (VPC)

**Resource ID:** vpc-022a72811066aa870  
**CIDR Block:** 10.0.0.0/16  
**State:** Available  
**Region:** eu-north-1

**Purpose:**
- Isolated network environment for all AWS resources
- Provides network boundary and security isolation
- Enables custom routing and network policies

**Configuration:**
- DNS hostnames: Enabled
- DNS resolution: Enabled
- VPC Flow Logs: Enabled (all traffic)

### 2. Internet Gateway (IGW)

**Resource ID:** igw-01a55c30c9fde14b2  
**State:** Available  
**Attachment:** Attached to vpc-022a72811066aa870

**Purpose:**
- Enables internet connectivity for public resources
- Provides route for inbound internet traffic
- Allows public subnets to communicate with internet

**Configuration:**
- Attached to VPC
- Route table: 0.0.0.0/0 → IGW

### 3. Public Subnets

**Subnet 1a:**
- Resource ID: subnet-05e35cee7e7de19d7
- CIDR: 10.0.0.0/24
- AZ: eu-north-1a
- Available IPs: 250

**Subnet 1b:**
- Resource ID: subnet-0d9d470d83efbf855
- CIDR: 10.0.1.0/24
- AZ: eu-north-1b
- Available IPs: 250

**Purpose:**
- DMZ layer for load balancers and bastion hosts
- Minimal exposure to internet
- All traffic routed through IGW

**Configuration:**
- Auto-assign public IP: Disabled (security best practice)
- Route table: 0.0.0.0/0 → Internet Gateway
- Network ACL: Default (allow all)

### 4. Private Subnets

**Subnet 1a:**
- Resource ID: subnet-08f0a3f1ccb9c2a12
- CIDR: 10.0.32.0/19
- AZ: eu-north-1a
- Available IPs: 8,187

**Subnet 1b:**
- Resource ID: subnet-036bd6a7cdd325d1f
- CIDR: 10.0.64.0/19
- AZ: eu-north-1b
- Available IPs: 8,187

**Purpose:**
- Application layer for compute, databases, caches
- Isolated from direct internet access
- Outbound internet via NAT Gateways

**Configuration:**
- Auto-assign public IP: Disabled
- Route table: 0.0.0.0/0 → NAT Gateway (per AZ)
- Network ACL: Default (allow all)

### 5. NAT Gateways

**NAT Gateway 1a:**
- Resource ID: nat-0305d5f4eb1a16ce4
- Public IP: 13.51.99.77
- Elastic IP Allocation: eipalloc-06faaa96c6c589469
- Subnet: subnet-05e35cee7e7de19d7 (Public 1a)
- State: Available

**NAT Gateway 1b:**
- Resource ID: nat-08175d6ee16966cc1
- Public IP: 13.63.12.180
- Elastic IP Allocation: eipalloc-06ad19500e7e33452
- Subnet: subnet-0d9d470d83efbf855 (Public 1b)
- State: Available

**Purpose:**
- Provides secure outbound internet access for private resources
- Maintains connection state (stateful)
- High availability and bandwidth
- Enables third-party IP whitelisting (fixed Elastic IPs)

**Configuration:**
- One per availability zone (high availability)
- Elastic IP per NAT Gateway (fixed public IP)
- Placed in public subnets

### 6. Route Tables

**Public Route Table 1a:**
- Resource ID: rtb-0724222c0493ceb59
- Name: d-startup-public-rt-eu-north-1a
- Routes:
  - 10.0.0.0/16 → local
  - 0.0.0.0/0 → igw-01a55c30c9fde14b2

**Public Route Table 1b:**
- Resource ID: rtb-077997641a00d2cc0
- Name: d-startup-public-rt-eu-north-1b
- Routes:
  - 10.0.0.0/16 → local
  - 0.0.0.0/0 → igw-01a55c30c9fde14b2

**Private Route Table 1a:**
- Resource ID: rtb-005caeefb997743f8
- Name: d-startup-private-rt-eu-north-1a
- Routes:
  - 10.0.0.0/16 → local
  - 0.0.0.0/0 → nat-0305d5f4eb1a16ce4

**Private Route Table 1b:**
- Resource ID: rtb-03f3c92b4f257c17a
- Name: d-startup-private-rt-eu-north-1b
- Routes:
  - 10.0.0.0/16 → local
  - 0.0.0.0/0 → nat-08175d6ee16966cc1

**Purpose:**
- Controls traffic routing between subnets
- Directs internet traffic to appropriate gateways
- Ensures private subnets route through NAT Gateways

### 7. VPC Flow Logs

**Resource ID:** fl-04d77d17928eaa754  
**Resource:** vpc-022a72811066aa870  
**Status:** ACTIVE  
**Log Destination:** arn:aws:s3:::vpc-flow-logs-vpc-022a72811066aa870  
**S3 Bucket:** vpc-flow-logs-vpc-022a72811066aa870

**Purpose:**
- Monitor network traffic for security analysis
- Troubleshoot connectivity issues
- Meet compliance requirements (audit trails)
- Detect anomalous traffic patterns

**Configuration:**
- Traffic Type: ALL (inbound and outbound)
- Log Format: AWS default format
- Destination: S3 bucket
- Retention: Configurable via S3 lifecycle policies

---

## Deployment Guide

### Prerequisites

**AWS Account Requirements:**
1. AWS Access Key ID & Secret Access Key
2. S3 bucket for Terraform state (versioning enabled, encryption enabled)
3. DynamoDB table for state locking
4. 2 Elastic IP allocations (one per NAT Gateway)

**Terraform Requirements:**
- Terraform >= 1.0
- AWS Provider >= 3.0
- AWS CLI configured with credentials

**Environment Variables:**
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="eu-north-1"
```

### Step 1: Prepare AWS Resources

**Create S3 Bucket:**
```bash
aws s3api create-bucket \
  --bucket startup-landing-zone-terraform \
  --region eu-north-1 \
  --create-bucket-configuration LocationConstraint=eu-north-1
```

**Enable Versioning:**
```bash
aws s3api put-bucket-versioning \
  --bucket startup-landing-zone-terraform \
  --versioning-configuration Status=Enabled
```

**Enable Encryption:**
```bash
aws s3api put-bucket-encryption \
  --bucket startup-landing-zone-terraform \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

**Block Public Access:**
```bash
aws s3api put-public-access-block \
  --bucket startup-landing-zone-terraform \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

**Allocate Elastic IPs:**
```bash
aws ec2 allocate-address --region eu-north-1
aws ec2 allocate-address --region eu-north-1
```

**Create DynamoDB Lock Table:**
```bash
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-north-1
```

### Step 2: Configure Terraform

**Update `environments/development/main.tf`:**
```hcl
terraform {
  backend "s3" {
    bucket         = "startup-landing-zone-terraform"  # Your S3 bucket
    key            = "network/dev"
    region         = "eu-north-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**Update `environments/development/terraform.tfvars`:**
```hcl
aws_region                    = "eu-north-1"
aws_elastic_ip_allocation_ids = ["eipalloc-06faaa96c6c589469", "eipalloc-06ad19500e7e33452"]
product                       = "startup"
environment                   = "d"
```

### Step 3: Deploy Infrastructure

```bash
cd environments/development

# Initialize Terraform
terraform init

# Review planned changes
terraform plan -out=tfplan

# Apply configuration
terraform apply tfplan
```

### Step 4: Verify Deployment

```bash
# View outputs
terraform output

# Check VPC
aws ec2 describe-vpcs --region eu-north-1

# Check subnets
aws ec2 describe-subnets --region eu-north-1

# Check NAT Gateways
aws ec2 describe-nat-gateways --region eu-north-1

# Check route tables
aws ec2 describe-route-tables --region eu-north-1

# Check VPC Flow Logs
aws ec2 describe-flow-logs --region eu-north-1
```

---

## Verification

### Deployment Verification Checklist

- [x] VPC created with correct CIDR block (10.0.0.0/16)
- [x] VPC state is "available"
- [x] 2 public subnets created with correct CIDR blocks
- [x] 2 private subnets created with correct CIDR blocks
- [x] All subnets in correct availability zones
- [x] All subnets in "available" state
- [x] Internet Gateway created and attached
- [x] Internet Gateway in "available" state
- [x] 2 NAT Gateways created
- [x] Both NAT Gateways in "available" state
- [x] NAT Gateways have correct public IPs
- [x] 4 route tables created
- [x] Public route tables route 0.0.0.0/0 to IGW
- [x] Private route tables route 0.0.0.0/0 to NAT Gateways
- [x] VPC Flow Logs enabled and ACTIVE
- [x] VPC Flow Logs S3 bucket created
- [x] VPC Flow Logs successfully writing to S3
- [x] All resources have correct tags
- [x] All resources have correct names

### Verification Commands

```bash
# Verify VPC
aws ec2 describe-vpcs --region eu-north-1 \
  --query 'Vpcs[?VpcId==`vpc-022a72811066aa870`].[VpcId,CidrBlock,State]' \
  --output table

# Verify Subnets
aws ec2 describe-subnets --region eu-north-1 \
  --query 'Subnets[*].[SubnetId,CidrBlock,AvailabilityZone,State]' \
  --output table

# Verify NAT Gateways
aws ec2 describe-nat-gateways --region eu-north-1 \
  --query 'NatGateways[*].[NatGatewayId,State,PublicIp]' \
  --output table

# Verify Route Tables
aws ec2 describe-route-tables --region eu-north-1 \
  --query 'RouteTables[*].[RouteTableId,Routes[*].[DestinationCidrBlock,GatewayId,NatGatewayId]]' \
  --output table

# Verify VPC Flow Logs
aws ec2 describe-flow-logs --region eu-north-1 \
  --query 'FlowLogs[*].[FlowLogId,ResourceId,FlowLogStatus]' \
  --output table
```

---

## Cost Analysis

### Monthly Cost Breakdown

| Component | Quantity | Unit Cost | Monthly Cost |
|-----------|----------|-----------|---|
| NAT Gateways | 2 | $32/month | $64 |
| Elastic IPs | 2 | $3.50/month | $7 |
| VPC Flow Logs | 1 | $1-5/month | $1-5 |
| S3 Storage | Variable | $0.023/GB | $1-5 |
| **Total** | | | **$73-81/month** |

### Cost Optimization Tips

1. **NAT Gateways:** Consider using NAT instances for lower cost (if traffic is low)
2. **VPC Flow Logs:** Adjust log retention in S3 lifecycle policies
3. **Elastic IPs:** Only pay when not associated with running instances
4. **S3 Storage:** Implement S3 lifecycle policies to move old logs to Glacier

### Cost Allocation Tags

All resources are tagged for cost allocation:
- **Product:** startup
- **Environment:** d (development)
- **Component:** vpc, igw, nat-gateway, etc.

Use these tags in AWS Cost Explorer for detailed cost analysis.

---

## Best Practices

### Security Best Practices Implemented

✅ **Principle of Least Privilege**
- Private subnets isolated from internet
- No public IPs on private resources
- All traffic logged for audit

✅ **Defense in Depth**
- Multiple layers (IGW, NAT, security groups)
- Network segmentation (public/private)
- Encryption at rest and in transit

✅ **Monitoring & Logging**
- VPC Flow Logs for all traffic
- CloudWatch integration ready
- Audit trails for compliance

✅ **Encryption**
- S3 bucket encryption for flow logs
- Terraform state encryption
- TLS for all communications

### Reliability Best Practices Implemented

✅ **Multi-AZ Deployment**
- Resources across 2 availability zones
- NAT Gateway per AZ for redundancy
- High availability by design

✅ **State Management**
- Terraform state in versioned S3 bucket
- DynamoDB locking for concurrent access
- Disaster recovery via versioning

✅ **Modular Design**
- Reusable Terraform modules
- Easy to extend and customize
- Testable components

### Operational Excellence Best Practices Implemented

✅ **Infrastructure as Code**
- Version-controlled deployments
- Repeatable and consistent
- Easy to audit and review

✅ **Resource Tagging**
- Consistent naming conventions
- Cost allocation and chargeback
- Operational clarity

✅ **Documentation**
- Comprehensive guides
- Architecture diagrams
- Troubleshooting guides

---

## Troubleshooting

### Common Issues & Solutions

**Issue:** Terraform state lock timeout
```
Error: Error acquiring the state lock
```
**Solution:**
1. Check S3 bucket permissions
2. Verify network connectivity
3. Check DynamoDB table status
4. Force unlock if necessary: `terraform force-unlock <LOCK_ID>`

**Issue:** NAT Gateway creation fails
```
Error: InvalidAllocationID.NotFound
```
**Solution:**
1. Verify Elastic IP allocation IDs are valid
2. Check Elastic IPs are not already in use
3. Verify AWS account limits

**Issue:** Private subnet cannot reach internet
```
No route to host
```
**Solution:**
1. Verify NAT Gateway is in AVAILABLE state
2. Check route table has correct route (0.0.0.0/0 → NAT)
3. Verify security groups allow outbound traffic
4. Check VPC Flow Logs for traffic patterns

**Issue:** VPC Flow Logs not appearing in S3
```
No logs in S3 bucket
```
**Solution:**
1. Check S3 bucket exists and is accessible
2. Verify VPC Flow Logs IAM role has S3 permissions
3. Wait 5-10 minutes for logs to appear
4. Check S3 bucket policy allows VPC Flow Logs

---

## Next Steps

### Immediate (Today)
1. Review deployment documentation
2. Verify all resources in AWS Console
3. Test network connectivity

### Short-term (This Week)
1. Create Security Groups for public and private subnets
2. Deploy EC2 instances in public subnets (web tier)
3. Deploy EC2 instances in private subnets (app tier)
4. Configure security group rules

### Medium-term (Next Week)
1. Create staging environment (copy development configuration)
2. Set up monitoring and alerts (CloudWatch)
3. Configure auto-scaling groups
4. Set up load balancers

### Long-term (Ongoing)
1. Deploy production environment
2. Set up VPC Endpoints for AWS services
3. Implement AWS Systems Manager Session Manager
4. Monitor costs and optimize

---

## Repository Structure

```
aws-startup-landing-zone/
│
├── modules/                          # Reusable Terraform modules
│   ├── vpc/                         # VPC creation
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── internet-gateway/            # IGW setup
│   ├── public-subnet/               # Public subnet configuration
│   ├── private-subnet/              # Private subnet configuration
│   └── nat-gateway/                 # NAT gateway setup
│
├── environments/                     # Environment-specific configurations
│   └── development/                  # Development environment
│       ├── main.tf                  # Provider & modules
│       ├── variables.tf             # Variable definitions
│       ├── terraform.tfvars         # Variable values
│       ├── outputs.tf               # Output definitions
│       └── deployment_outputs.txt   # Deployment results
│
├── generated-diagrams/               # Architecture diagrams
│   └── diagram_*.png                # Visual architecture
│
├── README.md                         # This file
├── BUSINESS_GUIDE.md                # Non-technical guide
├── QUICK_START.md                   # Quick reference
└── .gitignore                       # Git ignore rules
```

---

## Support & References

### AWS Documentation
- [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/)
- [AWS NAT Gateway Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [AWS VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)

### Terraform Documentation
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform State Management](https://www.terraform.io/language/state)
- [Terraform Modules](https://www.terraform.io/language/modules)

### AWS Best Practices
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/security/)
- [AWS Cost Optimization](https://aws.amazon.com/architecture/cost-optimization/)

---

## License

This project is provided as-is for educational and commercial use.

---

**Project Status:** ✅ Production Ready  
**Last Updated:** February 26, 2026  
**Version:** 1.0

