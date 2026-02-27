"""
Structured logging and monitoring for Bedrock Conversational Intake.
"""
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional
import boto3


class Logger:
    """Structured logger with CloudWatch integration."""

    def __init__(self):
        """Initialize logger."""
        self.cloudwatch = boto3.client('cloudwatch')
        self.namespace = 'BedrockConversationalIntake'

    def log_event(self, event_type: str, data: Dict[str, Any], session_id: Optional[str] = None):
        """Log structured event to CloudWatch Logs."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'session_id': session_id,
            'data': self.redact_sensitive_data(data)
        }
        
        print(json.dumps(log_entry))

    def redact_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Redact sensitive information from log data."""
        redacted = data.copy()
        
        # Redact email addresses
        if 'email' in redacted:
            email = redacted['email']
            if '@' in email:
                parts = email.split('@')
                redacted['email'] = f"{parts[0][:2]}***@{parts[1]}"
        
        # Redact GitHub tokens
        if 'token' in redacted:
            redacted['token'] = '***REDACTED***'
        
        # Redact any field containing 'password' or 'secret'
        for key in list(redacted.keys()):
            if 'password' in key.lower() or 'secret' in key.lower():
                redacted[key] = '***REDACTED***'
        
        return redacted

    def log_conversation_started(self, session_id: str, user_id: str):
        """Log conversation start event."""
        self.log_event('conversation_started', {
            'user_id': user_id
        }, session_id)
        
        self.publish_metric('ConversationStarted', 1)

    def log_conversation_completed(self, session_id: str, duration_seconds: float, github_issue: int):
        """Log conversation completion event."""
        self.log_event('conversation_completed', {
            'duration_seconds': duration_seconds,
            'github_issue': github_issue
        }, session_id)
        
        self.publish_metric('ConversationCompleted', 1)
        self.publish_metric('ConversationDuration', duration_seconds, unit='Seconds')

    def log_conversation_abandoned(self, session_id: str, current_question: int):
        """Log conversation abandonment event."""
        self.log_event('conversation_abandoned', {
            'current_question': current_question,
            'total_questions': 10
        }, session_id)
        
        self.publish_metric('ConversationAbandoned', 1)

    def log_validation_failure(self, session_id: str, field_name: str, error_message: str, attempt: int):
        """Log validation failure event."""
        self.log_event('validation_failure', {
            'field_name': field_name,
            'error_message': error_message,
            'attempt': attempt
        }, session_id)
        
        self.publish_metric('ValidationFailure', 1, dimensions={'FieldName': field_name})

    def log_auto_correction(self, session_id: str, field_name: str, corrections: list):
        """Log auto-correction event."""
        self.log_event('auto_correction_applied', {
            'field_name': field_name,
            'corrections': corrections
        }, session_id)
        
        self.publish_metric('AutoCorrectionApplied', 1, dimensions={'FieldName': field_name})

    def log_github_issue_created(self, session_id: str, issue_number: int, team_name: str):
        """Log GitHub Issue creation event."""
        self.log_event('github_issue_created', {
            'issue_number': issue_number,
            'team_name': team_name
        }, session_id)
        
        self.publish_metric('GitHubIssueCreated', 1, dimensions={'Status': 'Success'})

    def log_github_issue_failed(self, session_id: str, error: str):
        """Log GitHub Issue creation failure."""
        self.log_event('github_issue_failed', {
            'error': error
        }, session_id)
        
        self.publish_metric('GitHubIssueCreated', 1, dimensions={'Status': 'Failure'})

    def log_response_time(self, endpoint: str, duration_ms: float):
        """Log API response time."""
        self.publish_metric('ResponseTime', duration_ms, unit='Milliseconds', 
                          dimensions={'Endpoint': endpoint})

    def publish_metric(self, metric_name: str, value: float, unit: str = 'Count', 
                      dimensions: Optional[Dict[str, str]] = None):
        """Publish metric to CloudWatch."""
        try:
            metric_data = {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.utcnow()
            }
            
            if dimensions:
                metric_data['Dimensions'] = [
                    {'Name': k, 'Value': v} for k, v in dimensions.items()
                ]
            
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[metric_data]
            )
        except Exception as e:
            print(f"Error publishing metric {metric_name}: {e}")


# Global logger instance
logger = Logger()
