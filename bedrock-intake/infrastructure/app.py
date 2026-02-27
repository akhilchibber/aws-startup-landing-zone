#!/usr/bin/env python3
"""
CDK app entry point for Bedrock Conversational Intake.
"""
import aws_cdk as cdk
from stacks.data_stack import DataStack
from stacks.security_stack import SecurityStack
from stacks.api_stack import ApiStack
from stacks.monitoring_stack import MonitoringStack


app = cdk.App()

# Environment configuration
env = cdk.Environment(
    account=app.node.try_get_context("account"),
    region=app.node.try_get_context("region") or "us-east-1"
)

# Stack naming
project_name = "bedrock-intake"
environment = app.node.try_get_context("environment") or "dev"

# Create stacks
data_stack = DataStack(
    app,
    f"{project_name}-data-{environment}",
    env=env,
    description="DynamoDB table for session state"
)

security_stack = SecurityStack(
    app,
    f"{project_name}-security-{environment}",
    env=env,
    description="Secrets and IAM roles"
)

api_stack = ApiStack(
    app,
    f"{project_name}-api-{environment}",
    table=data_stack.table,
    lambda_role=security_stack.lambda_role,
    github_secret=security_stack.github_secret,
    env=env,
    description="Lambda function and API Gateway"
)

monitoring_stack = MonitoringStack(
    app,
    f"{project_name}-monitoring-{environment}",
    lambda_function=api_stack.lambda_function,
    api=api_stack.api,
    table=data_stack.table,
    env=env,
    description="CloudWatch dashboards and alarms"
)

# Add dependencies
api_stack.add_dependency(data_stack)
api_stack.add_dependency(security_stack)
monitoring_stack.add_dependency(api_stack)

app.synth()
