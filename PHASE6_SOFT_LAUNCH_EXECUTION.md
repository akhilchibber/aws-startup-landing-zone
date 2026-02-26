# Phase 6 - Soft Launch Execution Guide

**Phase:** Phase 6 - Launch & Monitoring  
**Stage:** Stage 1 - Soft Launch (Internal Testing)  
**Status:** ⏳ IN PROGRESS  
**Date:** February 26, 2026  
**Duration:** 3-5 days  
**Audience:** Cloud team (internal testing)  
**Goal:** Verify system works in production environment

---

## Overview

This guide walks through executing the soft launch of the AWS Hospital Account Factory. The soft launch is internal testing with the cloud team to verify the system works before expanding to pilot teams.

**What will happen:**
1. Configure GitHub secrets in the repository
2. Create a test account request via GitHub issue
3. Monitor the GitHub Actions workflow execution
4. Verify AWS account creation
5. Verify infrastructure deployment
6. Document results

**Expected timeline:** 1-2 hours total

---

## Prerequisites

Before starting, ensure you have:
- [ ] Access to GitHub repository
- [ ] Access to AWS Organizations console
- [ ] Access to AWS IAM console
- [ ] AWS CLI installed locally (optional but helpful)
- [ ] Terraform installed locally (optional but helpful)

---

## Step 1: Configure GitHub Secrets

GitHub secrets are required for the workflow to authenticate with AWS and access Terraform state.

### 1.1 Create IAM Role for GitHub Actions

First, create an IAM role that GitHub Actions will assume to provision accounts.

**In AWS Console:**

1. Go to IAM → Roles → Create role
2. Select "Web identity" as trusted entity type
3. Configure trust relationship:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
           },
           "StringLike": {
             "token.actions.githubusercontent.com:sub": "repo:GITHUB_ORG/GITHUB_REPO:*"
           }
         }
       }
     ]
   }
   ```

4. Attach policies:
   - AdministratorAccess (for testing - restrict in production)
   - Or create custom policy with specific permissions

5. Note the role ARN: `arn:aws:iam::ACCOUNT_ID:role/GitHubActionsRole`

### 1.2 Create S3 Bucket for Terraform State

Create an S3 bucket to store Terraform state files.

**In AWS Console:**

1. Go to S3 → Create bucket
2. Bucket name: `hospital-terraform-state`
3. Enable versioning:
   - Properties → Versioning → Enable
4. Enable encryption:
   - Properties → Default encryption → Enable
5. Block public access:
   - Permissions → Block all public access → Enable

### 1.3 Create DynamoDB Table for Terraform Locks

Create a DynamoDB table for Terraform state locking.

**In AWS Console:**

1. Go to DynamoDB → Create table
2. Table name: `terraform-locks`
3. Partition key: `LockID` (String)
4. Billing mode: On-demand
5. Create table

### 1.4 Add GitHub Secrets

Add the required secrets to the GitHub repository.

**In GitHub:**

1. Go to repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add three secrets:

**Secret 1: AWS_ROLE_TO_ASSUME**
- Name: `AWS_ROLE_TO_ASSUME`
- Value: `arn:aws:iam::ACCOUNT_ID:role/GitHubActionsRole`
- Replace ACCOUNT_ID with your AWS account ID

**Secret 2: TERRAFORM_STATE_BUCKET**
- Name: `TERRAFORM_STATE_BUCKET`
- Value: `hospital-terraform-state`

**Secret 3: TERRAFORM_LOCK_TABLE**
- Name: `TERRAFORM_LOCK_TABLE`
- Value: `terraform-locks`

### 1.5 Verify Secrets

Verify all three secrets are configured:

1. Go to repository → Settings → Secrets and variables → Actions
2. Confirm you see:
   - AWS_ROLE_TO_ASSUME
   - TERRAFORM_STATE_BUCKET
   - TERRAFORM_LOCK_TABLE

**Status:** ✅ GitHub secrets configured

---

## Step 2: Verify GitHub Configuration

Verify the GitHub issue template and workflow are properly configured.

### 2.1 Verify Issue Template

1. Go to repository → .github/ISSUE_TEMPLATE/
2. Confirm `account-request.md` exists
3. Verify it contains all 10 intake questions

### 2.2 Verify Workflow

1. Go to repository → .github/workflows/
2. Confirm `account-factory.yml` exists
3. Verify workflow has two jobs:
   - `validate-intake-form`
   - `provision-account`

**Status:** ✅ GitHub configuration verified

---

## Step 3: Create Test Account Request

Create a test GitHub issue to trigger the account factory workflow.

### 3.1 Create New Issue

1. Go to repository → Issues → New issue
2. Click "Account Request" template
3. Fill in the form with test data:

```
Team Name: cloud-team-test
Team Lead: Cloud Team Lead
Team Email: cloud-team@hospital.com
Cost Center: CC-CLOUD-001
Data Classification: Confidential
Business Criticality: High
Primary Use Case: Cloud Infrastructure
Monthly Budget: 5000
Additional Services: RDS, S3, Lambda
Compliance Requirements: HIPAA
```

### 3.2 Submit Issue

1. Click "Submit new issue"
2. GitHub will create the issue
3. Note the issue number (e.g., #1)

### 3.3 Add Label to Trigger Workflow

The workflow only runs when the `account-factory` label is present.

1. On the issue page, click "Labels"
2. Select `account-factory` label
3. The workflow should start automatically

**Status:** ✅ Test account request created

---

## Step 4: Monitor Workflow Execution

Monitor the GitHub Actions workflow as it runs.

### 4.1 Watch Workflow Progress

1. Go to repository → Actions
2. Find the workflow run (should be at the top)
3. Click on it to see details
4. Watch the jobs execute:
   - `validate-intake-form` (1-2 minutes)
   - `provision-account` (10-15 minutes)

### 4.2 Check Validation Job

The validation job should:
1. Parse the intake form
2. Validate all fields
3. Post a comment with validation result

**Expected comment:**
```
✅ Validation Passed

