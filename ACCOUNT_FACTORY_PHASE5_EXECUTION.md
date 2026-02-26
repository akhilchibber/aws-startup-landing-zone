# AWS Hospital Account Factory - Phase 5 Execution Guide

**Phase:** Phase 5 - Testing & Documentation  
**Status:** In Progress  
**Start Date:** February 26, 2026  
**Target Completion:** February 27, 2026  
**Overall Progress:** 80% → 90% (after Phase 5)

---

## Phase 5 Overview

Phase 5 focuses on end-to-end testing of the account factory system before launching to hospital teams. This phase validates that:

1. GitHub workflow triggers correctly
2. Intake form validation works
3. AWS account creation succeeds
4. 3 environments (dev/staging/prod) are created
5. Landing zone infrastructure deploys correctly
6. Error handling works for invalid submissions
7. All documentation is accurate

---

## Prerequisites Checklist

Before starting Phase 5, verify:

- [ ] AWS Organization is set up
- [ ] Organization Unit (OU) created for account provisioning
- [ ] S3 bucket exists for Terraform state (`hospital-terraform-state`)
- [ ] DynamoDB table exists for state locking (`terraform-locks`)
- [ ] IAM role created for GitHub Actions (`GitHubActionsRole`)
- [ ] GitHub repository is set up
- [ ] GitHub Actions is enabled
- [ ] All Terraform modules are validated
- [ ] Account factory configuration is ready

---

## Step 1: Configure GitHub Secrets

### 1.1 Create IAM Role for GitHub Actions

First, create an IAM role that GitHub Actions will assume:

```bash
# Create trust policy document
cat > /tmp/trust-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::MANAGEMENT_ACCOUNT_ID:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "github-actions-external-id"
        }
      }
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name GitHubActionsRole \
  --assume-role-policy-document file:///tmp/trust-policy.json \
  --region eu-north-1

# Attach policies
aws iam attach-role-policy \
  --role-name GitHubActionsRole \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess \
  --region eu-north-1
```

**Note:** Replace `MANAGEMENT_ACCOUNT_ID` with your AWS management account ID.

### 1.2 Get Role ARN

```bash
aws iam get-role \
  --role-name GitHubActionsRole \
  --query 'Role.Arn' \
  --output text
```

**Output Example:** `arn:aws:iam::123456789012:role/GitHubActionsRole`

### 1.3 Configure GitHub Secrets

In your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following secrets:

#### Secret 1: AWS_ROLE_TO_ASSUME
- **Name:** `AWS_ROLE_TO_ASSUME`
- **Value:** `arn:aws:iam::123456789012:role/GitHubActionsRole`

#### Secret 2: TERRAFORM_STATE_BUCKET
- **Name:** `TERRAFORM_STATE_BUCKET`
- **Value:** `hospital-terraform-state`

#### Secret 3: TERRAFORM_LOCK_TABLE
- **Name:** `TERRAFORM_LOCK_TABLE`
- **Value:** `terraform-locks`

### 1.4 Verify Secrets Configuration

```bash
# Test role assumption
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/GitHubActionsRole \
  --role-session-name test-session \
  --external-id github-actions-external-id
```

**Expected Output:** Temporary credentials returned successfully

---

## Step 2: Validate Terraform Modules

### 2.1 Validate Account Factory Module

```bash
cd modules/account-factory
terraform init
terraform validate
```

**Expected Output:**
```
Success! The configuration is valid.
```

### 2.2 Validate Environment Module

```bash
cd ../environment
terraform init
terraform validate
```

**Expected Output:**
```
Success! The configuration is valid.
```

### 2.3 Validate Account Factory Configuration

```bash
cd ../../environments/account-factory
terraform init \
  -backend-config="bucket=hospital-terraform-state" \
  -backend-config="key=account-factory/state" \
  -backend-config="region=eu-north-1" \
  -backend-config="dynamodb_table=terraform-locks"

terraform validate
```

**Expected Output:**
```
Success! The configuration is valid.
```

---

## Step 3: Create Test GitHub Issue

### 3.1 Prepare Test Data

Use this test data for the first account creation:

```
Team Name: radiology-test-team
Team Lead: Dr. Test User
Team Email: radiology-test@hospital.com
Cost Center: CC-RADIOLOGY-TEST-001
Data Classification: Confidential
Business Criticality: High
Primary Use Case: Medical Imaging / PACS
Estimated Monthly Budget: $2,500
Additional Services: RDS, S3
Compliance Requirements: HIPAA, HITECH
```

### 3.2 Create GitHub Issue

