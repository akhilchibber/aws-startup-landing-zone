# Phase 5 - Quick Reference Card

**Print this page for quick reference during Phase 5 execution**

---

## Phase 5 Overview

| Item | Details |
|------|---------|
| **Phase** | Phase 5 - Testing & Documentation |
| **Duration** | 45-60 minutes |
| **Status** | Ready for Execution |
| **Overall Progress** | 87% (was 85%) |
| **Completion Target** | February 27, 2026 |

---

## 7 Steps to Complete Phase 5

### Step 1: Configure GitHub Secrets (5 min)
```bash
# Create IAM role
aws iam create-role \
  --role-name GitHubActionsRole \
  --assume-role-policy-document file:///tmp/trust-policy.json

# Get role ARN
aws iam get-role --role-name GitHubActionsRole \
  --query 'Role.Arn' --output text

# Add to GitHub: Settings → Secrets and variables → Actions
# Secret 1: AWS_ROLE_TO_ASSUME = arn:aws:iam::ACCOUNT_ID:role/GitHubActionsRole
# Secret 2: TERRAFORM_STATE_BUCKET = hospital-terraform-state
# Secret 3: TERRAFORM_LOCK_TABLE = terraform-locks
```

### Step 2: Validate Terraform (5 min)
```bash
# Validate account factory module
cd modules/account-factory && terraform init && terraform validate

# Validate environment module
cd ../environment && terraform init && terraform validate

# Validate account factory configuration
cd ../../environments/account-factory && terraform init -backend=false && terraform validate
```

### Step 3: Test Valid Account (15-20 min)
```
GitHub Issue Data:
- Team Name: radiology-test-team
- Team Lead: Dr. Test User
- Team Email: radiology-test@hospital.com
- Cost Center: CC-RADIOLOGY-001
- Data Classification: Confidential
- Business Criticality: High
- Primary Use Case: Medical Imaging / PACS
- Monthly Budget: 2500
- Additional Services: RDS, S3
- Compliance: HIPAA, HITECH

Expected: ✅ Account created, 3 VPCs, infrastructure deployed
```

### Step 4: Test Invalid Email (5 min)
```
GitHub Issue Data:
- Team Email: test@gmail.com (INVALID)

Expected: ❌ Validation fails with error message
```

### Step 5: Test Invalid Cost Center (5 min)
```
GitHub Issue Data:
- Cost Center: INVALID-FORMAT (should be CC-DEPT-XXX)

Expected: ❌ Validation fails with error message
```

### Step 6: Test Invalid Budget (5 min)
```
GitHub Issue Data:
- Monthly Budget: 50 (minimum is $100)

Expected: ❌ Validation fails with error message
```

### Step 7: Document Results (10 min)
```
Update:
1. ACCOUNT_FACTORY_TEST_RESULTS.md
2. ACCOUNT_FACTORY_IMPLEMENTATION.md
3. STATUS_SUMMARY.md
```

---

## Verification Commands

### Verify Account Created
```bash
aws organizations list-accounts \
  --query 'Accounts[?Name==`radiology-test-team`]' \
  --output json
```

### Verify VPCs Created
```bash
aws ec2 describe-vpcs \
  --filters "Name=tag:Team,Values=radiology-test-team" \
  --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Environment`].Value|[0]]' \
  --output table
```

### Verify Subnets
```bash
aws ec2 describe-subnets \
  --filters "Name=tag:Team,Values=radiology-test-team" \
  --query 'Subnets[*].[SubnetId,CidrBlock,Tags[?Key==`Type`].Value|[0]]' \
  --output table
```

### Verify NAT Gateways
```bash
aws ec2 describe-nat-gateways \
  --filter "Name=tag:Team,Values=radiology-test-team" \
  --query 'NatGateways[*].[NatGatewayId,State]' \
  --output table
```

### Verify Internet Gateways
```bash
aws ec2 describe-internet-gateways \
  --filters "Name=tag:Team,Values=radiology-test-team" \
  --query 'InternetGateways[*].[InternetGatewayId]' \
  --output table