Your account request has been validated successfully. 
Provisioning will begin shortly.

Status: Processing
```

### 4.3 Check Provisioning Job

The provisioning job should:
1. Initialize Terraform
2. Plan infrastructure
3. Apply Terraform configuration
4. Extract outputs
5. Post completion comment

**Expected comment:**
```
✅ Account Provisioning Complete

Account Details:
- Team: cloud-team-test
- Primary Account: [ACCOUNT_ID]
- Dev Environment: [DEV_ACCOUNT]
- Staging Environment: [STAGING_ACCOUNT]
- Prod Environment: [PROD_ACCOUNT]

Next Steps:
1. Check your email for credentials
2. Log in to AWS console
3. Review landing zone infrastructure
4. Start deploying applications

Support: Contact cloud-team@hospital.com
```

### 4.4 Monitor for Errors

If the workflow fails:
1. Click on the failed job
2. Expand the step that failed
3. Read the error message
4. Check the troubleshooting guide below

**Status:** ✅ Workflow execution monitored

---

## Step 5: Verify AWS Account Creation

Verify that the AWS account was created successfully.

### 5.1 Check AWS Organizations

1. Go to AWS Organizations console
2. Click "Accounts"
3. Look for account named `cloud-team-test`
4. Verify account status is "ACTIVE"

**Expected result:**
- Account name: `cloud-team-test`
- Account ID: [12-digit number]
- Status: ACTIVE
- Email: cloud-team@hospital.com

### 5.2 Check Account Details

1. Click on the account
2. Verify:
   - Account name: `cloud-team-test`
   - Email: `cloud-team@hospital.com`
   - Status: ACTIVE
   - ARN: `arn:aws:organizations::MASTER_ACCOUNT:account/o-XXXXX/ACCOUNT_ID`

**Status:** ✅ AWS account created

---

## Step 6: Verify Infrastructure Deployment

Verify that the landing zone infrastructure was deployed to each environment.

### 6.1 Check VPCs Created

1. Go to EC2 console
2. Click "VPCs"
3. Look for VPCs with tag `Team=cloud-team-test`
4. Verify 3 VPCs exist (dev, staging, prod)

**Expected VPCs:**
- `cloud-team-test-dev` (10.0.0.0/16)
- `cloud-team-test-staging` (10.1.0.0/16)
- `cloud-team-test-prod` (10.2.0.0/16)

### 6.2 Check Subnets

1. Click "Subnets"
2. Filter by VPC
3. Verify each VPC has 4 subnets:
   - 2 public subnets
   - 2 private subnets

**Expected subnets per VPC:**
- Public subnet 1: 10.x.1.0/24
- Public subnet 2: 10.x.2.0/24
- Private subnet 1: 10.x.11.0/24
- Private subnet 2: 10.x.12.0/24

### 6.3 Check NAT Gateways

1. Click "NAT Gateways"
2. Filter by VPC
3. Verify 2 NAT Gateways per VPC (one per availability zone)

**Expected NAT Gateways:**
- 6 total (2 per VPC × 3 VPCs)
- Each in a different public subnet

### 6.4 Check Internet Gateways

1. Click "Internet Gateways"
2. Filter by VPC
3. Verify 1 IGW per VPC

**Expected Internet Gateways:**
- 3 total (1 per VPC)
- Each attached to its VPC

### 6.5 Check Route Tables

1. Click "Route Tables"
2. Filter by VPC
3. Verify 4 route tables per VPC:
   - 1 public route table
   - 2 private route tables (one per AZ)
   - 1 default route table

**Expected route tables:**
- 12 total (4 per VPC × 3 VPCs)

### 6.6 Check VPC Flow Logs

1. Click "VPC Flow Logs"
2. Filter by VPC
3. Verify 1 flow log per VPC

**Expected flow logs:**
- 3 total (1 per VPC)
- Destination: CloudWatch Logs

**Status:** ✅ Infrastructure deployed

---

## Step 7: Document Soft Launch Results

Document the results of the soft launch testing.

### 7.1 Create Soft Launch Results Document

Create a new file: `PHASE6_SOFT_LAUNCH_RESULTS.md`

Include:
- Date and time of test
- Test data used
- Workflow execution time
- Account creation time
- Infrastructure verification results
- Any issues encountered
- Recommendations

### 7.2 Example Results

```markdown
# Soft Launch Results

