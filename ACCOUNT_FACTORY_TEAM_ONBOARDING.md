# AWS Hospital Account Factory - Team Onboarding Guide

**Purpose:** Guide for hospital teams to request and use their new AWS account  
**Audience:** Hospital team leads, developers, DevOps engineers  
**Status:** Ready for teams  
**Last Updated:** February 26, 2026

---

## Welcome to AWS Hospital Landing Zone

Your hospital team now has access to AWS through our automated Account Factory. This guide will help you request an account, access it, and start deploying applications.

---

## Part 1: Request Your AWS Account

### Step 1: Gather Required Information

Before submitting your request, gather these 10 pieces of information:

| # | Question | Example | Notes |
|---|----------|---------|-------|
| 1 | Team Name | `radiology-team` | Lowercase, hyphens/underscores only |
| 2 | Team Lead | `Dr. John Smith` | Primary contact for the account |
| 3 | Team Email | `radiology-team@hospital.com` | Must be hospital domain |
| 4 | Cost Center | `CC-RADIOLOGY-001` | Format: CC-DEPARTMENT-XXX |
| 5 | Data Classification | `Confidential` | Public / Internal / Confidential / Restricted |
| 6 | Business Criticality | `High` | Low / Medium / High / Critical |
| 7 | Primary Use Case | `Medical Imaging` | EHR, Telemedicine, Lab System, etc. |
| 8 | Monthly Budget | `$5,000` | Between $100-$100,000 |
| 9 | Additional Services | `RDS, S3` | Optional: RDS, S3, Lambda, DynamoDB, etc. |
| 10 | Compliance | `HIPAA, HITECH` | HIPAA, HITECH, SOC 2, PCI DSS, GDPR |

### Step 2: Submit Account Request

1. Go to the GitHub repository
2. Click **Issues** → **New Issue**
3. Select **AWS Account Request** template
4. Fill in all 10 fields with your information
5. Check the checklist at the bottom
6. Click **Submit new issue**

### Step 3: Wait for Automatic Provisioning

The system will automatically:
- ✅ Validate your submission (1-2 minutes)
- ✅ Create your AWS account (2-3 minutes)
- ✅ Set up 3 environments: dev, staging, prod (3-5 minutes)
- ✅ Deploy landing zone infrastructure to each environment
- ✅ Send you credentials via email

**Total Time:** 5-10 minutes

### Step 4: Receive Credentials

Check your email (the one you provided in the form) for:
- AWS Account ID
- Temporary credentials
- Console login link
- Initial password

**Important:** Change your password on first login.

---

## Part 2: Access Your AWS Account

### Step 1: First Login

1. Click the console login link from your email
2. Enter your username and temporary password
3. Change your password to something secure
4. Enable MFA (Multi-Factor Authentication)

### Step 2: Understand Your Account Structure

Your account has 3 environments:

```
Your AWS Account
├── Dev Environment (10.0.0.0/16)
│   ├── VPC with 2 public subnets
│   ├── 2 private subnets
│   ├── NAT Gateways for outbound traffic
│   └── Internet Gateway for inbound traffic
│
├── Staging Environment (10.1.0.0/16)
│   ├── VPC with 2 public subnets
│   ├── 2 private subnets
│   ├── NAT Gateways for outbound traffic
│   └── Internet Gateway for inbound traffic
│
└── Prod Environment (10.2.0.0/16)
    ├── VPC with 2 public subnets
    ├── 2 private subnets
    ├── NAT Gateways for outbound traffic
    └── Internet Gateway for inbound traffic
```

### Step 3: View Your Infrastructure

In the AWS Console:

1. Go to **VPC** → **Your VPCs**
2. You should see 3 VPCs:
   - `radiology-team-dev-vpc` (10.0.0.0/16)
   - `radiology-team-staging-vpc` (10.1.0.0/16)
   - `radiology-team-prod-vpc` (10.2.0.0/16)

3. Click on each VPC to see:
   - Subnets (public and private)
   - Route tables
   - NAT Gateways
   - Internet Gateway

