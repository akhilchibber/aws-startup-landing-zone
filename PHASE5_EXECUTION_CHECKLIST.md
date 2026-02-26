# Phase 5 Execution Checklist

**Phase:** Phase 5 - Testing & Documentation  
**Date:** February 26-27, 2026  
**Executor:** [Your Name]  
**Status:** Ready to Execute

---

## Pre-Execution Checklist

### Prerequisites Verification
- [ ] AWS Organization is set up
- [ ] Organization Unit (OU) created for account provisioning
- [ ] S3 bucket exists: `hospital-terraform-state`
- [ ] DynamoDB table exists: `terraform-locks`
- [ ] GitHub repository is set up
- [ ] GitHub Actions is enabled
- [ ] All Terraform modules are validated
- [ ] Account factory configuration is ready

### Documentation Review
- [ ] Read `PHASE5_QUICK_START.md` (5 min)
- [ ] Read `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` (10 min)
- [ ] Understand the 9-step process
- [ ] Understand expected outputs
- [ ] Understand troubleshooting steps

---

## Step 1: Configure GitHub Secrets

**Duration:** 5 minutes  
**Reference:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` → Step 1

### 1.1 Create IAM Role
- [ ] Create trust policy document
- [ ] Create IAM role: `GitHubActionsRole`
- [ ] Attach `AdministratorAccess` policy
- [ ] Get role ARN

**Command:**
```bash
aws iam get-role --role-name GitHubActionsRole --query 'Role.Arn' --output text
```

**Expected Output:** `arn:aws:iam::123456789012:role/GitHubActionsRole`

### 1.2 Configure GitHub Secrets
- [ ] Go to GitHub Repository → Settings → Secrets and variables → Actions
- [ ] Add secret: `AWS_ROLE_TO_ASSUME`
  - Value: `arn:aws:iam::123456789012:role/GitHubActionsRole`
- [ ] Add secret: `TERRAFORM_STATE_BUCKET`
  - Value: `hospital-terraform-state`
- [ ] Add secret: `TERRAFORM_LOCK_TABLE`
  - Value: `terraform-locks`

### 1.3 Verify Secrets
- [ ] Test role assumption:
```bash
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/GitHubActionsRole \
  --role-session-name test-session
```

**Expected:** Temporary credentials returned

---

## Step 2: Validate Terraform Modules

**Duration:** 5 minutes  
**Reference:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` → Step 2

### 2.1 Validate Account Factory Module
- [ ] Navigate to `modules/account-factory`
- [ ] Run: `terraform init`
- [ ] Run: `terraform validate`
- [ ] Verify: No errors

### 2.2 Validate Environment Module
- [ ] Navigate to `modules/environment`
- [ ] Run: `terraform init`
- [ ] Run: `terraform validate`
- [ ] Verify: No errors

### 2.3 Validate Account Factory Configuration
- [ ] Navigate to `environments/account-factory`
- [ ] Run: `terraform init` with backend config
- [ ] Run: `terraform validate`
- [ ] Verify: No errors

**Expected Output:** `Success! The configuration is valid.`

---

## Step 3: Create Test GitHub Issue

**Duration:** 5 minutes  
**Reference:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` → Step 3

### 3.1 Prepare Test Data
- [ ] Team Name: `radiology-test-team`
- [ ] Team Lead: `Dr. Test User`
- [ ] Team Email: `radiology-test@hospital.com`
- [ ] Cost Center: `CC-RADIOLOGY-TEST-001`
- [ ] Data Classification: `Confidential`
- [ ] Business Criticality: `High`
- [ ] Primary Use Case: `Medical Imaging / PACS`
- [ ] Estimated Monthly Budget: `$2,500`
- [ ] Additional Services: `RDS, S3`
- [ ] Compliance Requirements: `HIPAA, HITECH`

### 3.2 Create GitHub Issue
- [ ] Go to GitHub Repository → Issues → New Issue
- [ ] Select "Account Request" template
- [ ] Fill in all fields with test data
- [ ] Click "Submit new issue"

### 3.3 Add Label
- [ ] Click "Labels" on the issue
- [ ] Select `account-factory` label
- [ ] Verify label is added

**Expected:** Issue created with `account-factory` label

---

## Step 4: Monitor Workflow Execution

**Duration:** 10-15 minutes  
**Reference:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` → Step 4

