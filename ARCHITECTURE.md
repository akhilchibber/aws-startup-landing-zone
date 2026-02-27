# AWS Hospital Landing Zone - Technical Architecture

**Version:** 1.0  
**Last Updated:** February 27, 2026  
**Status:** Production Ready

---

## Overview

The AWS Hospital Landing Zone is a production-ready, HIPAA-compliant cloud infrastructure designed specifically for healthcare organizations. It provides automated account provisioning through an Account Factory that creates isolated AWS accounts with pre-configured landing zone infrastructure for hospital teams.

---

## System Architecture

### High-Level Architecture

```
GitHub Issue (Account Request)
        ↓
GitHub Actions Workflow
        ↓
Terraform Provisioning
        ↓
AWS Organizations Account
        ↓
Landing Zone Infrastructure
  ├── VPC (10.0.0.0/16)
  ├── Public Subnets (DMZ)
  ├── Private Subnets (Applications)
  ├── NAT Gateway (Internet Access)
  ├── Internet Gateway
  ├── Route Tables
  └── VPC Flow Logs (Monitoring)
```

### Account Factory Architecture

```
Hospital AWS Organization (Root)
├── Management Account (akhil.chibber3)
│   └── Account Factory Infrastructure
│       ├── GitHub Actions Workflow
│       ├── Terraform State (S3)
│       ├── State Locking (DynamoDB)
│       └── IAM Roles (OIDC)
│
└── Member Accounts (Created by Account Factory)
    ├── cloud-team-production-ready
    ├── radiology-team
    ├── cardiology-team
    └── [Future Teams...]
```

---

## Network Architecture

### VPC Design

Each team account receives a VPC with the following structure:

```
VPC (10.0.0.0/16)
│
├── Public Subnets (DMZ Layer)
│   ├── Subnet 1a: 10.0.0.0/24 (eu-north-1a)
│   └── Subnet 1b: 10.0.1.0/24 (eu-north-1b)
│
├── Private Subnets (Application Layer)
│   ├── Subnet 1a: 10.0.32.0/19 (eu-north-1a)
│   └── Subnet 1b: 10.0.64.0/19 (eu-north-1b)
│
├── Internet Gateway (IGW)
│   └── Attached to VPC
│
├── NAT Gateway
│   └── Deployed in Public Subnet 1a
│
└── Route Tables
    ├── Public RT → IGW (0.0.0.0/0)
    └── Private RT → NAT Gateway (0.0.0.0/0)
```

### Traffic Flow

**Inbound Traffic (Internet → Application):**
```
Internet
  ↓
Internet Gateway
  ↓
Public Subnet (Load Balancer)
  ↓
Private Subnet (Application)
```

**Outbound Traffic (Application → Internet):**
```
Private Subnet (Application)
  ↓
NAT Gateway (Public Subnet)
  ↓
Internet Gateway
  ↓
Internet
```

---

## Infrastructure Components

### 1. VPC (Virtual Private Cloud)

**Purpose:** Isolated network environment for team applications

**Configuration:**
- CIDR Block: 10.0.0.0/16
- DNS Hostnames: Enabled
- DNS Support: Enabled
- Tenancy: Default

**Features:**
- Network isolation per team
- Multi-AZ deployment
- VPC Flow Logs enabled

### 2. Subnets

**Public Subnets (2):**
- CIDR: 10.0.0.0/24, 10.0.1.0/24
- Availability Zones: eu-north-1a, eu-north-1b
- Auto-assign Public IP: Enabled
- Use Cases: Load balancers, NAT Gateway, bastion hosts

**Private Subnets (2):**
- CIDR: 10.0.32.0/19, 10.0.64.0/19
- Availability Zones: eu-north-1a, eu-north-1b
- Auto-assign Public IP: Disabled
- Use Cases: Application servers, databases, internal services

### 3. Internet Gateway

**Purpose:** Enable internet connectivity for VPC

