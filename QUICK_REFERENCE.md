# AWS Startup Landing Zone - Quick Reference

**TL;DR - Get started in 5 minutes**

---

## 1️⃣ Prepare AWS (2 minutes)

```bash
# Create S3 bucket
aws s3api create-bucket \
  --bucket startup-landing-zone-terraform \
  --region eu-north-1 \
  --create-bucket-configuration LocationConstraint=eu-north-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket startup-landing-zone-terraform \
  --versioning-configuration Status=Enabled

# Allocate 2 Elastic IPs
aws ec2 allocate-address --region eu-north-1 --domain vpc
aws ec2 allocate-address --region eu-north-1 --domain vpc

# Get allocation IDs
aws ec2 describe-addresses --region eu-north-1 --query 'Addresses[?Domain==`vpc`].AllocationId' --output text
```

---

## 2️⃣ Configure Terraform (2 minutes)

**File: `environments/development/main.tf`**
```hcl
backend "s3" {
  bucket = "startup-landing-zone-terraform"  # ← Your bucket name
  key    = "network/dev"
  region = "eu-north-1"
}
```

**File: `environments/development/terraform.tfvars`**
```hcl
aws_elastic_ip_allocation_ids = ["eipalloc-xxxxx", "eipalloc-yyyyy"]  # ← Your EIP IDs
```

---

## 3️⃣ Deploy (1 minute)

```bash
cd environments/development
terraform init
terraform plan
terraform apply
```

---

## 📊 What Gets Created

| Resource | Count | Details |
|----------|-------|---------|
| VPC | 1 | 10.0.0.0/16 |
| Public Subnets | 2 | 10.0.0.0/24, 10.0.1.0/24 |
| Private Subnets | 2 | 10.0.32.0/19, 10.0.64.0/19 |
| NAT Gateways | 2 | 1 per public subnet |
| Internet Gateway | 1 | For public subnet |
| Route Tables | 4 | 2 public, 2 private |
| VPC Flow Logs | 1 | S3-based monitoring |

---

## 🔍 Verify Deployment

```bash
# View outputs
terraform output

# Check VPC
aws ec2 describe-vpcs --region eu-north-1

# Check subnets
aws ec2 describe-subnets --region eu-north-1

# Check NAT Gateways
aws ec2 describe-nat-gateways --region eu-north-1
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `LANDING_ZONE_EXPLAINER.md` | Architecture details |
| `README.md` | Full deployment guide |
| `DEPLOYMENT_CHECKLIST.md` | Verification steps |
| `environments/development/terraform.tfvars` | Your configuration |
| `modules/*/main.tf` | Resource definitions |

---

## 🔧 Common Commands

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Format code
terraform fmt -recursive

# Plan changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# View outputs
terraform output

# Destroy infrastructure
terraform destroy

# View specific output
terraform output vpc_id
terraform output nat_gateways
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| S3 bucket already exists | Use unique bucket name |
| Elastic IP not available | Allocate new EIPs |
| Terraform init fails | Check AWS credentials |
| Apply fails | Check IAM permissions |
| State lock timeout | Run `terraform force-unlock <LOCK_ID>` |

---

## 💰 Costs

- **NAT Gateway:** ~$32/month each
- **Elastic IP:** ~$3.65/month each (if not in use)
- **VPC Flow Logs:** ~$0.50/month per million records
- **Total:** ~$70-80/month for development

---

## 🔐 Security Checklist

- ✅ Private subnets isolated from internet
- ✅ NAT Gateways for outbound access
- ✅ VPC Flow Logs enabled
- ✅ S3 encryption enabled
- ✅ Public access blocked on S3
- ✅ Resource tagging enabled

---

## 📚 Documentation

- **Architecture:** See `LANDING_ZONE_EXPLAINER.md`
- **Deployment:** See `README.md`
- **Verification:** See `DEPLOYMENT_CHECKLIST.md`
- **Diagram:** See `generated-diagrams/`

---

## 🎯 Next Steps

1. ✅ Deploy development environment
2. Create Security Groups
3. Deploy staging environment
4. Deploy production environment
5. Set up monitoring and alerts

---

## 📞 Support

- Check documentation files
- Review AWS documentation
- Check Terraform AWS provider docs
- Verify AWS credentials and permissions

---

**Ready to deploy? Start with Step 1 above!**
