"""
API stack for Lambda function and API Gateway.
"""
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager
)
from constructs import Construct


class ApiStack(Stack):
    """Stack for Lambda and API Gateway."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        table: dynamodb.Table,
        lambda_role: iam.Role,
        github_secret: secretsmanager.Secret,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda function
        self.lambda_function = lambda_.Function(
            self, "ConversationHandler",
            function_name="bedrock-intake-handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="lambda_handler.lambda_handler",
            code=lambda_.Code.from_asset("../src"),
            role=lambda_role,
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name,
                "GITHUB_SECRET_ARN": github_secret.secret_arn,
                "GITHUB_REPO_NAME": "your-org/hospital-landing-zone",
                "BEDROCK_FLOW_ID": "placeholder-flow-id"
            }
        )

        # Grant DynamoDB permissions
        table.grant_read_write_data(self.lambda_function)

        # API Gateway
        self.api = apigateway.RestApi(
            self, "ConversationApi",
            rest_api_name="bedrock-intake-api",
            description="API for Bedrock Conversational Intake",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "Authorization"]
            )
        )

        # Lambda integration
        lambda_integration = apigateway.LambdaIntegration(self.lambda_function)

        # API resources and methods
        conversation = self.api.root.add_resource("conversation")
        
        # POST /conversation/start
        start = conversation.add_resource("start")
        start.add_method("POST", lambda_integration)
        
        # POST /conversation/message
        message = conversation.add_resource("message")
        message.add_method("POST", lambda_integration)
        
        # GET /conversation/status
        status = conversation.add_resource("status")
        status.add_method("GET", lambda_integration)
        
        # POST /conversation/resume
        resume = conversation.add_resource("resume")
        resume.add_method("POST", lambda_integration)
        
        # DELETE /conversation/end
        end = conversation.add_resource("end")
        end.add_method("DELETE", lambda_integration)

        # Usage plan for throttling
        plan = self.api.add_usage_plan(
            "UsagePlan",
            throttle=apigateway.ThrottleSettings(
                rate_limit=100,
                burst_limit=200
            )
        )