### 4.1 Watch Validation Job
- [ ] Go to GitHub Repository → Actions
- [ ] Find the workflow run for your issue
- [ ] Click on the run
- [ ] Monitor `validate-intake-form` job
- [ ] Wait for completion (1-2 min)

**Expected:** Job completes successfully

### 4.2 Check Validation Comment
- [ ] Go back to the GitHub issue
- [ ] Look for validation comment
- [ ] Verify comment shows: ✅ Validation Passed

**Expected Comment:**
```
✅ Validation Passed

Your account request has been validated successfully. 
Provisioning will begin shortly.

Status: Processing
```

### 4.3 Watch Provisioning Job
- [ ] Go back to Actions tab
- [ ] Monitor `provision-account` job
- [ ] Wait for completion (5-10 min)

**Expected Timeline:**
- 0-1 min: Workflow starts
- 1-2 min: Validation completes
- 2-3 min: GitHub comment posted
- 3-13 min: Provisioning runs
- 13-15 min: Issue closed

### 4.4 Check Provisioning Comment
- [ ] Go back to the GitHub issue
- [ ] Look for provisioning comment
- [ ] Verify comment shows: ✅ Account Provisioning Complete
- [ ] Note the account IDs

**Expected Comment:**
```
✅ Account Provisioning Complete

Account Details:
- Team: radiology-test-team
- Primary Account: 123456789012
- Dev Environment: vpc-0123456789abc0
- Staging Environment: vpc-0123456789def0
- Prod Environment: vpc-0123456789ghi0
```

---

## Step 5: Verify AWS Account Creation

**Duration:** 5 minutes  
**Reference:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` → Step 5

### 5.1 Check AWS Organizations
- [ ] Run command:
```bash
aws organizations list-accounts \
  --region eu-north-1 \
  --query 'Accounts[?Name==`radiology-test-team`]'
```

- [ ] Verify account exists
- [ ] Verify status is ACTIVE
- [ ] Note the Account ID

**Expected Output:**
```json
[
  {
    "Id": "123456789012",
    "Status": "ACTIVE",
    "Name": "radiology-test-team",
    "Email": "radiology-test@hospital.com"
  }
]
```

### 5.2 Get Account ID
- [ ] Run command:
```bash
ACCOUNT_ID=$(aws organizations list-accounts \
  --region eu-north-1 \
  --query 'Accounts[?Name==`radiology-test-team`].Id' \
  --output text)
echo "Account ID: $ACCOUNT_ID"
```

- [ ] Save the Account ID for next steps

---

## Step 6: Verify VPC Infrastructure

**Duration:** 10 minutes  
**Reference:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` → Step 6

### 6.1 Assume Cross-Account Role
- [ ] Run command:
```bash
CREDENTIALS=$(aws sts assume-role \
  --role-arn arn:aws:iam::$ACCOUNT_ID:role/cross-account-access \
  --role-session-name test-session \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text)

export AWS_ACCESS_KEY_ID=$(echo $CREDENTIALS | awk '{print $1}')
export AWS_SECRET_ACCESS_KEY=$(echo $CREDENTIALS | awk '{print $2}')
export AWS_SESSION_TOKEN=$(echo $CREDENTIALS | awk '{print $3}')
```

- [ ] Verify credentials are set

### 6.2 Verify Dev Environment VPC
- [ ] Run command:
```bash
aws ec2 describe-vpcs \
  --region eu-north-1 \
  --filters "Name=tag:Environment,Values=dev" \
  --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0]]'
```

- [ ] Verify VPC exists
- [ ] Verify CIDR block is 10.0.0.0/16
- [ ] Note the VPC ID

**Expected Output:**
```
[
  [
    "vpc-0123456789abc0",
    "10.0.0.0/16",
    "radiology-test-team-dev"
  ]
]
```

