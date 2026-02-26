# AWS Hospital Account Factory - Testing & Deployment Guide

**Purpose:** Guide for testing the account factory before launching to hospital teams  
**Status:** Ready for testing  
**Last Updated:** February 26, 2026

---

## Prerequisites

Before testing, ensure you have:

1. **AWS Organization Setup**
   - AWS Organization created
   - Organization Unit (OU) ID for account creation
   - Management account with Organizations API access

2. **GitHub Setup**
   - Repository with account factory code
   - GitHub Actions enabled
   - GitHub secrets configured (see below)

3. **Terraform State Backend**
   - S3 bucket for Terraform state
   - DynamoDB table for state locking
   - Encryption enabled

4. **IAM Permissions**
   - Permission to create AWS accounts via Organizations API
   - Permission to assume cross-account roles
   - Permission to manage VPCs, subnets, NAT gateways, etc.

---

## GitHub Secrets Configuration

Configure these secrets in your GitHub repository:

```
AWS_ROLE_TO_ASSUME
  Description: ARN of IAM role to assume for account provisioning
  Format: arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME
  Example: arn:aws:iam::123456789012:role/GitHubActionsRole

TERRAFORM_STATE_BUCKET
  Description: S3 bucket name for Terraform state
  Example: hospital-terraform-state

TERRAFORM_LOCK_TABLE
  Description: DynamoDB table name for Terraform locks
  Example: terraform-locks
```

---

## Step 1: Verify Terraform Modules

### 1.1 Validate Module Syntax

```bash
# Validate account factory module
cd modules/account-factory
terraform init
terraform validate

# Validate environment module
cd ../environment
terraform init
terraform validate

# Validate account factory configuration
cd ../../environments/account-factory
terraform init
terraform validate
```

**Expected Output:** No errors, all modules validate successfully

### 1.2 Check Module Dependencies

```bash
# View module structure
cd environments/account-factory
terraform graph | grep -E "module\.|resource\."
```

**Expected Output:** Shows account-factory module → dev/staging/prod environment modules

---

## Step 2: Test with Sample Submission

### 2.1 Create Test GitHub Issue

Create a new GitHub issue with the following content:

**Title:** `Account Request: radiology-test-team`

**Body:**
```
# AWS Hospital Account Request

**Please fill out all fields below to request a new AWS account.**

---

## 1. Team Name

radiology-test-team

---

## 2. Team Lead / Owner

Dr. Test User

---

## 3. Team Email

radiology-test@hospital.com

---

## 4. Cost Center

CC-RADIOLOGY-TEST-001

---

## 5. Data Classification

- [x] **Confidential** - Patient data (PII)

---

## 6. Business Criticality

- [x] **High** - Patient-facing or critical operations

---

## 7. Primary Use Case

- [x] Medical Imaging / PACS

---

## 8. Estimated Monthly Budget

$2,500

---

## 9. Additional AWS Services (Optional)

- [x] RDS (Relational Database)
- [x] S3 (Object Storage)

---

## 10. Compliance Requirements

- [x] HIPAA (Health Insurance Portability and Accountability Act)
- [x] HITECH (Health Information Technology for Economic and Clinical Health)

---

## Checklist

- [x] All required fields are filled out
- [x] Team email is a hospital domain (@hospital.com)
- [x] Cost center follows format: CC-DEPARTMENT-XXX
- [x] Budget is between $100-$100,000
- [x] At least one compliance requirement is selected
- [x] I have read the Intake Form Documentation

---

## Additional Information (Optional)

Testing account factory for medical imaging workload.
```

### 2.2 Add Label

Add the `account-factory` label to the issue to trigger the workflow.

### 2.3 Monitor Workflow Execution

1. Go to **Actions** tab in GitHub
2. Find the workflow run for your issue
3. Monitor the `validate-intake-form` job
4. Check for validation comments on the issue

**Expected Outcomes:**
- ✅ Validation passes
- ✅ GitHub comment shows "Validation Passed"
- ✅ `provision-account` job starts automatically

---

## Step 3: Verify Account Creation

### 3.1 Check AWS Organizations

```bash
# List accounts in organization
aws organizations list-accounts \
  --region eu-north-1 \
  --query 'Accounts[?Name==`radiology-test-team`]'
```

**Expected Output:**
```json
[
  {
    "Id": "123456789012",
    "Arn": "arn:aws:organizations::...",
    "Email": "radiology-test@hospital.com",
    "Name": "radiology-test-team",
    "Status": "ACTIVE",
    "JoinedMethod": "CREATED",
    "JoinedTimestamp": "2026-02-26T..."
  }
]
```

### 3.2 Check VPC Creation in Dev Environment

```bash
# Assume role in new account
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/cross-account-access \
  --role-session-name test-session

# Set temporary credentials from output

# List VPCs in dev environment
aws ec2 describe-vpcs \
  --region eu-north-1 \
  --filters "Name=tag:Environment,Values=dev" \
  --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0]]'
```

**Expected Output:**
```
[
  [
    "vpc-0123456789abcdef0",
    "10.0.0.0/16",
    "radiology-test-team-dev-vpc"
  ]
]
```

### 3.3 Verify Landing Zone Infrastructure

