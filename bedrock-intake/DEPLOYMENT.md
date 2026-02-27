# Deployment Guide: Bedrock Conversational Intake

This guide walks through deploying the Bedrock Conversational Intake system to AWS.

## Prerequisites

1. **AWS Account** with administrator access
2. **AWS CLI** configured with credentials
3. **Python 3.11+** installed
4. **Node.js 18+** (for AWS CDK)
5. **AWS CDK CLI** installed: `npm install -g aws-cdk`
6. **GitHub Personal Access Token** with `repo` permissions

## Step 1: Prepare GitHub Token

Create a GitHub personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name: "Bedrock Intake Bot"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)

Store the token in AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name bedrock-intake/github-token \
  --description "GitHub token for Bedrock Intake bot" \
  --secret-string "ghp_your_token_here" \
  --region us-east-1
```

## Step 2: Clone and Setup

```bash
# Navigate to your hospital landing zone repository
cd hospital-landing-zone

# Install Python dependencies
cd bedrock-intake
pip install -r requirements.txt

# Install CDK dependencies
cd infrastructure
pip install -r requirements.txt
```

## Step 3: Configure Environment

Edit `infrastructure/app.py` and update:

```python
# Line 24: Update repository name
"GITHUB_REPO_NAME": "your-org/hospital-landing-zone",
```

Create a CDK context file for your environment:

```bash
cat > infrastructure/cdk.context.json << EOF
{
  "account": "123456789012",
  "region": "us-east-1",
  "environment": "prod"
}
EOF
```

## Step 4: Bootstrap CDK (First Time Only)

If this is your first CDK deployment in this account/region:

```bash
cd infrastructure
cdk bootstrap aws://123456789012/us-east-1
```

## Step 5: Deploy Infrastructure

Deploy all stacks:

```bash
cd infrastructure
cdk deploy --all --require-approval never
```

This will deploy:
- **bedrock-intake-data-prod**: DynamoDB table
- **bedrock-intake-security-prod**: Secrets and IAM roles
- **bedrock-intake-api-prod**: Lambda and API Gateway
- **bedrock-intake-monitoring-prod**: CloudWatch dashboards and alarms

Deployment takes approximately 5-10 minutes.

## Step 6: Verify Deployment

After deployment, CDK will output the API Gateway URL:

```
Outputs:
bedrock-intake-api-prod.ConversationApiEndpoint = https://abc123.execute-api.us-east-1.amazonaws.com/prod/
```

Test the API:

```bash
# Start a conversation
curl -X POST https://your-api-url/conversation/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test@example.com"}'

# You should receive a response with session_id and first question
```

## Step 7: Configure CloudWatch Alarms

Subscribe to alarm notifications:

```bash
# Get the SNS topic ARN from CloudWatch console
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:bedrock-intake-monitoring-prod-AlarmTopic \
  --protocol email \
  --notification-endpoint your-email@example.com

# Confirm the subscription via email
```

## Step 8: Test End-to-End

Run a complete conversation test:

```bash
# Use the test script
python tests/integration/test_conversation_flow.py
```

Or test manually:

1. Start conversation
2. Answer all 10 questions
3. Verify GitHub Issue is created
4. Verify Account Factory workflow triggers
5. Check CloudWatch logs and metrics

## Step 9: Production Checklist

Before going to production:

- [ ] GitHub token has correct permissions
- [ ] Repository name is correct in Lambda environment
- [ ] CloudWatch alarms are configured and tested
- [ ] SNS email subscriptions are confirmed
- [ ] DynamoDB table has point-in-time recovery enabled
- [ ] Lambda function has appropriate memory/timeout settings
- [ ] API Gateway throttling limits are appropriate
- [ ] End-to-end test completed successfully
- [ ] Documentation is updated with API endpoint URL
- [ ] Team is trained on using the chatbot

## Updating the Application

To deploy updates:

```bash
cd infrastructure
cdk deploy --all
```

CDK will show a diff of changes before deploying.

## Rollback

To rollback to a previous version:

```bash
# Delete the current stacks
cdk destroy --all

# Checkout previous version
git checkout <previous-commit>

# Redeploy
cdk deploy --all
```

## Monitoring

Access the CloudWatch dashboard:

1. Go to AWS Console → CloudWatch → Dashboards
2. Open "bedrock-intake-dashboard"
3. Monitor conversation metrics, errors, and performance

## Troubleshooting

### Deployment Fails

**Error: "Secret not found"**
- Ensure GitHub token is stored in Secrets Manager
- Verify secret name matches: `bedrock-intake/github-token`

**Error: "Insufficient permissions"**
- Ensure AWS credentials have administrator access
- Check IAM policies for CDK deployment

### Lambda Errors

**Error: "Unable to import module 'lambda_handler'"**
- Verify Lambda code is packaged correctly
- Check Python dependencies in requirements.txt

**Error: "GitHub authentication failed"**
- Verify GitHub token is valid
- Check token has `repo` permissions
- Ensure token is not expired

### API Gateway Errors

**Error: 404 Not Found**
- Verify API endpoint URL is correct
- Check API Gateway deployment stage

**Error: 429 Too Many Requests**
- API throttling limit reached
- Increase throttling limits in api_stack.py

## Cost Optimization

To reduce costs:

1. **Use DynamoDB on-demand billing** (already configured)
2. **Set Lambda reserved concurrency** to limit max concurrent executions
3. **Enable API Gateway caching** for status endpoint
4. **Reduce CloudWatch log retention** from default (never expire) to 30 days
5. **Delete old DynamoDB items** using TTL (already configured)

## Security Best Practices

1. **Rotate GitHub token** every 90 days
2. **Enable AWS CloudTrail** for audit logging
3. **Use AWS WAF** with API Gateway for additional protection
4. **Enable VPC endpoints** for DynamoDB and Secrets Manager
5. **Implement API authentication** using Cognito or IAM

## Support

For deployment issues:
- Check CloudWatch Logs: `/aws/lambda/bedrock-intake-handler`
- Review CDK deployment logs
- Consult AWS documentation
- Contact AWS Support