### 6.3 Verify Subnets
- [ ] Run command:
```bash
aws ec2 describe-subnets \
  --region eu-north-1 \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[*].[SubnetId,CidrBlock,Tags[?Key==`Type`].Value|[0]]'
```

- [ ] Verify 2 public subnets (10.0.0.0/18, 10.0.64.0/18)
- [ ] Verify 2 private subnets (10.0.128.0/18, 10.0.192.0/18)

### 6.4 Verify NAT Gateways
- [ ] Run command:
```bash
aws ec2 describe-nat-gateways \
  --region eu-north-1 \
  --filter "Name=vpc-id,Values=$VPC_ID" \
  --query 'NatGateways[*].[NatGatewayId,State]'
```

- [ ] Verify 2 NAT Gateways
- [ ] Verify both are in AVAILABLE state

### 6.5 Verify Internet Gateway
- [ ] Run command:
```bash
aws ec2 describe-internet-gateways \
  --region eu-north-1 \
  --filters "Name=attachment.vpc-id,Values=$VPC_ID" \
  --query 'InternetGateways[*].InternetGatewayId'
```

- [ ] Verify 1 Internet Gateway exists

### 6.6 Verify Route Tables
- [ ] Run command:
```bash
aws ec2 describe-route-tables \
  --region eu-north-1 \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'RouteTables[*].[RouteTableId,Tags[?Key==`Type`].Value|[0]]'
```

- [ ] Verify 1 public route table
- [ ] Verify 2 private route tables

### 6.7 Verify Staging Environment
- [ ] Repeat steps 6.2-6.6 for staging environment
- [ ] Verify VPC CIDR: 10.1.0.0/16

### 6.8 Verify Production Environment
- [ ] Repeat steps 6.2-6.6 for production environment
- [ ] Verify VPC CIDR: 10.2.0.0/16

---

## Step 7: Verify GitHub Issue Status

**Duration:** 2 minutes  
**Reference:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` → Step 7

### 7.1 Check Issue Comments
- [ ] Go to GitHub issue
- [ ] Verify 2 comments exist:
  - [ ] Validation Passed comment
  - [ ] Account Provisioning Complete comment

### 7.2 Check Issue Status
- [ ] Verify issue is CLOSED
- [ ] Verify labels include `account-factory`
- [ ] Verify labels include `completed`

---

## Step 8: Test Validation Failures

**Duration:** 10 minutes  
**Reference:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` → Step 8

### 8.1 Test Invalid Email
- [ ] Create new GitHub issue
- [ ] Use test data but set:
  - Team Email: `test@gmail.com` (not @hospital.com)
- [ ] Add `account-factory` label
- [ ] Wait for validation (1-2 min)
- [ ] Verify validation FAILS
- [ ] Verify error message shows email error
- [ ] Verify issue remains OPEN with `validation-failed` label

**Expected Error:**
```
❌ Validation Failed

Please correct the following errors:
- Team Email: Must be valid hospital domain (@hospital.com)
```

### 8.2 Test Invalid Cost Center
- [ ] Create new GitHub issue
- [ ] Use test data but set:
  - Cost Center: `INVALID` (should be CC-DEPT-XXX)
- [ ] Add `account-factory` label
- [ ] Wait for validation (1-2 min)
- [ ] Verify validation FAILS
- [ ] Verify error message shows cost center error

**Expected Error:**
```
❌ Validation Failed

Please correct the following errors:
- Cost Center: Must follow format CC-DEPARTMENT-XXX
```

### 8.3 Test Budget Out of Range
- [ ] Create new GitHub issue
- [ ] Use test data but set:
  - Estimated Monthly Budget: `$50` (minimum is $100)
- [ ] Add `account-factory` label
- [ ] Wait for validation (1-2 min)
- [ ] Verify validation FAILS
- [ ] Verify error message shows budget error

**Expected Error:**
```
❌ Validation Failed

Please correct the following errors:
- Monthly Budget: Must be between $100-$100,000
```

---

## Step 9: Document Test Results