1. Go to your GitHub repository
2. Click **Issues** → **New issue**
3. Click **Account Request** template
4. Fill in the form with test data above
5. Click **Submit new issue**

### 3.3 Add Label

1. On the issue page, click **Labels**
2. Select `account-factory` label
3. This triggers the GitHub Actions workflow

---

## Step 4: Monitor Workflow Execution

### 4.1 Watch Workflow Run

1. Go to **Actions** tab
2. Find the workflow run for your issue
3. Click on the run to see details
4. Monitor the `validate-intake-form` job

### 4.2 Check Validation Results

**Expected Timeline:**
- 0-1 min: Workflow starts
- 1-2 min: Validation completes
- 2-3 min: GitHub comment posted

**Expected Comment:**
```
✅ Validation Passed

Your account request has been validated successfully. 
Provisioning will begin shortly.

Status: Processing
```

### 4.3 Monitor Provisioning Job

If validation passes:
1. `provision-account` job starts automatically
2. Terraform initializes (1-2 min)
3. Terraform plans (2-3 min)
4. Terraform applies (5-10 min)

**Expected Timeline:** 10-15 minutes total

---

## Step 5: Verify AWS Account Creation

### 5.1 Check AWS Organizations

```bash
# List all accounts
aws organizations list-accounts \
  --region eu-north-1 \
  --query 'Accounts[?Name==`radiology-test-team`]' \
  --output json
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

**Verification Points:**
- [ ] Account ID is numeric (12 digits)
- [ ] Account status is ACTIVE
- [ ] Account name matches team name
- [ ] Account email matches team email

### 5.2 Get Account ID

```bash
ACCOUNT_ID=$(aws organizations list-accounts \
  --region eu-north-1 \
  --query 'Accounts[?Name==`radiology-test-team`].Id' \
  --output text)

echo "Account ID: $ACCOUNT_ID"
```

---

## Step 6: Verify VPC Infrastructure

### 6.1 Assume Cross-Account Role

```bash
# Assume role in new account
CREDENTIALS=$(aws sts assume-role \
  --role-arn arn:aws:iam::$ACCOUNT_ID:role/cross-account-access \
  --role-session-name test-session \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text)

# Extract credentials
export AWS_ACCESS_KEY_ID=$(echo $CREDENTIALS | awk '{print $1}')
export AWS_SECRET_ACCESS_KEY=$(echo $CREDENTIALS | awk '{print $2}')
export AWS_SESSION_TOKEN=$(echo $CREDENTIALS | awk '{print $3}')
```

### 6.2 Verify Dev Environment VPC

```bash
# List VPCs in dev environment
aws ec2 describe-vpcs \
  --region eu-north-1 \
  --filters "Name=tag:Environment,Values=dev" \
  --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0]]' \
  --output table
```

**Expected Output:**
```
|  VpcId              |  CidrBlock    |  Name                      |
|---------------------|---------------|----------------------------|
|  vpc-0123456789abc0  |  10.0.0.0/16  |  radiology-test-team-dev   |
```

**Verification Points:**
- [ ] VPC ID starts with `vpc-`
- [ ] CIDR block is `10.0.0.0/16`
- [ ] Name includes team name and environment

### 6.3 Verify Subnets

```bash
# List subnets
aws ec2 describe-subnets \
  --region eu-north-1 \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[*].[SubnetId,CidrBlock,Tags[?Key==`Type`].Value|[0],AvailabilityZone]' \
  --output table
```

**Expected Output:**
```
|  SubnetId           |  CidrBlock      |  Type     |  AZ           |
|---------------------|-----------------|-----------|---------------|
|  subnet-0123456789a |  10.0.0.0/18    |  public   |  eu-north-1a  |
|  subnet-0123456789b |  10.0.64.0/18   |  public   |  eu-north-1b  |
|  subnet-0123456789c |  10.0.128.0/18  |  private  |  eu-north-1a  |
|  subnet-0123456789d |  10.0.192.0/18  |  private  |  eu-north-1b  |
```

**Verification Points:**
- [ ] 2 public subnets (10.0.0.0/18, 10.0.64.0/18)
- [ ] 2 private subnets (10.0.128.0/18, 10.0.192.0/18)
- [ ] Subnets span 2 availability zones

### 6.4 Verify NAT Gateways

```bash
# List NAT Gateways
aws ec2 describe-nat-gateways \
  --region eu-north-1 \
  --filter "Name=vpc-id,Values=$VPC_ID" \
  --query 'NatGateways[*].[NatGatewayId,State,SubnetId]' \
  --output table
