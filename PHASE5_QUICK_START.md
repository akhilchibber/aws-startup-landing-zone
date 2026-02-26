# Phase 5 - Quick Start Guide

**Phase:** Phase 5 - Testing & Documentation  
**Status:** Ready to Execute  
**Duration:** 1 day  
**Target Completion:** February 27, 2026

---

## 5-Minute Overview

Phase 5 tests the entire account factory system end-to-end:

1. **Configure GitHub Secrets** (5 min)
   - Add 3 secrets to GitHub repository
   - Required for GitHub Actions to access AWS

2. **Validate Terraform** (5 min)
   - Ensure all modules are ready
   - No syntax errors

3. **Test Account Creation** (10 min)
   - Create test GitHub issue
   - Watch workflow run
   - Verify AWS account created

4. **Verify Infrastructure** (10 min)
   - Check VPCs created
   - Check subnets, NAT gateways, IGW
   - Verify all 3 environments

5. **Test Validation Failures** (10 min)
   - Test invalid email
   - Test invalid cost center
   - Test budget out of range

6. **Document Results** (5 min)
   - Record what worked
   - Record any issues
   - Update documentation

**Total Time:** ~45 minutes

---

## Step-by-Step Execution

### Step 1: Configure GitHub Secrets (5 min)

**Location:** GitHub Repository → Settings → Secrets and variables → Actions

**Add 3 Secrets:**

1. `AWS_ROLE_TO_ASSUME`
   - Value: `arn:aws:iam::123456789012:role/GitHubActionsRole`
   - Replace with your actual account ID and role name

2. `TERRAFORM_STATE_BUCKET`
   - Value: `hospital-terraform-state`

3. `TERRAFORM_LOCK_TABLE`
   - Value: `terraform-locks`

**Verify:** Try to assume role:
```bash
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/GitHubActionsRole \
  --role-session-name test-session
```

---

### Step 2: Validate Terraform (5 min)

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
terraform init \
  -backend-config="bucket=hospital-terraform-state" \
  -backend-config="key=account-factory/state" \
  -backend-config="region=eu-north-1" \
  -backend-config="dynamodb_table=terraform-locks"
terraform validate
```

**Expected:** All validations pass with no errors

---

### Step 3: Create Test GitHub Issue (5 min)

**Go to:** GitHub Repository → Issues → New Issue → Account Request

**Fill in:**
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

**Add Label:** `account-factory` (this triggers the workflow)

---

### Step 4: Monitor Workflow (10 min)

**Go to:** GitHub Repository → Actions

**Watch:**
1. `validate-intake-form` job (1-2 min)
   - Should show ✅ Validation Passed comment
2. `provision-account` job (5-10 min)
   - Should show ✅ Account Provisioning Complete comment

**Expected Timeline:**
- 0-1 min: Workflow starts
- 1-2 min: Validation completes
- 2-3 min: GitHub comment posted
- 3-13 min: Provisioning runs
- 13-15 min: Issue closed with completion comment

---

### Step 5: Verify AWS Account (10 min)

```bash
# Check account created
aws organizations list-accounts \
  --region eu-north-1 \
  --query 'Accounts[?Name==`radiology-test-team`]'

# Get account ID
ACCOUNT_ID=$(aws organizations list-accounts \
  --region eu-north-1 \
  --query 'Accounts[?Name==`radiology-test-team`].Id' \
  --output text)

# Assume role in new account
aws sts assume-role \
  --role-arn arn:aws:iam::$ACCOUNT_ID:role/cross-account-access \
  --role-session-name test-session

# Check VPCs created
aws ec2 describe-vpcs \
  --region eu-north-1 \
  --filters "Name=tag:Team,Values=radiology-test-team" \
  --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Environment`].Value|[0]]'
```

**Expected:**
- 1 AWS account created
- 3 VPCs created (dev, staging, prod)
- CIDR blocks: 10.0.0.0/16, 10.1.0.0/16, 10.2.0.0/16

---

### Step 6: Verify Infrastructure (10 min)