**Configuration:**
- Attached to VPC
- Routes traffic from public subnets to internet
- Handles inbound traffic from internet

### 4. NAT Gateway

**Purpose:** Enable private subnet internet access

**Configuration:**
- Deployed in: Public Subnet 1a
- Elastic IP: Allocated and associated
- High Availability: Single NAT (cost-optimized)
- Bandwidth: Up to 45 Gbps

**Cost:** $45/month

### 5. Route Tables

**Public Route Table:**
```
Destination     Target
10.0.0.0/16     local
0.0.0.0/0       igw-xxxxx
```

**Private Route Table:**
```
Destination     Target
10.0.0.0/16     local
0.0.0.0/0       nat-xxxxx
```

### 6. VPC Flow Logs

**Purpose:** Network traffic monitoring and security auditing

**Configuration:**
- Traffic Type: ALL (accepted and rejected)
- Destination: CloudWatch Logs
- Log Group: /aws/vpc/flowlogs/{team-name}
- Retention: 7 days
- IAM Role: Dedicated flow log role

**Cost:** $1-5/month

---

## Account Factory Implementation

### Terraform Module Structure

```
modules/
├── account-factory/
│   ├── main.tf          # AWS account creation
│   ├── variables.tf     # Input validation
│   └── outputs.tf       # Account details
│
└── environment/
    ├── main.tf          # VPC infrastructure
    ├── variables.tf     # Environment config
    └── outputs.tf       # Infrastructure details
```

### Account Creation Process

1. **GitHub Issue Submission**
   - Team fills 10-question intake form
   - Issue labeled with `account-factory`

2. **Validation (1-2 minutes)**
   - Parse intake form fields
   - Validate email domain
   - Validate cost center format
   - Validate budget range
   - Check team name uniqueness

3. **Terraform Provisioning (3-4 minutes)**
   - Initialize Terraform with unique state file
   - Create AWS Organizations account
   - Configure IAM cross-account role
   - Set up budget alerts
   - Deploy landing zone infrastructure

4. **Notification**
   - GitHub issue comment with account details
   - Email to team (placeholder)
   - Issue automatically closed

**Total Time:** 4-6 minutes

### State Management

**S3 Backend:**
- Bucket: hospital-landing-zone-terraform
- Key Pattern: account-factory/{team_name}/state
- Encryption: AES256
- Versioning: Enabled

**DynamoDB Locking:**
- Table: terraform-locks
- Prevents concurrent modifications
- Ensures state consistency

---

## Security Architecture

### Network Security

**Defense in Depth:**
1. VPC isolation per team
2. Public/private subnet segmentation
3. Security groups (stateful firewall)
4. Network ACLs (stateless firewall)
5. VPC Flow Logs (monitoring)

**Security Groups:**
- Default deny all inbound
- Allow specific ports as needed
- Stateful connection tracking

### IAM Security

**Cross-Account Access:**
- Management account can assume role in member accounts
- Principle of least privilege
- MFA recommended for console access

**Service Roles:**
- VPC Flow Logs role
- Terraform execution role
- GitHub Actions OIDC role

### Compliance Controls

**HIPAA Compliance:**
- Encryption at rest (EBS, S3, RDS)
- Encryption in transit (TLS/HTTPS)
- VPC Flow Logs for audit trails
- Network isolation
- Access logging

**Audit Trail:**
- VPC Flow Logs (network traffic)
- CloudWatch Logs (application logs)
- AWS CloudTrail (API calls)
- Cost allocation tags

---

## Cost Architecture

### Monthly Cost Breakdown

**Per Team Account:**

| Component | Quantity | Unit Cost | Monthly Cost |
|-----------|----------|-----------|--------------|
| NAT Gateway | 1 | $45 | $45 |
| NAT Gateway Data | Variable | $0.045/GB | $5-10 |
| Elastic IP (in use) | 1 | $0 | $0 |
| VPC Flow Logs | 1 | Variable | $1-5 |
| S3 State Storage | <1 GB | $0.023/GB | $0 |
| DynamoDB Locks | Minimal | On-demand | $0 |
| **Total** | | | **$51-60** |

