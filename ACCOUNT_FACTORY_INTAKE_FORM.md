# AWS Hospital Account Factory - Intake Form Documentation

**Purpose:** Standardized intake form for hospital teams requesting new AWS accounts

**Version:** 1.0  
**Last Updated:** February 26, 2026

---

## Overview

This document defines the 10 essential questions that hospital teams must answer to request a new AWS account. Based on these answers, the Account Factory will automatically:

1. Create a new AWS account
2. Set up 3 environments (dev, staging, prod)
3. Deploy the hospital landing zone to each environment
4. Configure IAM, security, compliance, and cost controls
5. Provide team access credentials

**No manual intervention required** - the entire process is automated via GitHub CI/CD.

---

## The 10 Essential Questions

### Question 1: Team Name

**Field Name:** `team_name`  
**Type:** Text (required)  
**Character Limit:** 50  
**Pattern:** Alphanumeric, hyphens, underscores only  
**Example:** `radiology-team`, `pharmacy-department`, `lab-services`

**Purpose:** Identify which hospital team/department is requesting the account

**Validation Rules:**
- Must be unique (no duplicate team names)
- Must be lowercase
- Must not contain spaces
- Must be 3-50 characters

**Used For:**
- AWS account naming
- Resource tagging
- Cost allocation
- Team identification

---

### Question 2: Team Lead / Owner

**Field Name:** `team_lead_name`  
**Type:** Text (required)  
**Character Limit:** 100  
**Example:** `Dr. John Smith`, `Jane Doe`

**Purpose:** Primary contact and account owner for the team

**Validation Rules:**
- Must be a valid person name
- Must be 3-100 characters
- Will be used for account notifications

**Used For:**
- Account owner designation
- Primary contact for notifications
- Access request approvals
- Escalation point

---

### Question 3: Team Email

**Field Name:** `team_email`  
**Type:** Email (required)  
**Example:** `radiology-team@hospital.com`, `pharmacy@hospital.com`

**Purpose:** Email address for team notifications and account access

**Validation Rules:**
- Must be valid email format
- Should be team distribution list (not individual)
- Must be hospital domain (@hospital.com)
- Will receive account credentials and notifications

**Used For:**
- Sending account credentials
- Deployment notifications
- Cost alerts
- Security notifications
- Account access invitations

---

### Question 4: Cost Center

**Field Name:** `cost_center`  
**Type:** Text (required)  
**Pattern:** CC-DEPARTMENT-XXX  
**Example:** `CC-RADIOLOGY-001`, `CC-PHARMACY-002`, `CC-LAB-003`

**Purpose:** For billing, chargeback, and cost allocation

**Validation Rules:**
- Must follow pattern: CC-[DEPARTMENT]-[NUMBER]
- Must be valid hospital cost center
- Used for AWS billing tags
- Enables department-level cost tracking

**Used For:**
- AWS cost allocation tags
- Monthly billing reports
- Department chargeback
- Budget tracking
- Cost anomaly detection

---

### Question 5: Data Classification

**Field Name:** `data_classification`  
**Type:** Dropdown (required)  
**Options:**
- `public` - No sensitive data
- `internal` - Internal hospital data
- `confidential` - Patient data (PII)
- `restricted` - Highly sensitive (PHI, genetic data)

**Example:** `confidential` (for patient-facing systems)

**Purpose:** Determine security controls and compliance requirements

**Validation Rules:**
- Must select one option
- Determines encryption requirements
- Determines access controls
- Determines audit logging level

**Used For:**
- Security group configuration
- Encryption requirements
- Access control policies
- Audit logging level
- Compliance controls

**Security Implications:**
- **Public:** Standard security controls
- **Internal:** Enhanced encryption, access logging
- **Confidential:** HIPAA controls, encryption, audit trails
- **Restricted:** Maximum security, encryption, MFA, audit trails

---

### Question 6: Business Criticality

**Field Name:** `business_criticality`  
**Type:** Dropdown (required)  
**Options:**
- `low` - Non-critical, experimental
- `medium` - Important but not patient-facing
- `high` - Patient-facing or critical operations
- `critical` - Life-critical systems

**Example:** `high` (for patient-facing systems)

**Purpose:** Determine availability and disaster recovery requirements

**Validation Rules:**
- Must select one option
- Determines multi-AZ requirements
- Determines backup frequency
- Determines RTO/RPO targets

**Used For:**
- Multi-AZ deployment decisions
- Backup and recovery policies
- Monitoring and alerting levels
- SLA definitions
- Disaster recovery planning