**Date:** February 26, 2026  
**Time:** 14:00 UTC  
**Tester:** Cloud Team  
**Status:** ✅ SUCCESS

## Test Data
- Team Name: cloud-team-test
- Team Email: cloud-team@hospital.com
- Cost Center: CC-CLOUD-001
- Budget: $5,000

## Execution Timeline
- Issue created: 14:00
- Validation started: 14:01
- Validation completed: 14:02 (1 minute)
- Provisioning started: 14:02
- Provisioning completed: 14:15 (13 minutes)
- Total time: 15 minutes

## Verification Results
- ✅ AWS account created
- ✅ 3 VPCs created
- ✅ 12 subnets created
- ✅ 6 NAT Gateways created
- ✅ 3 Internet Gateways created
- ✅ 12 route tables created
- ✅ 3 VPC Flow Logs created

## Issues Encountered
- None

## Recommendations
- System is ready for limited launch
- Consider monitoring workflow execution time
- Consider adding more detailed logging
```

**Status:** ✅ Results documented

---

## Troubleshooting

### Issue: Workflow Fails at Validation

**Symptoms:**
- Validation job fails
- Error message in workflow logs

**Troubleshooting:**
1. Check the error message in the workflow logs
2. Verify all required fields are filled
3. Verify email is @hospital.com domain
4. Verify cost center format is CC-DEPARTMENT-XXX
5. Verify budget is between $100-$100,000

**Resolution:**
- Edit the GitHub issue
- Correct the invalid field
- Re-add the `account-factory` label
- Workflow will run again

### Issue: Workflow Fails at Provisioning

**Symptoms:**
- Validation passes but provisioning fails
- Error message in workflow logs

**Troubleshooting:**
1. Check GitHub Actions logs for error
2. Check AWS CloudFormation events
3. Check Terraform state
4. Check IAM permissions

**Resolution:**
- Check the specific error message
- Fix the underlying issue
- Manually delete the partial account if needed
- Retry the workflow

### Issue: AWS Account Not Created

**Symptoms:**
- Workflow completes but account not visible in Organizations

**Troubleshooting:**
1. Check AWS Organizations console
2. Check CloudTrail logs
3. Check IAM permissions
4. Check Organizations API limits

**Resolution:**
- Verify IAM role has Organizations permissions
- Check if account limit reached
- Manually create account if needed

### Issue: VPCs Not Created

**Symptoms:**
- Account created but VPCs missing
- Workflow shows success

**Troubleshooting:**
1. Check Terraform state
2. Check CloudFormation stacks
3. Check IAM permissions
4. Check VPC limits

**Resolution:**
- Check Terraform state for errors
- Manually create VPCs if needed
- Update Terraform configuration

---

## Success Criteria

Soft launch is successful when:

- [x] GitHub secrets configured
- [x] Test account request submitted
- [x] Workflow executed successfully
- [x] AWS account created
- [x] 3 VPCs created with correct configuration
- [x] Landing zone infrastructure deployed
- [x] GitHub issue closed with completion comment
- [x] No critical errors
- [x] Results documented
- [x] System ready for limited launch

---

## Next Steps

After successful soft launch:

1. **Review Results**
   - Review soft launch results document
   - Identify any issues or improvements

2. **Make Improvements**
   - Fix any issues found
   - Update documentation if needed
   - Update troubleshooting guide

3. **Prepare for Limited Launch**
   - Select 1-2 pilot teams
   - Prepare onboarding materials
   - Schedule kickoff meetings

4. **Begin Limited Launch**
   - Onboard pilot teams
   - Support pilot teams
   - Gather feedback

---

## Conclusion

The soft launch is the first stage of Phase 6. It verifies the system works in the production environment before expanding to pilot teams. After successful soft launch, the system is ready for limited launch to 1-2 pilot teams.

**Status:** ⏳ Soft Launch In Progress  
**Next Phase:** Limited Launch (after soft launch completion)

---

**Phase 6 - Soft Launch Execution Guide**  
**Date:** February 26, 2026  
**Version:** 1.0  
**Status:** ⏳ IN PROGRESS
