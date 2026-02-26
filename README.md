# AWS Startup Landing Zone - Terraform Implementation

A production-ready, Infrastructure-as-Code implementation of an AWS Startup Landing Zone using Terraform. This project provisions a secure, scalable, and well-organized AWS network foundation.

## 📋 Overview

This repository contains a complete Terraform implementation of the AWS Startup Landing Zone reference architecture. It creates:

- **Virtual Private Cloud (VPC)** with configurable CIDR blocks
- **Public Subnets** (DMZ layer) across multiple availability zones
- **Private Subnets** (Application layer) with NAT Gateway access
- **Internet Gateway** for public subnet internet connectivity
- **NAT Gateways** for private subnet outbound internet access
- **Route Tables** with proper routing configuration
- **VPC Flow Logs** for network monitoring and compliance

## 🏗️ Architecture

See `LANDING_ZONE_EXPLAINER.md` for detailed architecture documentation and `generated-diagrams/` for visual diagrams.

### Key Components

```
Internet
    ↓
Internet Gateway
    ↓
Public Subnets (10.0.0.0/24, 10.0.1.0/24)
    ↓
NAT Gateways (with Elastic IPs)
    ↓
Private Subnets (10.0.32.0/19, 10.0.64.0/19)
    ↓
Application Workloads
```

## 📁 Project Structure

```
.
├── modules/                          # Reusable Terraform modules
│   ├── vpc/                         # VPC creation with flow logs
│   ├── internet-gateway/            # IGW setup
│   ├── public-subnet/               # Public subnet configuration
│   ├── private-subnet/              # Private subnet configuration
│   └── nat-gateway/                 # NAT gateway setup
│
├── environments/                     # Environment-specific configurations
│   └── development/                  # Development environment
│       ├── main.tf                  # Provider and module configuration
│       ├── variables.tf             # Variable definitions
│       ├── terraform.tfvars         # Variable values (customize this)
│       └── outputs.tf               # Output definitions
│
├── LANDING_ZONE_EXPLAINER.md        # Detailed architecture documentation
├── README.md                         # This file
└── generated-diagrams/              # Architecture diagrams
```

## 🚀 Quick Start

### Prerequisites

1. **AWS Account** with appropriate permissions
2. **Terraform** >= 1.0 installed
3. **AWS CLI** configured with credentials
4. **S3 Bucket** for Terraform state (with versioning and encryption)
5. **Elastic IP Allocations** (2 for development, 3 for production)

### Step 1: Prepare AWS Resources

```bash
# Create S3 bucket for Terraform state
aws s3api create-bucket \
  --bucket startup-landing-zone-terraform \
  --region eu-north-1 \
  --create-bucket-configuration LocationConstraint=eu-north-1

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

# Allocate Elastic IPs (run twice for 2 IPs)
aws ec2 allocate-address --region eu-north-1 --domain vpc
aws ec2 allocate-address --region eu-north-1 --domain vpc

# List allocated Elastic IPs
aws ec2 describe-addresses --region eu-north-1 --query 'Addresses[?Domain==`vpc`].AllocationId' --output text
```

### Step 2: Configure Terraform

1. Update `environments/development/main.tf`:
   ```hcl
   backend "s3" {
     bucket = "startup-landing-zone-terraform"  # Your bucket name
     key    = "network/dev"
     region = "eu-north-1"
   }
   ```

2. Update `environments/development/terraform.tfvars`:
   ```hcl
   aws_elastic_ip_allocation_ids = ["eipalloc-xxxxx", "eipalloc-yyyyy"]
   ```

### Step 3: Deploy Infrastructure

```bash
cd environments/development

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply configuration
terraform apply

# View outputs
terraform output
```

### Step 4: Verify Deployment

```bash
# Check VPC
aws ec2 describe-vpcs --region eu-north-1 --query 'Vpcs[0]'

# Check subnets
aws ec2 describe-subnets --region eu-north-1 --query 'Subnets[*].[SubnetId,CidrBlock,AvailabilityZone]'

# Check NAT Gateways
aws ec2 describe-nat-gateways --region eu-north-1 --query 'NatGateways[*].[NatGatewayId,State,PublicIp]'

# Check Internet Gateway
aws ec2 describe-internet-gateways --region eu-north-1
```

## 📝 Configuration

### Variables

