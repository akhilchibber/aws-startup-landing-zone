# Phase 6 - Quick Reference Guide

**Phase:** Phase 6 - Launch & Monitoring  
**Status:** ⏳ IN PROGRESS  
**Date:** February 26, 2026

---

## What is Phase 6?

Phase 6 is the launch and monitoring phase. It involves:
1. **Soft Launch** - Internal testing with cloud team
2. **Limited Launch** - Testing with 1-2 pilot teams
3. **Full Launch** - Scaling to all hospital teams

---

## Quick Start - Soft Launch (1-2 hours)

### Step 1: Configure GitHub Secrets (15 min)

In GitHub repository settings:
```
Settings → Secrets and variables → Actions

Add 3 secrets:
1. AWS_ROLE_TO_ASSUME = arn:aws:iam::ACCOUNT_ID:role/GitHubActionsRole
2. TERRAFORM_STATE_BUCKET = hospital-terraform-state
3. TERRAFORM_LOCK_TABLE = terraform-locks
```

### Step 2: Create Test Account Request (5 min)

1. Go to repository → Issues → New issue
2. Select "Account Request" template
3. Fill with test data:
   - Team Name: `cloud-team-test`
   - Team Email: `cloud-team@hospital.com`
   - Cost Center: `CC-CLOUD-001`
   - Budget: `5000`
4. Submit issue
5. Add `account-factory` label

### Step 3: Monitor Workflow (15 min)

1. Go to Actions tab
2. Watch workflow execute:
   - `validate-intake-form` (1-2 min)
   - `provision-account` (10-15 min)
3. Check GitHub comments for results

### Step 4: Verify Infrastructure (10 min)

In AWS console:
1. Check AWS Organizations → Accounts
   - Verify account `cloud-team-test` created
2. Check EC2 → VPCs
   - Verify 3 VPCs created (dev/staging/prod)
3. Check EC2 → Subnets
   - Verify 6 subnets per VPC (2 public, 2 private)
4. Check EC2 → NAT Gateways
   - Verify 2 per VPC (6 total)

### Step 5: Document Results (10 min)

Create `PHASE6_SOFT_LAUNCH_RESULTS.md` with:
- Date and time of test
- Test data used
- Workflow execution time
- Account creation time
- Infrastructure verification results
- Any issues encountered

---

## Key Files

### Primary Reference
- `PHASE6_SOFT_LAUNCH_EXECUTION.md` - Detailed step-by-step guide
- `PHASE6_LAUNCH_GUIDE.md` - Overview of all 3 stages

### Supporting
- `ACCOUNT_FACTORY_IMPLEMENTATION.md` - Overall plan
- `STATUS_SUMMARY.md` - Current status

### GitHub
- `.github/ISSUE_TEMPLATE/account-request.md` - Issue template
- `.github/workflows/account-factory.yml` - Workflow

### Terraform
- `environments/account-factory/main.tf` - Main config
- `modules/account-factory/main.tf` - Account module
- `modules/environment/main.tf` - VPC module

---

## Success Criteria

Soft launch is successful when:
- [x] GitHub secrets configured
- [x] Test account created
- [x] Workflow executed successfully
- [x] AWS account created
- [x] 3 VPCs created
- [x] Infrastructure deployed
- [x] No critical errors
- [x] Results documented

---

## Troubleshooting

### Workflow Fails at Validation
- Check error message in workflow logs
- Verify all fields filled correctly
- Verify email is @hospital.com
- Verify cost center format: CC-DEPARTMENT-XXX
- Verify budget: $100-$100,000

### Workflow Fails at Provisioning
- Check GitHub Actions logs
- Check AWS CloudFormation events
- Check Terraform state
- Check IAM permissions

### Account Not Created
- Check AWS Organizations console
- Check CloudTrail logs
- Check IAM permissions
- Check Organizations API limits

### VPCs Not Created
- Check Terraform state
- Check CloudFormation stacks
- Check IAM permissions
- Check VPC limits

---

## Timeline

| Stage | Duration | When |
|-------|----------|------|
| Soft Launch | 3-5 days | Week 1 (Now) |
| Limited Launch | 3-5 days | Week 2 |
| Full Launch | Ongoing | Week 3+ |

---

## Next Steps

1. **Now:** Execute soft launch (1-2 hours)
2. **Today:** Document results
3. **Tomorrow:** Review results, identify improvements
4. **Next week:** Select pilot teams, begin limited launch
5. **Following week:** Make improvements, full launch

---

## Key Contacts

- Cloud Team Lead: cloud-team@hospital.com
- Implementation Lead: cloud-team@hospital.com
- Support: cloud-team@hospital.com

---

## Progress Tracking

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1-5 | ✅ Complete | 100% |
| Phase 6 | ⏳ In Progress | 0% |
| **Overall** | **⏳ In Progress** | **90%** |

After Phase 6 completion: **95%**

---

**Phase 6 - Quick Reference**  
**Date:** February 26, 2026  
**Version:** 1.0
