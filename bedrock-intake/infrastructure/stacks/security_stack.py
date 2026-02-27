"""
Security stack for secrets and IAM roles.
"""
from aws_cdk import (
    Stack,
    aws_secretsmanager as secretsmanager,
    aws_iam as iam
)
from constructs import Construct


class SecurityStack(Stack):
    """Stack for secrets and IAM roles."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # GitHub token secret
        self.github_secret = secretsmanager.Secret(
            self, "GitHubToken",
            secret_name="bedrock-intake/github-token",
            description="GitHub personal access token for creating issues"
        )

        # Lambda execution role
        self.lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ]
        )

        # Grant permissions
        self.github_secret.grant_read(self.lambda_role)
        
        # CloudWatch Logs and Metrics permissions
        self.lambda_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "cloudwatch:PutMetricData"
            ],
            resources=["*"]
        ))
        
        # Bedrock permissions
        self.lambda_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "bedrock:InvokeFlow"
            ],
            resources=["*"]
        ))