```

### Verify Route Tables
```bash
aws ec2 describe-route-tables \
  --filters "Name=tag:Team,Values=radiology-test-team" \
  --query 'RouteTables[*].[RouteTableId,Tags[?Key==`Type`].Value|[0]]' \
  --output table
```

---

## Expected Results

### Test 1: Valid Account ✅
- [ ] Account created in Organizations
- [ ] 3 VPCs created (10.0.0.0/16, 10.1.0.0/16, 10.2.0.0/16)
- [ ] 12 subnets created (4 per VPC)
- [ ] 6 NAT Gateways created (2 per VPC)
- [ ] 3 Internet Gateways created (1 per VPC)
- [ ] 12 route tables created (4 per VPC)
- [ ] GitHub issue closed with completion comment

### Test 2: Invalid Email ❌
- [ ] Validation fails
- [ ] Error: "Team Email: Must be valid hospital domain (@hospital.com)"
- [ ] Issue remains open
- [ ] Issue labeled `validation-failed`

### Test 3: Invalid Cost Center ❌
- [ ] Validation fails
- [ ] Error: "Cost Center: Must follow format CC-DEPARTMENT-XXX"
- [ ] Issue remains open
- [ ] Issue labeled `validation-failed`

### Test 4: Invalid Budget ❌
- [ ] Validation fails
- [ ] Error: "Monthly Budget: Must be between $100-$100,000"
- [ ] Issue remains open
- [ ] Issue labeled `validation-failed`

---

## Success Criteria Checklist

- [ ] GitHub secrets configured (3 secrets)
- [ ] Terraform modules validated (3 modules)
- [ ] Test 1: PASS (Account + 3 VPCs + Infrastructure)
- [ ] Test 2: PASS (Invalid email rejected)
- [ ] Test 3: PASS (Invalid cost center rejected)
- [ ] Test 4: PASS (Invalid budget rejected)
- [ ] No critical issues found
- [ ] Documentation updated
- [ ] Implementation plan updated

---

## Key Files

| File | Purpose |
|------|---------|
| `PHASE5_EXECUTION_STEPS.md` | Step-by-step instructions |
| `ACCOUNT_FACTORY_PHASE5_EXECUTION.md` | Comprehensive guide |
| `PHASE5_QUICK_START.md` | Quick reference |
| `ACCOUNT_FACTORY_TEST_RESULTS.md` | Test results |
| `ACCOUNT_FACTORY_IMPLEMENTATION.md` | Implementation plan |
| `STATUS_SUMMARY.md` | Current status |

---

## Troubleshooting

### Workflow doesn't trigger
**Solution:** Add `account-factory` label to GitHub issue

### Validation fails with "Access Denied"
**Solution:** Verify GitHub secrets are configured correctly

### Terraform apply fails
**Solution:** Check AWS credentials and IAM role permissions

### Account not created
**Solution:** Check AWS Organizations setup and OU configuration

---

## Timeline

```
Step 1: 5 min   ├─ Configure GitHub Secrets
Step 2: 5 min   ├─ Validate Terraform
Step 3: 20 min  ├─ Test Valid Account
Step 4: 5 min   ├─ Test Invalid Email
Step 5: 5 min   ├─ Test Invalid Cost Center
Step 6: 5 min   ├─ Test Invalid Budget
Step 7: 10 min  └─ Document Results
─────────────────────────────────────
Total: 55 minutes
```

---

## After Phase 5

**Phase 6: Launch & Monitoring**
- Soft launch to cloud team
- Limited launch to pilot teams
- Full launch to all teams

**Overall Progress:** 87% → 90%

---

## Contact

**Support:** cloud-team@hospital.com  
**Documentation:** See `PHASE5_EXECUTION_STEPS.md`

---

**Phase 5 Status:** ✅ Ready for Execution  
**Date:** February 26, 2026  
**Duration:** 45-60 minutes
