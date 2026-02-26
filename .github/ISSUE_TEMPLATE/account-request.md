---
name: AWS Account Request
about: Request a new AWS account for your hospital team
title: "Account Request: [Team Name]"
labels: account-factory, pending-review
assignees: ''

---

# AWS Hospital Account Request

**Please fill out all fields below to request a new AWS account.**

---

## 1. Team Name

**What is your team/department name?**

Example: `radiology-team`, `pharmacy-department`, `lab-services`

```
[Enter team name here]
```

---

## 2. Team Lead / Owner

**Who is the primary contact for this account?**

Example: `Dr. John Smith`

```
[Enter team lead name here]
```

---

## 3. Team Email

**What is your team's email address?**

Example: `radiology-team@hospital.com`

```
[Enter team email here]
```

---

## 4. Cost Center

**What is your cost center code?**

Format: `CC-DEPARTMENT-XXX`  
Example: `CC-RADIOLOGY-001`

```
[Enter cost center here]
```

---

## 5. Data Classification

**What type of data will you be working with?**

- [ ] **Public** - No sensitive data
- [ ] **Internal** - Internal hospital data
- [ ] **Confidential** - Patient data (PII)
- [ ] **Restricted** - Highly sensitive (PHI, genetic data)

---

## 6. Business Criticality

**How critical is this system to hospital operations?**

- [ ] **Low** - Non-critical, experimental
- [ ] **Medium** - Important but not patient-facing
- [ ] **High** - Patient-facing or critical operations
- [ ] **Critical** - Life-critical systems

---

## 7. Primary Use Case

**What will you be building?**

- [ ] EHR System (Electronic Health Records)
- [ ] Telemedicine Platform
- [ ] Medical Imaging / PACS
- [ ] Lab Information System
- [ ] Patient Portal
- [ ] Healthcare Analytics
- [ ] Medical Research
- [ ] Other (please specify below)

**If "Other", please describe:**

```
[Describe your use case here]
```

---

## 8. Estimated Monthly Budget

**What is your estimated monthly AWS spending?**

Range: $100 - $100,000  
Example: `$5,000`

```
$[Enter amount here]
```

---

## 9. Additional AWS Services (Optional)

**Do you need any of these services beyond the landing zone?**

- [ ] RDS (Relational Database)
- [ ] S3 (Object Storage)
- [ ] Lambda (Serverless Functions)
- [ ] DynamoDB (NoSQL Database)
- [ ] ElastiCache (In-Memory Cache)
- [ ] SQS (Message Queue)
- [ ] SNS (Notifications)
- [ ] CloudFront (CDN)
- [ ] Kinesis (Streaming Data)
- [ ] SageMaker (Machine Learning)
- [ ] Other (please specify below)

**If "Other", please describe:**

```
[Describe additional services here]
```

---

## 10. Compliance Requirements

**What compliance standards apply to your workload?**

- [ ] HIPAA (Health Insurance Portability and Accountability Act)
- [ ] HITECH (Health Information Technology for Economic and Clinical Health)
- [ ] SOC 2 (Service Organization Control)
- [ ] PCI DSS (Payment Card Industry Data Security Standard)
- [ ] GDPR (General Data Protection Regulation)
- [ ] None / Not applicable

---

## Checklist

Before submitting, please confirm:

- [ ] All required fields are filled out
- [ ] Team email is a hospital domain (@hospital.com)
- [ ] Cost center follows format: CC-DEPARTMENT-XXX
- [ ] Budget is between $100-$100,000
- [ ] At least one compliance requirement is selected
- [ ] I have read the [Intake Form Documentation](../../ACCOUNT_FACTORY_INTAKE_FORM.md)

---

## Additional Information (Optional)

**Is there anything else we should know about your request?**

```
[Add any additional context here]
```

---

## What Happens Next

1. ✅ Your request will be validated automatically
2. ✅ If valid, AWS account provisioning will begin
3. ✅ 3 environments (dev/staging/prod) will be created
4. ✅ Landing zone will be deployed to each environment
5. ✅ You'll receive account credentials via email
6. ✅ You can start deploying applications immediately

**Typical timeline:** 5-10 minutes from submission to account ready

---

## Support

- 📖 [Account Factory Documentation](../../ACCOUNT_FACTORY_IMPLEMENTATION.md)
- 📋 [Intake Form Details](../../ACCOUNT_FACTORY_INTAKE_FORM.md)
- 🏥 [Hospital Landing Zone](../../README.md)
- 💬 Questions? Contact: cloud-team@hospital.com

---

**Thank you for using the AWS Hospital Account Factory!**