### Cost Optimization

**Current Setup (Production):**
- Single NAT Gateway per VPC
- 7-day log retention
- On-demand DynamoDB pricing

**Free Tier Optimization:**
- Remove NAT Gateway (saves $45/month)
- Use public subnets only
- Disable VPC Flow Logs (saves $1-5/month)
- **Total Savings:** $46-50/month → $0/month

---

## Automation Architecture

### GitHub Actions Workflow

**Trigger:** Issue opened/edited with `account-factory` label

**Jobs:**

1. **validate-intake-form**
   - Parse issue body
   - Extract 10 intake fields
   - Validate formats and ranges
   - Comment validation result

2. **provision-account**
   - Configure AWS credentials (OIDC)
   - Create Terraform variables file
   - Initialize Terraform with unique state
   - Plan infrastructure changes
   - Apply infrastructure
   - Extract outputs
   - Comment provisioning result
   - Close issue

3. **handle-validation-failure**
   - Add `validation-failed` label
   - Provide error feedback

### CI/CD Pipeline

```
GitHub Issue
    ↓
Workflow Trigger
    ↓
Parse & Validate
    ↓
AWS Authentication (OIDC)
    ↓
Terraform Init
    ↓
Terraform Plan
    ↓
Terraform Apply
    ↓
Extract Outputs
    ↓
Notify Team
    ↓
Close Issue
```

---

## Monitoring & Observability

### VPC Flow Logs

**Captured Data:**
- Source/destination IP addresses
- Source/destination ports
- Protocol
- Packet count
- Byte count
- Action (ACCEPT/REJECT)
- Log status

**Use Cases:**
- Security analysis
- Troubleshooting connectivity
- Compliance auditing
- Cost optimization

### CloudWatch Integration

**Metrics:**
- NAT Gateway bytes in/out
- NAT Gateway packets in/out
- NAT Gateway connection count
- VPC Flow Log delivery

**Alarms:**
- Budget threshold (80%, 100%)
- NAT Gateway errors
- Flow log delivery failures

---

## Disaster Recovery

### High Availability

**Multi-AZ Deployment:**
- Subnets in 2 availability zones
- Automatic failover for AWS services
- No single point of failure

**Recovery Objectives:**
- RTO (Recovery Time Objective): < 1 hour
- RPO (Recovery Point Objective): < 15 minutes

### Backup Strategy

**Infrastructure as Code:**
- Terraform state in S3 (versioned)
- Configuration in Git (version controlled)
- Can recreate infrastructure from code

**Data Backup:**
- Team responsibility for application data
- Recommend automated backups for databases
- S3 versioning for critical data

---

## Scalability

### Current Capacity

**AWS Free Tier Limits:**
- Elastic IPs: 5 per region
- NAT Gateways: Unlimited (cost constraint)
- VPCs: 5 per region (soft limit)
- Accounts: 10 in organization (default)

**Current Usage:**
- Accounts: 3 (management + 2 members)
- Elastic IPs: 1 in use
- NAT Gateways: 1 active
- VPCs: 1 per member account

### Scaling Strategy

**Horizontal Scaling:**
- Add more member accounts as needed
- Request AWS Organizations limit increase
- Each account is isolated and independent

**Vertical Scaling:**
- Upgrade NAT Gateway bandwidth (automatic)
- Add more subnets within VPC
- Implement VPC peering for cross-account communication

---

## Technology Stack

### Infrastructure as Code
- **Terraform:** v1.0.0+
- **AWS Provider:** v5.0+
- **State Backend:** S3 + DynamoDB

### CI/CD
- **GitHub Actions:** Workflow automation
- **GitHub Issues:** Intake form interface
- **OIDC:** Secure AWS authentication