```bash
# Check subnets
aws ec2 describe-subnets \
  --region eu-north-1 \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[*].[SubnetId,CidrBlock,Tags[?Key==`Type`].Value|[0]]'

# Check NAT Gateways
aws ec2 describe-nat-gateways \
  --region eu-north-1 \
  --filter "Name=vpc-id,Values=$VPC_ID" \
  --query 'NatGateways[*].[NatGatewayId,State]'

# Check Internet Gateway
aws ec2 describe-internet-gateways \
  --region eu-north-1 \
  --filters "Name=attachment.vpc-id,Values=$VPC_ID" \
  --query 'InternetGateways[*].InternetGatewayId'
```

**Expected per VPC:**
- 2 public subnets
- 2 private subnets
- 2 NAT Gateways
- 1 Internet Gateway
- 4 route tables

---

### Step 7: Test Validation Failures (10 min)

**Test 1: Invalid Email**
```
Team Email: test@gmail.com  ← Not @hospital.com
```
Expected: ❌ Validation fails

**Test 2: Invalid Cost Center**
```
Cost Center: INVALID  ← Should be CC-DEPT-XXX
```
Expected: ❌ Validation fails

**Test 3: Budget Out of Range**
```
Estimated Monthly Budget: $50  ← Minimum is $100
```
Expected: ❌ Validation fails

---

### Step 8: Document Results

Create file: `ACCOUNT_FACTORY_TEST_RESULTS.md`

```markdown
# Test Results - February 26, 2026

## Test 1: Valid Account Creation
- [x] GitHub issue created
- [x] Workflow triggered
- [x] Validation passed
- [x] AWS account created
- [x] 3 environments created
- [x] Infrastructure deployed
- [x] Issue closed

**Result:** ✅ PASS

## Test 2: Invalid Email Validation
- [x] Validation failed as expected
- [x] Error message displayed

**Result:** ✅ PASS

## Test 3: Invalid Cost Center Validation
- [x] Validation failed as expected
- [x] Error message displayed

**Result:** ✅ PASS

## Test 4: Budget Out of Range Validation
- [x] Validation failed as expected
- [x] Error message displayed

**Result:** ✅ PASS

## Overall Result: ✅ ALL TESTS PASSED

## Issues Found: None

## Recommendations: None
```

---

## Success Checklist

- [ ] GitHub secrets configured
- [ ] Terraform modules validate
- [ ] Test GitHub issue created
- [ ] Workflow triggers automatically
- [ ] Validation passes for valid form
- [ ] AWS account created
- [ ] 3 VPCs created (dev/staging/prod)
- [ ] Each VPC has subnets, NAT, IGW
- [ ] GitHub issue closed with completion comment
- [ ] Validation fails for invalid email
- [ ] Validation fails for invalid cost center
- [ ] Validation fails for budget out of range
- [ ] Test results documented

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow doesn't trigger | Add `account-factory` label to issue |
| Validation fails with email error | Use format: `team@hospital.com` |
| Terraform apply fails | Verify GitHub Actions role has AdministratorAccess |
| Account not created | Check GitHub Actions logs for errors |
| VPCs not created | Verify cross-account role exists in new account |

---

## Next Steps After Phase 5

1. **Update Implementation Plan**
   - Mark Phase 5 as complete
   - Update progress to 90%

2. **Prepare Phase 6 Launch**
   - Soft launch to cloud team
   - Limited launch to 1-2 pilot teams
   - Full launch to all teams

3. **Monitor and Support**
   - Watch for issues
   - Gather feedback
   - Iterate and improve

---

## Reference Documents

- **Full Guide:** `ACCOUNT_FACTORY_PHASE5_EXECUTION.md`
- **Implementation Plan:** `ACCOUNT_FACTORY_IMPLEMENTATION.md`
- **Status Summary:** `STATUS_SUMMARY.md`
- **Testing Guide:** `ACCOUNT_FACTORY_TESTING_GUIDE.md`

---

**Estimated Time:** 45 minutes  
**Target Completion:** February 27, 2026  
**Next Phase:** Phase 6 - Launch & Monitoring (Feb 28, 2026)