**Availability Implications:**
- **Low:** Single AZ acceptable, daily backups
- **Medium:** Multi-AZ recommended, daily backups
- **High:** Multi-AZ required, hourly backups
- **Critical:** Multi-AZ required, real-time replication

---

### Question 7: Primary Use Case

**Field Name:** `primary_use_case`  
**Type:** Dropdown (required)  
**Options:**
- `ehr-system` - Electronic Health Records
- `telemedicine` - Telemedicine Platform
- `medical-imaging` - Medical Imaging / PACS
- `lab-system` - Lab Information System
- `patient-portal` - Patient Portal
- `analytics` - Healthcare Analytics
- `research` - Medical Research
- `other` - Other (specify)

**Example:** `ehr-system`, `telemedicine`, `lab-system`

**Purpose:** Understand what the team will build to recommend services

**Validation Rules:**
- Must select one option
- If "other", must provide description
- Used for service recommendations

**Used For:**
- Service recommendations
- Architecture guidance
- Compliance requirement determination
- Resource sizing
- Cost estimation

**Service Recommendations by Use Case:**
- **EHR System:** RDS, S3, Lambda, CloudWatch
- **Telemedicine:** EC2, RDS, S3, CloudFront
- **Medical Imaging:** S3, EC2, RDS, Lambda
- **Lab System:** RDS, Lambda, SNS
- **Patient Portal:** EC2, RDS, CloudFront
- **Analytics:** Athena, Glue, QuickSight
- **Research:** EC2, S3, SageMaker

---

### Question 8: Estimated Monthly Budget

**Field Name:** `estimated_monthly_budget`  
**Type:** Number (required)  
**Unit:** USD  
**Minimum:** $100  
**Maximum:** $100,000  
**Example:** `5000`, `10000`, `25000`

**Purpose:** Cost control and forecasting

**Validation Rules:**
- Must be number between $100-$100,000
- Used for budget alerts
- Used for cost anomaly detection
- Used for forecasting

**Used For:**
- AWS budget alerts (120% of estimate)
- Cost anomaly detection
- Monthly cost reports
- Capacity planning
- ROI calculations

**Budget Guidance by Use Case:**
- **EHR System:** $5,000-$25,000/month
- **Telemedicine:** $3,000-$15,000/month
- **Medical Imaging:** $10,000-$50,000/month
- **Lab System:** $2,000-$10,000/month
- **Patient Portal:** $2,000-$8,000/month
- **Analytics:** $5,000-$20,000/month
- **Research:** $3,000-$30,000/month

---

### Question 9: Additional AWS Services (Optional)

**Field Name:** `additional_services`  
**Type:** Checkboxes (optional)  
**Options:**
- `rds` - Relational Database (PostgreSQL, MySQL, etc.)
- `s3` - Object Storage
- `lambda` - Serverless Functions
- `dynamodb` - NoSQL Database
- `elasticache` - In-Memory Cache
- `sqs` - Message Queue
- `sns` - Notifications
- `cloudfront` - CDN
- `kinesis` - Streaming Data
- `sagemaker` - Machine Learning
- `other` - Other (specify)

**Example:** `rds`, `s3`, `lambda`

**Purpose:** Identify additional services beyond landing zone

**Validation Rules:**
- Can select multiple options
- If "other", must provide description
- Used for IAM policy generation

**Used For:**
- IAM policy generation
- Service enablement
- Cost estimation
- Architecture planning

**Note:** Landing zone provides VPC, NAT, IGW, security groups. These are additional services.

---

### Question 10: Compliance Requirements

**Field Name:** `compliance_requirements`  
**Type:** Checkboxes (required)  
**Options:**
- `hipaa` - HIPAA (Health Insurance Portability and Accountability Act)
- `hitech` - HITECH (Health Information Technology for Economic and Clinical Health)
- `soc2` - SOC 2 (Service Organization Control)
- `pci-dss` - PCI DSS (Payment Card Industry Data Security Standard)
- `gdpr` - GDPR (General Data Protection Regulation)
- `none` - No specific compliance requirements

**Example:** `hipaa`, `hitech`, `soc2`

**Purpose:** Determine compliance controls and audit requirements

**Validation Rules:**
- Must select at least one option
- Multiple selections allowed
- Determines encryption, logging, access controls

**Used For:**
- Compliance control enforcement
- Audit logging configuration
- Encryption requirements
- Access control policies
- Compliance reporting