```

**Expected Output:**
```
|  NatGatewayId       |  State    |  SubnetId           |
|---------------------|-----------|---------------------|
|  natgw-0123456789a  |  available|  subnet-0123456789a |
|  natgw-0123456789b  |  available|  subnet-0123456789b |
```

**Verification Points:**
- [ ] 2 NAT Gateways created
- [ ] Both in AVAILABLE state
- [ ] One per public subnet

### 6.5 Verify Internet Gateway

```bash
# List Internet Gateways
aws ec2 describe-internet-gateways \
  --region eu-north-1 \
  --filters "Name=attachment.vpc-id,Values=$VPC_ID" \
  --query 'InternetGateways[*].[InternetGatewayId,Tags[?Key==`Name`].Value|[0]]' \
  --output table
```

**Expected Output:**
```
|  InternetGatewayId  |  Name                      |
|---------------------|----------------------------|
|  igw-0123456789abc  |  radiology-test-team-igw   |
```

**Verification Points:**
- [ ] 1 Internet Gateway created
- [ ] Attached to VPC

### 6.6 Verify Route Tables

```bash
# List Route Tables
aws ec2 describe-route-tables \
  --region eu-north-1 \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'RouteTables[*].[RouteTableId,Tags[?Key==`Name`].Value|[0],Tags[?Key==`Type`].Value|[0]]' \
  --output table
```

**Expected Output:**
```
|  RouteTableId       |  Name                      |  Type     |
|---------------------|----------------------------|-----------|
|  rtb-0123456789abc  |  radiology-test-team-pub   |  public   |
|  rtb-0123456789def  |  radiology-test-team-priv1 |  private  |
|  rtb-0123456789ghi  |  radiology-test-team-priv2 |  private  |
```

**Verification Points:**
- [ ] 1 public route table
- [ ] 2 private route tables (one per AZ)

### 6.7 Verify Staging Environment

Repeat steps 6.2-6.6 for staging environment:

```bash
# List VPCs in staging environment
aws ec2 describe-vpcs \
  --region eu-north-1 \
  --filters "Name=tag:Environment,Values=staging" \
  --query 'Vpcs[*].[VpcId,CidrBlock]' \
  --output table
```

**Expected Output:**
```
|  VpcId              |  CidrBlock    |
|---------------------|---------------|
|  vpc-0123456789def0 |  10.1.0.0/16  |
```

### 6.8 Verify Production Environment

Repeat steps 6.2-6.6 for production environment:

```bash
# List VPCs in production environment
aws ec2 describe-vpcs \
  --region eu-north-1 \
  --filters "Name=tag:Environment,Values=prod" \
  --query 'Vpcs[*].[VpcId,CidrBlock]' \
  --output table
```

**Expected Output:**
```
|  VpcId              |  CidrBlock    |
|---------------------|---------------|
|  vpc-0123456789ghi0 |  10.2.0.0/16  |
```

---

## Step 7: Verify GitHub Issue Status

### 7.1 Check Issue Comments

The GitHub issue should have multiple comments:

**Comment 1 - Validation Result:**
```
✅ Validation Passed

Your account request has been validated successfully. 
Provisioning will begin shortly.

Status: Processing
```

**Comment 2 - Provisioning Result:**
```
✅ Account Provisioning Complete

Account Details:
- Team: radiology-test-team
- Primary Account: 123456789012
- Dev Environment: vpc-0123456789abc0
- Staging Environment: vpc-0123456789def0
- Prod Environment: vpc-0123456789ghi0

Next Steps:
1. Check your email (radiology-test@hospital.com) for credentials
2. Log in to AWS console
3. Review landing zone infrastructure
4. Start deploying applications