---

## Part 3: Deploy Your Application

### Step 1: Choose Your Environment

- **Dev:** For development and testing (no cost controls)
- **Staging:** For pre-production testing (cost alerts at 80%)
- **Prod:** For production workloads (cost alerts at 80%, hard limit at 100%)

### Step 2: Deploy to Private Subnet (Recommended)

For security, deploy applications to private subnets:

```
Internet → Internet Gateway → Public Subnet → NAT Gateway → Private Subnet → Your Application
```

**Benefits:**
- Applications not directly exposed to internet
- Outbound traffic goes through NAT Gateway
- Inbound traffic controlled via security groups

### Step 3: Deploy to Public Subnet (If Needed)

For public-facing applications:

```
Internet → Internet Gateway → Public Subnet → Your Application
```

**Use Cases:**
- Web servers
- Load balancers
- API gateways

### Step 4: Example: Launch an EC2 Instance

```bash
# 1. Go to EC2 Dashboard
# 2. Click "Launch Instance"
# 3. Choose AMI (Amazon Linux 2 recommended)
# 4. Choose instance type (t3.micro for testing)
# 5. Configure instance details:
#    - Network: Select your VPC (e.g., radiology-team-dev-vpc)
#    - Subnet: Select private subnet (recommended)
#    - Auto-assign Public IP: No (for private subnet)
# 6. Add storage (default 8GB is fine)
# 7. Add tags:
#    - Name: my-app-instance
#    - Environment: dev
#    - Team: radiology-team
# 8. Configure security group:
#    - Allow SSH from your IP (for management)
#    - Allow HTTP/HTTPS if needed
# 9. Review and launch
# 10. Create or select key pair for SSH access
```

---

## Part 4: Manage Costs

### Step 1: Set Budget Alerts

Your account has automatic budget alerts:
- **80% of budget:** Warning email
- **100% of budget:** Critical email

Example: If your budget is $5,000/month:
- Alert at $4,000 spent
- Alert at $5,000 spent

### Step 2: Monitor Spending

In AWS Console:

1. Go to **Billing** → **Cost Explorer**
2. View spending by service
3. View spending by tag (Environment, Team, etc.)
4. Set custom date ranges

### Step 3: Optimize Costs

- Use **dev** environment for testing (stop instances when not in use)
- Use **staging** for pre-production (similar to prod)
- Use **prod** only for production workloads
- Delete unused resources (EC2 instances, RDS databases, etc.)
- Use Reserved Instances for predictable workloads

### Step 4: Request Budget Increase

If you need more budget:

1. Contact: cloud-team@hospital.com
2. Provide:
   - Current spending
   - Reason for increase
   - New budget amount
   - Business justification

---

## Part 5: Security Best Practices

### Step 1: Enable MFA

1. Go to **IAM** → **Users** → Your username
2. Click **Security credentials**
3. Click **Assign MFA device**
4. Choose device type (authenticator app recommended)
5. Scan QR code with authenticator app
6. Enter two consecutive codes

### Step 2: Use IAM Roles (Not Access Keys)

For applications running on EC2:

1. Create IAM role with required permissions
2. Attach role to EC2 instance
3. Application automatically gets temporary credentials
4. No need to store access keys

### Step 3: Use Security Groups

Security groups act as firewalls:

```
# Example: Allow SSH from your office
Inbound Rule:
- Type: SSH (port 22)
- Source: Your office IP (e.g., 203.0.113.0/32)

# Example: Allow HTTP/HTTPS from internet
Inbound Rule:
- Type: HTTP (port 80)
- Source: 0.0.0.0/0 (anywhere)

Inbound Rule:
- Type: HTTPS (port 443)
- Source: 0.0.0.0/0 (anywhere)
```

### Step 4: Enable VPC Flow Logs

VPC Flow Logs are already enabled for your account. They capture:
- All network traffic
- Source and destination IPs
- Ports and protocols
- Accept/reject decisions