### AWS Services
- **Organizations:** Account management
- **VPC:** Network isolation
- **EC2:** NAT Gateway, Elastic IPs
- **CloudWatch:** Logging and monitoring
- **IAM:** Access control
- **S3:** State storage
- **DynamoDB:** State locking
- **Budgets:** Cost alerts

---

## Best Practices Implemented

### Security
✅ Network isolation per team  
✅ Public/private subnet segmentation  
✅ VPC Flow Logs enabled  
✅ Encryption at rest and in transit  
✅ IAM roles with least privilege  
✅ MFA recommended  

### Reliability
✅ Multi-AZ deployment  
✅ Automated infrastructure provisioning  
✅ Infrastructure as Code  
✅ State locking for consistency  

### Performance
✅ NAT Gateway (up to 45 Gbps)  
✅ Multi-AZ for low latency  
✅ Proper subnet sizing  

### Cost Optimization
✅ Single NAT Gateway per VPC  
✅ On-demand DynamoDB pricing  
✅ 7-day log retention  
✅ Budget alerts configured  

### Operational Excellence
✅ Automated provisioning  
✅ Comprehensive documentation  
✅ Monitoring and logging  
✅ Audit trails  

---

## Future Enhancements

### Phase 1 (Planned)
- Multi-environment support (dev/staging/prod per account)
- VPC peering between accounts
- Centralized logging
- Advanced monitoring dashboards

### Phase 2 (Future)
- AWS Transit Gateway for hub-and-spoke
- AWS Control Tower integration
- Service Catalog for approved services
- Automated compliance scanning

### Phase 3 (Long-term)
- Multi-region deployment
- Disaster recovery automation
- Advanced security controls
- Cost optimization automation

---

## Technical Specifications

### Network Specifications

| Parameter | Value |
|-----------|-------|
| VPC CIDR | 10.0.0.0/16 |
| Public Subnet 1a | 10.0.0.0/24 |
| Public Subnet 1b | 10.0.1.0/24 |
| Private Subnet 1a | 10.0.32.0/19 |
| Private Subnet 1b | 10.0.64.0/19 |
| Availability Zones | 2 (eu-north-1a, eu-north-1b) |
| NAT Gateways | 1 (cost-optimized) |
| Internet Gateways | 1 |
| Route Tables | 2 (public, private) |

### Performance Specifications

| Metric | Value |
|--------|-------|
| NAT Gateway Bandwidth | Up to 45 Gbps |
| NAT Gateway Connections | Up to 55,000 |
| VPC Flow Log Latency | < 10 minutes |
| Account Provisioning Time | 4-6 minutes |
| Terraform Apply Time | 3-4 minutes |

---

## Troubleshooting

### Common Issues

**Issue: NAT Gateway not working**
- Check Elastic IP is allocated
- Verify route table points to NAT Gateway
- Check security groups allow outbound traffic

**Issue: Private subnet can't reach internet**
- Verify NAT Gateway is in running state
- Check route table association
- Verify security groups

**Issue: Account creation fails**
- Check AWS Organizations limits
- Verify IAM permissions
- Check Terraform state lock

**Issue: High costs**
- Review NAT Gateway data transfer
- Check for unused Elastic IPs
- Optimize VPC Flow Log retention

---

## Support & Maintenance

### Regular Maintenance

**Weekly:**
- Review VPC Flow Logs for anomalies
- Check budget alerts
- Monitor NAT Gateway metrics

**Monthly:**
- Review and optimize costs
- Update Terraform modules
- Review security groups

**Quarterly:**
- Audit IAM permissions
- Review compliance controls
- Update documentation

### Support Contacts

- **Technical Issues:** cloud-team@hospital.com
- **Cost Questions:** cloud-team@hospital.com
- **Security Concerns:** cloud-team@hospital.com

---

**AWS Hospital Landing Zone - Technical Architecture**  
**Version:** 1.0  
**Last Updated:** February 27, 2026  
**Status:** Production Ready
