# AWS Startup Landing Zone - Deployment Checklist

Use this checklist to ensure successful deployment of the landing zone infrastructure.

## Pre-Deployment

### AWS Account Setup
- [ ] AWS account created and access verified
- [ ] AWS CLI installed and configured with credentials
- [ ] IAM user has AdministratorAccess or equivalent permissions
- [ ] AWS region selected (default: eu-north-1)

### Prerequisites
- [ ] Terraform >= 1.0 installed
- [ ] Git installed (for version control)
- [ ] S3 bucket created for Terraform state
- [ ] S3 bucket versioning enabled
- [ ] S3 bucket encryption enabled (AES256)
- [ ] S3 bucket public access blocked
- [ ] Elastic IPs allocated (2 for dev, 3 for prod)
- [ ] Elastic IP allocation IDs documented

### Repository Setup
- [ ] Repository cloned locally
- [ ] `.gitignore` configured
- [ ] AWS credentials NOT committed to repository
- [ ] `terraform.tfvars` customized with your values

## Configuration

### Terraform Configuration
- [ ] `environments/development/main.tf` updated with S3 bucket name
- [ ] `environments/development/terraform.tfvars` updated with:
  - [ ] AWS region
  - [ ] Availability zones
  - [ ] Elastic IP allocation IDs
  - [ ] VPC CIDR block
  - [ ] Public subnet CIDRs
  - [ ] Private subnet CIDRs
  - [ ] Environment code (d/s/p)
  - [ ] Product name

### Environment Variables
- [ ] `AWS_ACCESS_KEY_ID` set
- [ ] `AWS_SECRET_ACCESS_KEY` set
- [ ] `AWS_DEFAULT_REGION` set
- [ ] `TF_LOG` set (optional, for debugging)

## Deployment

### Terraform Initialization
- [ ] Run `terraform init` in `environments/development/`
- [ ] Verify `.terraform/` directory created
- [ ] Verify `.terraform.lock.hcl` created
- [ ] Verify S3 backend connection successful

### Terraform Validation
- [ ] Run `terraform validate`
- [ ] No validation errors reported
- [ ] Run `terraform fmt` to format code
- [ ] Review formatted changes

### Terraform Planning
- [ ] Run `terraform plan`
- [ ] Review planned resources:
  - [ ] 1 VPC
  - [ ] 1 Internet Gateway
  - [ ] 2 Public Subnets
  - [ ] 2 Private Subnets
  - [ ] 2 NAT Gateways
  - [ ] 4 Route Tables
  - [ ] VPC Flow Logs (if enabled)
  - [ ] S3 bucket for flow logs (if enabled)
- [ ] No unexpected resource deletions
- [ ] Save plan output: `terraform plan -out=tfplan`

### Terraform Apply
- [ ] Review plan one final time
- [ ] Run `terraform apply tfplan`
- [ ] Verify all resources created successfully
- [ ] No errors in apply output
- [ ] Terraform state uploaded to S3

## Post-Deployment Verification

### AWS Console Verification
- [ ] VPC created with correct CIDR block
- [ ] Internet Gateway attached to VPC
- [ ] Public subnets created in correct AZs
- [ ] Private subnets created in correct AZs
- [ ] NAT Gateways created in public subnets
- [ ] Route tables created and associated
- [ ] VPC Flow Logs enabled (if configured)
- [ ] S3 bucket created for flow logs (if enabled)

### AWS CLI Verification
```bash
# Verify VPC
aws ec2 describe-vpcs --region eu-north-1

# Verify subnets
aws ec2 describe-subnets --region eu-north-1

# Verify NAT Gateways
aws ec2 describe-nat-gateways --region eu-north-1

# Verify Internet Gateway
aws ec2 describe-internet-gateways --region eu-north-1

# Verify route tables
aws ec2 describe-route-tables --region eu-north-1
```