View logs in CloudWatch:
1. Go to **CloudWatch** → **Log Groups**
2. Find `/aws/vpc/flowlogs/radiology-team-dev`
3. View traffic patterns

### Step 5: Use Encryption

- **Data in Transit:** Use HTTPS/TLS
- **Data at Rest:** Enable encryption on RDS, S3, EBS volumes
- **Secrets:** Use AWS Secrets Manager (not hardcoded)

---

## Part 6: Troubleshooting

### Issue: Can't access AWS Console

**Solution:**
1. Check email for correct login link
2. Verify username and password
3. Check if MFA device is working
4. Contact: cloud-team@hospital.com

### Issue: Can't launch EC2 instance

**Solution:**
1. Verify you're in correct region (eu-north-1)
2. Verify you selected correct VPC
3. Verify security group allows required ports
4. Check account budget hasn't been exceeded

### Issue: Application can't reach internet

**Solution:**
1. If in private subnet: Verify NAT Gateway is running
2. If in public subnet: Verify Internet Gateway is attached
3. Check route table has correct routes
4. Check security group allows outbound traffic

### Issue: High AWS bill

**Solution:**
1. Go to **Cost Explorer** and identify expensive services
2. Stop unused EC2 instances
3. Delete unused RDS databases
4. Delete unused EBS volumes
5. Contact: cloud-team@hospital.com for help

---

## Part 7: Additional Resources

### Documentation
- [Hospital Landing Zone Architecture](README.md)
- [Account Factory Implementation](ACCOUNT_FACTORY_IMPLEMENTATION.md)
- [Intake Form Details](ACCOUNT_FACTORY_INTAKE_FORM.md)

### AWS Services Available
- **Compute:** EC2, Lambda, ECS, Fargate
- **Database:** RDS (PostgreSQL, MySQL, MariaDB), DynamoDB
- **Storage:** S3, EBS, EFS
- **Networking:** VPC, NAT Gateway, Internet Gateway, Route 53
- **Monitoring:** CloudWatch, VPC Flow Logs
- **Security:** IAM, Security Groups, KMS, Secrets Manager

### AWS Training
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Training and Certification](https://aws.amazon.com/training/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

---

## Part 8: Getting Help

### Support Channels

| Issue | Contact | Response Time |
|-------|---------|----------------|
| Account access problems | cloud-team@hospital.com | 1 hour |
| Billing questions | cloud-team@hospital.com | 2 hours |
| Technical questions | cloud-team@hospital.com | 4 hours |
| Emergency (production down) | cloud-team@hospital.com | 15 minutes |

### Information to Provide

When contacting support, include:
- Your team name
- AWS Account ID
- Environment (dev/staging/prod)
- Description of issue
- Steps you've already tried
- Error messages (if any)

---

## Checklist: Getting Started

- [ ] Submitted account request via GitHub issue
- [ ] Received credentials via email
- [ ] Logged into AWS Console
- [ ] Changed initial password
- [ ] Enabled MFA
- [ ] Viewed your 3 VPCs
- [ ] Reviewed security groups
- [ ] Deployed test application
- [ ] Verified application is running
- [ ] Checked billing/cost alerts
- [ ] Read security best practices
- [ ] Bookmarked support contact

---

## Next Steps

1. **Deploy Your Application**
   - Choose dev environment for initial testing
   - Use private subnets for security
   - Enable VPC Flow Logs for monitoring

2. **Set Up CI/CD**
   - Use GitHub Actions or similar
   - Deploy to dev automatically on push
   - Manual approval for staging/prod

3. **Monitor and Optimize**
   - Use CloudWatch for monitoring
   - Use Cost Explorer for cost optimization
   - Review security regularly

4. **Scale to Production**
   - Test thoroughly in dev/staging
   - Deploy to prod with confidence
   - Monitor production workloads

---

## Questions?

Contact the cloud team: **cloud-team@hospital.com**

We're here to help you succeed with AWS!

---

**Last Updated:** February 26, 2026  
**Version:** 1.0