All variables are defined in `environments/development/variables.tf`. Key variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `aws_region` | AWS region | `eu-north-1` |
| `aws_availability_zones` | List of AZs | `["eu-north-1a", "eu-north-1b"]` |
| `aws_elastic_ip_allocation_ids` | Elastic IP IDs | `["eipalloc-xxx", "eipalloc-yyy"]` |
| `vpc_cidr` | VPC CIDR block | `10.0.0.0/16` |
| `public_subnet_cidrs` | Public subnet CIDRs | `{"eu-north-1a" = "10.0.0.0/24"}` |
| `private_subnet_cidrs` | Private subnet CIDRs | `{"eu-north-1a" = "10.0.32.0/19"}` |
| `environment` | Environment code | `d` (dev), `s` (staging), `p` (prod) |
| `product` | Product name | `startup`, `website`, etc. |

### Resource Tagging

All resources are automatically tagged with:
- **Component**: Resource type (vpc, nat-gateway, etc.)
- **Environment**: Environment code (d, s, p)
- **Product**: Product name
- **Name**: Human-readable identifier

## 🔄 Multi-Environment Setup

To create additional environments (staging, production):

```bash
# Copy development environment
cp -r environments/development environments/staging

# Update terraform.tfvars for staging
# - Change aws_availability_zones to 3 zones
# - Update environment to "s"
# - Update aws_elastic_ip_allocation_ids with new IPs

# Deploy staging
cd environments/staging
terraform init
terraform apply
```

## 🔐 Security Best Practices

✅ **Implemented:**
- Private subnets isolated from internet
- NAT Gateways for secure outbound access
- VPC Flow Logs for monitoring
- S3 encryption for state and flow logs
- Terraform state versioning
- Resource tagging for compliance

✅ **Recommended Next Steps:**
- Configure Security Groups
- Enable VPC Endpoints for AWS services
- Implement Network ACLs
- Set up CloudWatch alarms
- Enable AWS Config for compliance

## 📊 Outputs

After deployment, Terraform outputs:

```
vpc_id              - VPC identifier
vpc_cidr            - VPC CIDR block
internet_gateway_id - IGW identifier
public_subnets      - Public subnet details by AZ
private_subnets     - Private subnet details by AZ
nat_gateways        - NAT Gateway IDs and public IPs
```

Access outputs:
```bash
terraform output
terraform output vpc_id
terraform output nat_gateways
```

## 🛠️ Troubleshooting

### Terraform State Lock
```bash
# If stuck on state lock
terraform force-unlock <LOCK_ID>
```

### Elastic IP Allocation Errors
```bash
# Verify EIPs are available
aws ec2 describe-addresses --region eu-north-1

# Check if EIP is already associated
aws ec2 describe-addresses --allocation-ids eipalloc-xxxxx
```

### VPC Flow Logs Not Appearing
```bash
# Check S3 bucket permissions
aws s3api get-bucket-policy --bucket vpc-flow-logs-vpc-xxxxx

# Check VPC Flow Logs status
aws ec2 describe-flow-logs --region eu-north-1
```

## 📚 Documentation

- `LANDING_ZONE_EXPLAINER.md` - Comprehensive architecture guide
- `generated-diagrams/` - Visual architecture diagrams
- [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

## 💰 Cost Estimation

**Monthly costs (approximate, eu-north-1):**
- NAT Gateway: ~$32/month per gateway + data processing
- Elastic IP: ~$3.65/month per IP (if not in use)
- VPC Flow Logs: ~$0.50/month per million records
- S3 (state + flow logs): ~$1-5/month

**Total: ~$40-80/month for development environment**

## 🔄 CI/CD Integration

Sample GitHub Actions workflow included in `_github/workflows/` (from original repo).

To use:
1. Add AWS credentials to GitHub Secrets
2. Push to repository
3. Workflow automatically runs `terraform plan` and `terraform apply`

## 📝 License

This implementation is based on the AWS Startup Landing Zone reference architecture.

## 🤝 Support

For issues or questions:
1. Check `LANDING_ZONE_EXPLAINER.md` for detailed documentation
2. Review AWS documentation links
3. Check Terraform AWS provider documentation
4. Verify AWS credentials and permissions

## 🎯 Next Steps

1. ✅ Deploy development environment
2. Deploy staging environment
3. Deploy production environment
4. Configure Security Groups
5. Set up VPC Endpoints
6. Implement monitoring and alerting
7. Document runbooks and procedures

---

**Last Updated:** February 26, 2026  
**Version:** 1.0  
**Status:** Ready for Deployment