- [ ] VPC ID matches Terraform output
- [ ] All subnets present with correct CIDRs
- [ ] All NAT Gateways in AVAILABLE state
- [ ] All route tables properly configured
- [ ] Public route table routes to IGW
- [ ] Private route tables route to NAT Gateways

### Terraform Outputs
- [ ] Run `terraform output`
- [ ] Verify all outputs displayed:
  - [ ] vpc_id
  - [ ] vpc_cidr
  - [ ] internet_gateway_id
  - [ ] public_subnets
  - [ ] private_subnets
  - [ ] nat_gateways
- [ ] Save outputs for documentation

### Resource Tagging
- [ ] All resources have Component tag
- [ ] All resources have Environment tag
- [ ] All resources have Product tag
- [ ] All resources have Name tag
- [ ] Tags follow naming convention

## Documentation

### Documentation Updates
- [ ] Architecture diagram reviewed
- [ ] LANDING_ZONE_EXPLAINER.md reviewed
- [ ] README.md reviewed
- [ ] Outputs documented
- [ ] Deployment notes recorded

### Team Communication
- [ ] Team notified of deployment
- [ ] Access credentials shared securely
- [ ] Documentation shared with team
- [ ] Runbooks created for common tasks

## Post-Deployment Tasks

### Security Hardening
- [ ] Security Groups created for workloads
- [ ] Network ACLs reviewed (if needed)
- [ ] VPC Flow Logs verified in S3
- [ ] CloudTrail enabled for API logging
- [ ] AWS Config enabled for compliance

### Monitoring & Alerting
- [ ] CloudWatch alarms configured for NAT Gateway
- [ ] CloudWatch alarms configured for VPC Flow Logs
- [ ] SNS topics created for alerts
- [ ] Email notifications tested

### Backup & Disaster Recovery
- [ ] Terraform state backup verified
- [ ] S3 bucket replication configured (if needed)
- [ ] Disaster recovery plan documented
- [ ] Backup restoration tested

### Cost Management
- [ ] Cost allocation tags verified
- [ ] AWS Budgets configured
- [ ] Cost anomaly detection enabled
- [ ] Monthly cost review scheduled

## Additional Environments

### Staging Environment
- [ ] Copy development environment to staging
- [ ] Update terraform.tfvars for staging
- [ ] Allocate new Elastic IPs for staging
- [ ] Deploy staging environment
- [ ] Verify staging deployment

### Production Environment
- [ ] Copy development environment to production
- [ ] Update terraform.tfvars for production (3 AZs)
- [ ] Allocate new Elastic IPs for production
- [ ] Deploy production environment
- [ ] Verify production deployment
- [ ] Enable enhanced monitoring for production

## Maintenance

### Regular Tasks
- [ ] Weekly: Review VPC Flow Logs
- [ ] Monthly: Review costs and resource usage
- [ ] Monthly: Review security group rules
- [ ] Quarterly: Review and update documentation
- [ ] Quarterly: Test disaster recovery procedures

### Updates
- [ ] Monitor Terraform AWS provider updates
- [ ] Test updates in development first
- [ ] Apply updates to staging
- [ ] Apply updates to production
- [ ] Document all changes

## Rollback Plan

### If Deployment Fails
- [ ] Review error messages
- [ ] Check AWS service limits
- [ ] Verify Elastic IP availability
- [ ] Check S3 bucket permissions
- [ ] Run `terraform destroy` to rollback
- [ ] Verify all resources deleted
- [ ] Fix issues and retry

### If Issues Occur Post-Deployment
- [ ] Check VPC Flow Logs for traffic issues
- [ ] Verify route table configurations
- [ ] Check security group rules
- [ ] Review CloudWatch logs
- [ ] Contact AWS support if needed

---

## Sign-Off

- [ ] Deployment completed successfully
- [ ] All verifications passed
- [ ] Documentation updated
- [ ] Team trained on infrastructure
- [ ] Deployment date: _______________
- [ ] Deployed by: _______________
- [ ] Reviewed by: _______________

---

**Notes:**
```
[Add any additional notes or observations here]
```