**Compliance Implications:**
- **HIPAA:** Encryption, audit logs, access controls, data residency
- **HITECH:** Enhanced HIPAA controls, breach notification
- **SOC 2:** Monitoring, logging, access controls, change management
- **PCI DSS:** Network segmentation, encryption, access controls
- **GDPR:** Data residency, encryption, right to deletion

---

## Form Submission Process

### Step 1: Team Fills Form
Team lead completes all 10 questions via GitHub issue template

### Step 2: Validation
GitHub Actions validates:
- All required fields are filled
- Data formats are correct
- Values are within acceptable ranges
- Team name is unique
- Email is valid hospital domain

### Step 3: Automatic Provisioning
If validation passes:
- Terraform provisions new AWS account
- 3 environments created (dev/staging/prod)
- Landing zone deployed to each environment
- IAM roles and policies created
- Cost allocation tags applied
- Credentials generated

### Step 4: Team Notification
Team receives email with:
- AWS account ID
- Account access credentials
- Environment details (dev/staging/prod)
- Getting started guide
- Support contact information

### Step 5: Team Access
Team can immediately:
- Log in to AWS console
- Deploy applications
- Use landing zone infrastructure
- Access monitoring and logs

---

## Example Completed Form

```
Team Name: radiology-team
Team Lead: Dr. Sarah Johnson
Team Email: radiology-team@hospital.com
Cost Center: CC-RADIOLOGY-001
Data Classification: confidential
Business Criticality: high
Primary Use Case: medical-imaging
Estimated Monthly Budget: $15,000
Additional Services: rds, s3, lambda
Compliance Requirements: hipaa, hitech, soc2
```

**Result:**
- AWS Account created: 123456789012
- Environments: dev, staging, prod
- Each environment has:
  - VPC (10.0.0.0/16)
  - Public subnets (DMZ)
  - Private subnets (applications)
  - NAT Gateways
  - Internet Gateway
  - VPC Flow Logs
  - Security groups
  - IAM roles
  - Cost allocation tags
  - HIPAA/HITECH/SOC2 controls

---

## Validation Rules Summary

| Question | Required | Type | Validation |
|----------|----------|------|-----------|
| Team Name | Yes | Text | Unique, lowercase, 3-50 chars |
| Team Lead | Yes | Text | 3-100 chars |
| Team Email | Yes | Email | Valid hospital domain |
| Cost Center | Yes | Text | Pattern: CC-DEPT-XXX |
| Data Classification | Yes | Dropdown | One of 4 options |
| Business Criticality | Yes | Dropdown | One of 4 options |
| Primary Use Case | Yes | Dropdown | One of 8 options |
| Monthly Budget | Yes | Number | $100-$100,000 |
| Additional Services | No | Checkboxes | Multiple allowed |
| Compliance | Yes | Checkboxes | At least one required |

---

## Error Handling

### Validation Errors

If validation fails, team receives error message:

```
❌ Account Request Failed

Errors:
- Team Name: Must be lowercase (you provided: Radiology-Team)
- Cost Center: Invalid format (expected: CC-DEPT-XXX)
- Team Email: Must be hospital domain (you provided: john@gmail.com)

Please correct these errors and resubmit.
```

### Provisioning Errors

If provisioning fails, team receives:

```
⚠️ Account Provisioning Failed

Error: AWS account creation failed
Reason: Account limit reached for organization

Action: Contact Cloud Team (cloud-team@hospital.com)
Reference: ACCT-20260226-001
```

---

## Support & FAQ

### Q: How long does account creation take?
**A:** 5-10 minutes from form submission to account ready

### Q: Can we change answers after submission?
**A:** Yes, submit a new form with updated information

### Q: What if we need more than 3 environments?
**A:** Contact cloud team, additional environments can be added

### Q: Can we change the monthly budget later?
**A:** Yes, update via AWS console or contact cloud team

### Q: What if we need additional AWS services?
**A:** Contact cloud team, services can be enabled post-provisioning

### Q: How do we access the account?
**A:** Credentials sent to team email, use AWS console or CLI

### Q: Is there a cost for the landing zone?
**A:** No, landing zone is included. You pay for additional services.

### Q: Can we delete the account?
**A:** Yes, contact cloud team for account deletion

---

## Next Steps

1. Team fills out intake form via GitHub issue
2. GitHub Actions validates submission
3. Terraform provisions account and environments
4. Team receives credentials and access
5. Team starts deploying applications

---

**For Questions:** Contact Cloud Team (cloud-team@hospital.com)  
**Documentation:** [Account Factory Implementation](ACCOUNT_FACTORY_IMPLEMENTATION.md)  
**Main README:** [Hospital Landing Zone](README.md)
