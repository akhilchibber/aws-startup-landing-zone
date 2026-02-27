"""
Monitoring stack for CloudWatch dashboards and alarms.
"""
from aws_cdk import (
    Stack,
    Duration,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb
)
from constructs import Construct


class MonitoringStack(Stack):
    """Stack for CloudWatch monitoring."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        lambda_function: lambda_.Function,
        api: apigateway.RestApi,
        table: dynamodb.Table,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # SNS topic for alarms
        alarm_topic = sns.Topic(
            self, "AlarmTopic",
            display_name="Bedrock Intake Alarms"
        )

        # CloudWatch Dashboard
        dashboard = cloudwatch.Dashboard(
            self, "Dashboard",
            dashboard_name="bedrock-intake-dashboard"
        )

        # Conversation metrics
        conversations_started = cloudwatch.Metric(
            namespace="BedrockConversationalIntake",
            metric_name="ConversationStarted",
            statistic="Sum",
            period=Duration.minutes(5)
        )

        conversations_completed = cloudwatch.Metric(
            namespace="BedrockConversationalIntake",
            metric_name="ConversationCompleted",
            statistic="Sum",
            period=Duration.minutes(5)
        )

        conversations_abandoned = cloudwatch.Metric(
            namespace="BedrockConversationalIntake",
            metric_name="ConversationAbandoned",
            statistic="Sum",
            period=Duration.minutes(5)
        )

        # Add widgets to dashboard
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Conversation Flow",
                left=[conversations_started, conversations_completed, conversations_abandoned],
                width=12
            )
        )

        # Lambda metrics
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Lambda Performance",
                left=[
                    lambda_function.metric_invocations(),
                    lambda_function.metric_errors(),
                    lambda_function.metric_throttles()
                ],
                width=12
            ),
            cloudwatch.GraphWidget(
                title="Lambda Duration",
                left=[lambda_function.metric_duration()],
                width=12
            )
        )

        # API Gateway metrics
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="API Gateway",
                left=[
                    api.metric_count(),
                    api.metric_client_error(),
                    api.metric_server_error()
                ],
                width=12
            ),
            cloudwatch.GraphWidget(
                title="API Latency",
                left=[api.metric_latency()],
                width=12
            )
        )

        # Alarms
        # High error rate alarm
        lambda_function.metric_errors(
            statistic="Sum",
            period=Duration.minutes(5)
        ).create_alarm(
            self, "HighErrorRate",
            alarm_name="bedrock-intake-high-error-rate",
            threshold=10,
            evaluation_periods=2,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD
        ).add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # High abandonment rate alarm
        cloudwatch.Alarm(
            self, "HighAbandonmentRate",
            alarm_name="bedrock-intake-high-abandonment",
            metric=conversations_abandoned,
            threshold=5,
            evaluation_periods=2,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD
        ).add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # API latency alarm
        api.metric_latency(
            statistic="Average",
            period=Duration.minutes(5)
        ).create_alarm(
            self, "HighLatency",
            alarm_name="bedrock-intake-high-latency",
            threshold=3000,  # 3 seconds
            evaluation_periods=2,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD
        ).add_alarm_action(cw_actions.SnsAction(alarm_topic))
