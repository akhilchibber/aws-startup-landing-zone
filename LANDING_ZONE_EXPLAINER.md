# AWS Startup Landing Zone - Implementation Guide

**Single Source of Truth for the Landing Zone Architecture**

## Overview

This document describes the AWS Startup Landing Zone implementation—a foundational, production-ready AWS environment designed for startups and organizations beginning their cloud journey. The landing zone provides a secure, scalable, and well-organized infrastructure foundation using Infrastructure as Code (Terraform).

**Analogy:** Think of a landing zone as preparing a city before construction. We're setting up roads (networking), electricity (connectivity), security (firewalls), and organization (tagging) before deploying applications.

---

## What We're Building

### Core Components

1. **Virtual Private Cloud (VPC)** - Isolated network environment
2. **Public Subnets** - DMZ layer for load balancers, bastion hosts, NAT gateways
3. **Private Subnets** - Application layer for compute, databases, caches
4. **Internet Gateway (IGW)** - Enables internet connectivity for public resources
5. **NAT Gateways** - Allows private resources to reach the internet securely
6. **Route Tables** - Controls traffic routing between subnets
7. **VPC Flow Logs** - Network traffic monitoring and compliance

### Architecture Diagram

See `generated-diagrams/diagram_*.png` for the visual architecture.

---

## Network Design

### VPC CIDR Block
- **CIDR:** `10.0.0.0/16`
- **Total Hosts:** 65,535 (minus 5 reserved AWS addresses per subnet)
- **Rationale:** Provides ample space for growth while maintaining security boundaries

### Public Subnets (DMZ Layer)
Purpose: Minimal exposure to internet, only load balancers and bastion hosts

| Availability Zone | CIDR        | Available Hosts | Purpose |
|-------------------|-------------|-----------------|---------|
| ap-southeast-1a   | 10.0.0.0/24 | 250             | NAT Gateway, Load Balancer |
| ap-southeast-1b   | 10.0.1.0/24 | 250             | NAT Gateway, Load Balancer |

**Key Points:**
- Small CIDR blocks (/24) to minimize attack surface
- No EC2 instances assigned public IPs (security best practice)
- All internet traffic routed through IGW

### Private Subnets (Application Layer)
Purpose: Hosts applications, databases, caches—isolated from direct internet access

| Availability Zone | CIDR         | Available Hosts | Purpose |
|-------------------|--------------|-----------------|---------|
| ap-southeast-1a   | 10.0.32.0/19 | 8,187           | Applications, Databases |
| ap-southeast-1b   | 10.0.64.0/19 | 8,187           | Applications, Databases |

**Key Points:**
- Large CIDR blocks (/19) for application workloads
- All outbound internet traffic routes through NAT Gateways
- No inbound internet access (secure by default)
- Communication to AWS services via VPC Endpoints (future enhancement)

---

## Traffic Flow

### Inbound Internet Traffic
```
Internet → Internet Gateway → Public Subnet → Load Balancer → Private Subnet (via security groups)
```

### Outbound Private Subnet Traffic
```
Private Subnet → NAT Gateway (in Public Subnet) → Internet Gateway → Internet
```

### Benefits
- **Security:** Private resources never directly exposed to internet
- **Scalability:** NAT Gateways provide high-bandwidth outbound connectivity
- **Monitoring:** VPC Flow Logs capture all traffic for compliance and troubleshooting

---

## NAT Gateways & Elastic IPs

### Why NAT Gateways?
- Provides secure outbound internet access for private resources
- Maintains connection state (stateful)
- High availability and bandwidth
- Enables third-party IP whitelisting (fixed Elastic IPs)

### Elastic IP Allocation
- **One Elastic IP per NAT Gateway** (one per availability zone)
- **Requirement:** Pre-allocate Elastic IPs before Terraform deployment
- **Cost:** ~$0.045/hour per NAT Gateway + data processing charges

---

## VPC Flow Logs

### Purpose
- Monitor network traffic for security analysis
- Troubleshoot connectivity issues
- Meet compliance requirements (audit trails)
- Detect anomalous traffic patterns

### Implementation
- **Destination:** S3 bucket (auto-created by Terraform)
- **Traffic Type:** ALL (inbound and outbound)
- **Retention:** Configurable via S3 lifecycle policies

---

## Resource Tagging Strategy

All resources are tagged with four standard tags for organization and cost allocation:

| Tag | Example | Purpose |
|-----|---------|---------|
| **Component** | `vpc`, `nat-gateway`, `private-subnet` | Identifies resource type |
| **Environment** | `d` (dev), `s` (staging), `p` (prod) | Environment classification |
| **Product** | `example`, `website`, `api` | Business unit/product |
| **Name** | `d-example-vpc` | Human-readable identifier |

**Benefits:**
- Cost allocation and chargeback
- Resource filtering and automation
- Compliance and governance
- Operational clarity

---

## Terraform Structure