**Duration:** 5 minutes  
**Reference:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` → Step 9

### 9.1 Create Test Results Document
- [ ] Create file: `ACCOUNT_FACTORY_TEST_RESULTS.md`
- [ ] Document all test results
- [ ] Record any issues found
- [ ] Record recommendations

### 9.2 Update Implementation Plan
- [ ] Open `ACCOUNT_FACTORY_IMPLEMENTATION.md`
- [ ] Update Phase 5 status to 100% COMPLETE
- [ ] Update overall progress to 90%
- [ ] Add completion date
- [ ] Update next steps to Phase 6

### 9.3 Update Status Summary
- [ ] Open `STATUS_SUMMARY.md`
- [ ] Update Phase 5 status to 100% COMPLETE
- [ ] Update overall progress to 90%
- [ ] Update next steps

---

## Success Criteria Verification

### Account Creation
- [ ] AWS account created in Organizations
- [ ] Account status is ACTIVE
- [ ] Account name is `radiology-test-team`
- [ ] Account email is `radiology-test@hospital.com`

### Infrastructure Deployment
- [ ] 3 VPCs created (dev, staging, prod)
- [ ] Dev VPC CIDR: 10.0.0.0/16
- [ ] Staging VPC CIDR: 10.1.0.0/16
- [ ] Prod VPC CIDR: 10.2.0.0/16
- [ ] Each VPC has 2 public subnets
- [ ] Each VPC has 2 private subnets
- [ ] Each VPC has 2 NAT Gateways
- [ ] Each VPC has 1 Internet Gateway
- [ ] Each VPC has 4 route tables

### GitHub Workflow
- [ ] Workflow triggered automatically
- [ ] Validation job completed
- [ ] Provisioning job completed
- [ ] GitHub comments posted
- [ ] Issue closed with completion comment

### Validation Testing
- [ ] Invalid email validation failed
- [ ] Invalid cost center validation failed
- [ ] Budget out of range validation failed
- [ ] Error messages are clear

### Documentation
- [ ] Test results documented
- [ ] Implementation plan updated
- [ ] Status summary updated
- [ ] All issues recorded

---

## Final Checklist

- [ ] All 9 steps completed
- [ ] All success criteria verified
- [ ] Test results documented
- [ ] Implementation plan updated
- [ ] Status summary updated
- [ ] No critical issues found
- [ ] Ready for Phase 6 launch

---

## Issues Found

**Issue 1:** [Describe any issues found]
- [ ] Severity: High / Medium / Low
- [ ] Impact: [Describe impact]
- [ ] Resolution: [Describe resolution]
- [ ] Status: Open / Resolved

**Issue 2:** [Describe any issues found]
- [ ] Severity: High / Medium / Low
- [ ] Impact: [Describe impact]
- [ ] Resolution: [Describe resolution]
- [ ] Status: Open / Resolved

---

## Recommendations

**Recommendation 1:** [Describe any recommendations]
- [ ] Priority: High / Medium / Low
- [ ] Effort: High / Medium / Low
- [ ] Status: Pending / In Progress / Complete

**Recommendation 2:** [Describe any recommendations]
- [ ] Priority: High / Medium / Low
- [ ] Effort: High / Medium / Low
- [ ] Status: Pending / In Progress / Complete

---

## Sign-Off

**Executor Name:** ___________________________

**Executor Email:** ___________________________

**Execution Date:** ___________________________

**Execution Time:** ___________________________

**Overall Result:** ✅ PASS / ❌ FAIL

**Comments:** ___________________________

---

## Next Steps

After Phase 5 completion:

1. **Phase 6: Launch & Monitoring**
   - Soft launch to cloud team
   - Limited launch to pilot teams
   - Full launch to all teams

2. **Monitoring Setup**
   - Configure CloudWatch alarms
   - Set up cost anomaly detection
   - Create dashboards

3. **Team Support**
   - Provide onboarding
   - Answer questions
   - Gather feedback

---

**Phase 5 Execution Checklist**  
**Version:** 1.0  
**Status:** Ready to Execute  
**Target Completion:** February 27, 2026