```bash
# Check subnets
aws ec2 describe-subnets \
  --region eu-north-1 \
  --filters "Name=vpc-id,Values=vpc-0123456789abcdef0" \
  --query 'Subnets[*].[SubnetId,CidrBlock,Tags[?Key==`Type`].Value|[0]]'

# Check NAT Gateways
aws ec2 describe-nat-gateways \
  --region eu-north-1 \
  --filter "Name=vpc-id,Values=vpc-0123456789abcdef0" \
  --query 'NatGateways[*].[NatGatewayId,State]'

# Check Internet Gateway
aws ec2 describe-internet-gateways \
  --region eu-north-1 \
  --filters "Name=attachment.vpc-id,Values=vpc-0123456789abcdef0" \
  --query 'InternetGateways[*].[InternetGatewayId,Tags[?Key==`Name`].Value|[0]]'
```

**Expected Output:**
- 2 public subnets (10.0.0.0/18, 10.0.64.0/18)
- 2 private subnets (10.0.128.0/18, 10.0.192.0/18)
- 2 NAT Gateways (one per AZ)
- 1 Internet Gateway
- 4 Route Tables (1 public, 2 private)

### 3.4 Verify All Three Environments

Repeat the above checks for staging and prod environments:

```bash
# Staging environment
aws ec2 describe-vpcs \
  --region eu-north-1 \
  --filters "Name=tag:Environment,Values=staging" \
  --query 'Vpcs[*].VpcId'

# Prod environment
aws ec2 describe-vpcs \
  --region eu-north-1 \
  --filters "Name=tag:Environment,Values=prod" \
  --query 'Vpcs[*].VpcId'
```

**Expected Output:** 3 VPCs (dev, staging, prod) with CIDR blocks 10.0.0.0/16, 10.1.0.0/16, 10.2.0.0/16

---

## Step 4: Verify GitHub Actions Output

### 4.1 Check Issue Comments

The GitHub issue should have comments showing:

1. **Validation Result**
   ```
   ✅ Validation Passed
   Your account request has been validated successfully. Provisioning will begin shortly.
   Status: Processing
   ```

2. **Provisioning Result**
   ```
   ✅ Account Provisioning Complete
   
   Account Details:
   - Team: radiology-test-team
   - Primary Account: 123456789012
   - Dev Environment: vpc-0123456789abcdef0
   - Staging Environment: vpc-0123456789abcdef1
   - Prod Environment: vpc-0123456789abcdef2
   
   Next Steps:
   1. Check your email (radiology-test@hospital.com) for credentials
   2. Log in to AWS console
   3. Review landing zone infrastructure
   4. Start deploying applications
   ```

### 4.2 Check Issue Status

The issue should be:
- ✅ Closed
- ✅ Labeled with `account-factory` and `completed`

---

## Step 5: Test Validation Failures

### 5.1 Test Invalid Email

Create an issue with invalid email (not @hospital.com):

**Expected Result:**
- ❌ Validation fails
- ❌ GitHub comment shows error
- ❌ Issue remains open with `validation-failed` label

### 5.2 Test Invalid Cost Center

Create an issue with invalid cost center format:

**Expected Result:**
- ❌ Validation fails
- ❌ Error message shows required format

### 5.3 Test Budget Out of Range

Create an issue with budget < $100 or > $100,000:

**Expected Result:**
- ❌ Validation fails
- ❌ Error message shows valid range

---

## Step 6: Cleanup Test Account

After successful testing, remove the test account:

```bash
# Close the test account
aws organizations close-account \
  --account-id 123456789012 \
  --region eu-north-1
```

**Note:** Account closure takes 90 days to complete.

---

## Troubleshooting

### Issue: Workflow doesn't trigger

**Cause:** Label not added to issue  
**Solution:** Add `account-factory` label to issue

### Issue: Validation fails with "Team email must be valid hospital domain"

**Cause:** Email doesn't match @hospital.com pattern  
**Solution:** Use email format: `team-name@hospital.com`

### Issue: Terraform apply fails with "Access Denied"

**Cause:** GitHub Actions role doesn't have required permissions  
**Solution:** Add these permissions to the IAM role:
- `organizations:CreateAccount`
- `organizations:DescribeAccount`
- `ec2:*` (for VPC resources)
- `iam:*` (for IAM roles)
- `logs:*` (for VPC Flow Logs)

### Issue: Account creation succeeds but VPCs not created

**Cause:** Cross-account role assumption failed  
**Solution:** Verify the cross-account role exists and has correct trust relationship

### Issue: GitHub Actions times out

**Cause:** Account creation takes longer than expected  
**Solution:** Increase timeout in workflow (currently 30s wait after account creation)

---

## Success Criteria Checklist

- [ ] Terraform modules validate without errors
- [ ] GitHub issue submission triggers workflow
- [ ] Validation passes for valid intake form
- [ ] Validation fails for invalid intake form
- [ ] AWS account created in Organizations
- [ ] 3 environments (dev/staging/prod) created
- [ ] Each environment has VPC with landing zone infrastructure
- [ ] GitHub issue closed with completion comment
- [ ] All resources properly tagged
- [ ] Budget alerts configured

---

## Next Steps After Testing

1. **Create Team Onboarding Guide**
   - How to access new account
   - How to deploy applications
   - How to manage costs

2. **Create Runbooks**
   - Account access troubleshooting
   - Cost management
   - Security best practices

3. **Launch to First Team**
   - Communicate process to team
   - Monitor first account creation
   - Gather feedback

4. **Iterate and Improve**
   - Refine based on feedback
   - Add additional services as needed
   - Scale to all teams

---

## Support

For issues or questions:
- 📖 [Account Factory Implementation](ACCOUNT_FACTORY_IMPLEMENTATION.md)
- 📋 [Intake Form Documentation](ACCOUNT_FACTORY_INTAKE_FORM.md)
- 🏥 [Hospital Landing Zone](README.md)
- 💬 Contact: cloud-team@hospital.com

---

**Last Updated:** February 26, 2026