Support: Contact cloud-team@hospital.com
```

### 7.2 Check Issue Status

The issue should be:
- [ ] Closed
- [ ] Labeled with `account-factory`
- [ ] Labeled with `completed`

---

## Step 8: Test Validation Failures

### 8.1 Test Invalid Email

**Create new issue with:**
```
Team Name: test-invalid-email
Team Lead: Test User
Team Email: test@gmail.com  ← Invalid (not @hospital.com)
Cost Center: CC-TEST-001
Data Classification: Confidential
Business Criticality: High
Primary Use Case: EHR System
Estimated Monthly Budget: $5,000
Additional Services: RDS
Compliance Requirements: HIPAA
```

**Expected Result:**
- ❌ Validation fails
- ❌ GitHub comment shows error:
  ```
  ❌ Validation Failed
  
  Please correct the following errors:
  - Team Email: Must be valid hospital domain (@hospital.com)
  ```
- ❌ Issue remains open with `validation-failed` label

### 8.2 Test Invalid Cost Center

**Create new issue with:**
```
Cost Center: INVALID-FORMAT  ← Invalid (should be CC-DEPT-XXX)
```

**Expected Result:**
- ❌ Validation fails
- ❌ Error message shows required format

### 8.3 Test Budget Out of Range

**Create new issue with:**
```
Estimated Monthly Budget: $50  ← Invalid (minimum is $100)
```

**Expected Result:**
- ❌ Validation fails
- ❌ Error message shows valid range ($100-$100,000)

### 8.4 Test Missing Required Field

**Create new issue with:**
```
Team Name: (empty)  ← Missing required field
```

**Expected Result:**
- ❌ Validation fails
- ❌ Error message indicates required field

---

## Step 9: Document Test Results

### 9.1 Create Test Results Document

Create a file `ACCOUNT_FACTORY_TEST_RESULTS.md` with:

```markdown
# Account Factory - Test Results

**Test Date:** February 26, 2026  
**Tester:** [Your Name]  
**Status:** PASS / FAIL

## Test 1: Valid Account Creation
- [ ] GitHub issue created
- [ ] Workflow triggered
- [ ] Validation passed
- [ ] AWS account created
- [ ] 3 environments created
- [ ] Landing zone deployed
- [ ] Issue closed with completion comment

**Result:** PASS / FAIL

## Test 2: Invalid Email Validation
- [ ] GitHub issue created with invalid email
- [ ] Validation failed as expected
- [ ] Error message displayed
- [ ] Issue remains open

**Result:** PASS / FAIL

## Test 3: Invalid Cost Center Validation
- [ ] GitHub issue created with invalid cost center
- [ ] Validation failed as expected
- [ ] Error message displayed

**Result:** PASS / FAIL

## Test 4: Budget Out of Range Validation
- [ ] GitHub issue created with budget < $100
- [ ] Validation failed as expected
- [ ] Error message displayed

**Result:** PASS / FAIL

## Issues Found

[Document any issues encountered]

## Recommendations

[Document any improvements needed]
```

### 9.2 Update Implementation Plan

Update `ACCOUNT_FACTORY_IMPLEMENTATION.md`:

```markdown
### Phase 5: Testing & Documentation ✅ COMPLETE
**Duration:** 1 day  
**Status:** 100% Complete  
**Completion Date:** February 26, 2026

**Deliverables:**
- ✅ End-to-end testing completed
- ✅ Account creation verified
- ✅ Infrastructure deployment verified
- ✅ Validation failure testing completed
- ✅ Test results documented
- ✅ All success criteria met
```

---

## Success Criteria Checklist

- [ ] GitHub secrets configured
- [ ] Terraform modules validate
- [ ] Test GitHub issue created
- [ ] Workflow triggers automatically
- [ ] Validation passes for valid form
- [ ] AWS account created in Organizations
- [ ] Dev environment VPC created (10.0.0.0/16)
- [ ] Staging environment VPC created (10.1.0.0/16)
- [ ] Prod environment VPC created (10.2.0.0/16)
- [ ] Each VPC has 2 public subnets
- [ ] Each VPC has 2 private subnets
- [ ] Each VPC has 2 NAT Gateways
- [ ] Each VPC has 1 Internet Gateway
- [ ] Each VPC has 4 route tables
- [ ] GitHub issue closed with completion comment
- [ ] Validation fails for invalid email
- [ ] Validation fails for invalid cost center
- [ ] Validation fails for budget out of range
- [ ] Test results documented
- [ ] Implementation plan updated

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
**Solution:** Verify role has AdministratorAccess policy attached

### Issue: Account creation succeeds but VPCs not created

**Cause:** Cross-account role assumption failed  
**Solution:** Verify cross-account role exists in new account

### Issue: GitHub Actions times out

**Cause:** Account creation takes longer than expected  
**Solution:** Increase timeout in workflow

---

## Next Steps After Phase 5

1. **Phase 6: Launch & Monitoring**
   - Soft launch to cloud team
   - Limited launch to 1-2 pilot teams
   - Monitor account creation
   - Gather feedback
   - Scale to all hospital teams

2. **Documentation Updates**
   - Update team onboarding guide
   - Create runbooks
   - Create troubleshooting guide

3. **Monitoring Setup**
   - Configure CloudWatch alarms
   - Set up cost anomaly detection
   - Create dashboards

---

**Phase 5 Status:** In Progress  
**Target Completion:** February 27, 2026  
**Next Phase:** Phase 6 - Launch & Monitoring (Feb 28, 2026)