### Directory Layout
```
.
├── modules/                          # Reusable Terraform modules
│   ├── vpc/                         # VPC creation
│   ├── internet-gateway/            # IGW setup
│   ├── public-subnet/               # Public subnet configuration
│   ├── private-subnet/              # Private subnet configuration
│   └── nat-gateway/                 # NAT gateway setup
│
└── environments/                     # Environment-specific configurations
    └── development/                  # Development environment
        ├── main.tf                  # Main configuration (providers, modules)
        ├── variables.tf             # Variable definitions
        ├── terraform.tfvars         # Variable values
        └── .terraform.lock.hcl      # Dependency lock file
```

### Module Design
- **Modular:** Each component (VPC, subnets, gateways) is a separate module
- **Reusable:** Modules can be used across environments
- **Testable:** Modules can be tested independently
- **Maintainable:** Clear separation of concerns

### Environment Separation
- **Development:** 2 availability zones, minimal resources
- **Staging:** 2-3 availability zones, production-like
- **Production:** 3 availability zones, high availability

---

## Prerequisites & Setup

### AWS Account Requirements
1. **AWS Access Key ID & Secret Access Key** - For Terraform authentication
2. **S3 Bucket** - For Terraform state storage (versioning enabled, encryption enabled)
3. **Elastic IP Allocations** - Pre-allocate 2 Elastic IPs (one per NAT Gateway)

### Terraform Requirements
- Terraform >= 1.0
- AWS Provider >= 3.0
- AWS CLI configured with credentials

### Environment Variables
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="ap-southeast-1"
export TF_LOG="INFO"  # Optional: for debugging
```

---

## Deployment Steps

### 1. Prepare AWS Resources
```bash
# Create S3 bucket for Terraform state
aws s3api create-bucket \
  --bucket startup-landing-zone-terraform \
  --region ap-southeast-1 \
  --create-bucket-configuration LocationConstraint=ap-southeast-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket startup-landing-zone-terraform \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket startup-landing-zone-terraform \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Allocate Elastic IPs
aws ec2 allocate-address --region ap-southeast-1
aws ec2 allocate-address --region ap-southeast-1
```

### 2. Configure Terraform
- Update `environments/development/main.tf` with your S3 bucket name
- Update `environments/development/terraform.tfvars` with your Elastic IP allocation IDs

### 3. Deploy Infrastructure
```bash
cd environments/development

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply configuration
terraform apply
```

### 4. Verify Deployment
```bash
# Check VPC creation
aws ec2 describe-vpcs --region ap-southeast-1

# Check subnets
aws ec2 describe-subnets --region ap-southeast-1

# Check NAT Gateways
aws ec2 describe-nat-gateways --region ap-southeast-1
```

---

## AWS Best Practices Implemented

### Security
✅ **Principle of Least Privilege** - Private subnets isolated from internet  
✅ **Defense in Depth** - Multiple layers (IGW, NAT, security groups)  
✅ **Encryption** - S3 bucket encryption for flow logs  
✅ **Monitoring** - VPC Flow Logs for audit trails  

### Reliability
✅ **Multi-AZ Deployment** - Resources across 2+ availability zones  
✅ **Redundancy** - NAT Gateway per AZ for high availability  
✅ **State Management** - Terraform state in versioned S3 bucket  

### Operational Excellence
✅ **Infrastructure as Code** - Version-controlled, repeatable deployments  
✅ **Tagging Strategy** - Consistent resource identification  
✅ **Modular Design** - Reusable components across environments  
✅ **Documentation** - Clear variable definitions and examples  

### Cost Optimization
✅ **Right-Sizing** - Appropriate CIDR blocks for each layer  
✅ **Shared Resources** - NAT Gateways shared across subnets in AZ  
✅ **Monitoring** - Cost allocation tags for chargeback  

---

## Next Steps (Future Enhancements)

1. **VPC Endpoints** - Private connectivity to AWS services (S3, DynamoDB, etc.)
2. **Security Groups** - Fine-grained network access control
3. **Network ACLs** - Subnet-level traffic filtering
4. **VPN/Direct Connect** - Hybrid cloud connectivity
5. **Auto Scaling** - Dynamic resource provisioning
6. **Load Balancing** - Application load distribution
7. **Monitoring & Alerting** - CloudWatch integration

---

## Troubleshooting

### Common Issues

**Issue:** Terraform state lock timeout
- **Solution:** Check S3 bucket permissions and network connectivity

**Issue:** NAT Gateway creation fails
- **Solution:** Verify Elastic IP allocation IDs are valid and available

**Issue:** Private subnet cannot reach internet
- **Solution:** Verify NAT Gateway is in AVAILABLE state and route table is configured

**Issue:** VPC Flow Logs not appearing in S3
- **Solution:** Check S3 bucket permissions and VPC Flow Logs IAM role

---

## Support & References

- [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/security/)

---

**Last Updated:** February 26, 2026  
**Version:** 1.0  
**Status:** Ready for Implementation
