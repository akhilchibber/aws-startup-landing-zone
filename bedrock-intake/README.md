# Bedrock Conversational Intake for AWS Account Factory

A conversational AI application built with Amazon Bedrock Flow that guides users through the AWS Account Factory intake process using natural language.

## Overview

This application provides a chatbot interface for creating AWS account requests. Instead of manually filling out a GitHub Issue form, users can have a natural conversation where the bot:

- Asks the 10 intake questions conversationally
- Validates responses in real-time
- Auto-corrects common formatting issues
- Creates GitHub Issues that trigger the existing Account Factory workflow

**Zero changes to existing Account Factory infrastructure or GitHub Actions workflow.**

## Architecture

The system consists of:

- **Lambda Function**: Handles conversation logic, validation, and GitHub integration
- **API Gateway**: REST API for conversation endpoints
- **DynamoDB**: Session state storage with 24-hour TTL
- **Secrets Manager**: Secure GitHub token storage
- **CloudWatch**: Logging, metrics, and alarms
- **Bedrock Flow**: Conversational AI interface (optional enhancement)

## Prerequisites

- AWS Account with appropriate permissions
- Python 3.11+
- AWS CDK CLI installed
- GitHub personal access token with repo permissions

## Deployment

### 1. Install Dependencies

```bash
cd bedrock-intake
pip install -r requirements.txt
cd infrastructure
pip install -r requirements.txt
```

### 2. Configure GitHub Token

Store your GitHub personal access token in AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name bedrock-intake/github-token \
  --secret-string "your-github-token-here"
```

### 3. Deploy Infrastructure

```bash
cd infrastructure
cdk bootstrap  # First time only
cdk deploy --all
```

### 4. Update Environment Variables

After deployment, update the Lambda function environment variables:
- `GITHUB_REPO_NAME`: Your repository (e.g., "your-org/hospital-landing-zone")
- `BEDROCK_FLOW_ID`: Your Bedrock Flow ID (if using Bedrock Flow)

## API Endpoints

### Start Conversation
```
POST /conversation/start
Body: { "user_id": "user@example.com" }
Response: { "session_id": "...", "message": "...", "question_id": "q1" }
```

### Send Message
```
POST /conversation/message
Body: { "session_id": "...", "message": "radiology-team" }
Response: { "message": "...", "question_id": "q2", "progress": "1/10" }
```

### Get Status
```
GET /conversation/status?session_id=...
Response: { "current_question": 3, "total_questions": 10, "is_complete": false }
```

### Resume Conversation
```
POST /conversation/resume
Body: { "session_id": "..." }
Response: { "message": "Welcome back! ...", "question_id": "q3" }
```

### End Conversation
```
DELETE /conversation/end
Body: { "session_id": "..." }
Response: { "message": "Conversation ended successfully" }
```

## Intake Questions

The chatbot asks these 10 questions:

1. **Team Name**: lowercase, hyphens only, 3-30 characters
2. **Team Lead**: full name
3. **Email**: valid email address
4. **Cost Center**: format CC-DEPT-XXXX
5. **Data Classification**: public, internal, confidential, restricted
6. **Business Criticality**: low, medium, high, critical
7. **Use Case**: predefined or custom description
8. **Monthly Budget**: $100-$100,000
9. **AWS Services**: optional, comma-separated
10. **Compliance**: optional, hipaa, pci-dss, sox, none

## Auto-Correction Features

The system automatically corrects common formatting issues:

- **Team Name**: "Radiology-Team" → "radiology-team"
- **Email**: "USER@EXAMPLE.COM" → "user@example.com"
- **Cost Center**: "cc-rad-1234" → "CC-RAD-1234"
- **Budget**: "5k" → "5000", "$10,000" → "10000"
- **AWS Services**: "ec2, s3" → "EC2, S3"
- **Compliance**: "HIPAA" → "hipaa"

All corrections are shown to the user for confirmation.

## Monitoring

CloudWatch Dashboard includes:
- Conversation flow metrics (started, completed, abandoned)
- Validation failure rates by field
- GitHub integration success/failure
- API latency and error rates
- Lambda performance metrics

Alarms are configured for:
- High error rate (>10 errors in 5 minutes)
- High abandonment rate (>5 abandonments in 5 minutes)
- High API latency (>3 seconds average)

## Testing

Run unit tests:
```bash
pytest tests/
```

Run integration tests:
```bash
pytest tests/integration/
```

## Troubleshooting

### Session Not Found
- Sessions expire after 30 minutes of inactivity
- Sessions are deleted after 24 hours (TTL)
- Use the resume endpoint to continue

### GitHub Issue Creation Failed
- Check GitHub token permissions (needs repo access)
- Verify repository name in environment variables
- Check CloudWatch logs for detailed error messages

### Validation Failures
- Maximum 3 attempts per question
- Use the help command to see examples
- Check auto-correction suggestions

## Security

- GitHub tokens stored in Secrets Manager
- Email addresses redacted in logs
- IAM roles follow least privilege principle
- API Gateway throttling enabled (100 req/sec per user)
- DynamoDB encryption at rest (AWS managed)

## Cost Estimate

Monthly costs (assuming 100 conversations/day):
- Lambda: ~$5
- API Gateway: ~$3
- DynamoDB: ~$2
- CloudWatch: ~$5
- Secrets Manager: ~$1
- **Total: ~$16/month**

## Support

For issues or questions:
1. Check CloudWatch logs for error details
2. Review the monitoring dashboard
3. Consult the Account Factory documentation
4. Contact your AWS administrator
