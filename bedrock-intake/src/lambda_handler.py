"""
Lambda handler for Bedrock Conversational Intake API.
"""
import json
import os
from typing import Dict, Any, Optional
from src.session_manager import SessionManager
from src.validation_engine import ValidationEngine
from src.auto_corrector import AutoCorrector
from src.github_client import GitHubIssueCreator
from config.questions import QUESTIONS


# Environment variables
TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')
SECRET_ARN = os.environ.get('GITHUB_SECRET_ARN')
REPO_NAME = os.environ.get('GITHUB_REPO_NAME')

# Initialize components
session_manager = SessionManager(TABLE_NAME)
validation_engine = ValidationEngine()
auto_corrector = AutoCorrector()
github_client = GitHubIssueCreator(SECRET_ARN, REPO_NAME)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main Lambda handler for API Gateway requests."""
    try:
        # Parse request
        http_method = event.get('httpMethod')
        path = event.get('path', '')
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        
        # Route to appropriate handler
        if path == '/conversation/start' and http_method == 'POST':
            return handle_start_conversation(body)
        elif path == '/conversation/message' and http_method == 'POST':
            return handle_message(body)
        elif path == '/conversation/status' and http_method == 'GET':
            return handle_status(event.get('queryStringParameters', {}))
        elif path == '/conversation/resume' and http_method == 'POST':
            return handle_resume(body)
        elif path == '/conversation/end' and http_method == 'DELETE':
            return handle_end_conversation(body)
        else:
            return create_response(404, {'error': 'Not found'})
    
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return create_response(500, {'error': 'Internal server error'})


def handle_start_conversation(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle POST /conversation/start - Start a new conversation."""
    user_id = body.get('user_id')
    
    if not user_id:
        return create_response(400, {'error': 'user_id is required'})
    
    # Create new session
    session = session_manager.create_session(user_id)
    
    # Get first question
    first_question = QUESTIONS[0]
    
    return create_response(200, {
        'session_id': session.session_id,
        'message': f"Welcome! Let's create your AWS account. {first_question.question_text}",
        'question_id': first_question.question_id,
        'help_text': first_question.help_text,
        'examples': first_question.examples
    })


def handle_message(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle POST /conversation/message - Process user message."""
    session_id = body.get('session_id')
    message = body.get('message', '').strip()
    
    if not session_id or not message:
        return create_response(400, {'error': 'session_id and message are required'})
    
    # Get session
    session = session_manager.get_session(session_id)
    if not session:
        return create_response(404, {'error': 'Session not found'})
    
    # Check timeout
    if session_manager.check_timeout(session):
        return create_response(408, {
            'error': 'Session timed out due to inactivity',
            'can_resume': True
        })
    
    # Handle special commands
    if message.lower() in ['exit', 'quit', 'cancel']:
        session_manager.delete_session(session_id)
        return create_response(200, {
            'message': 'Conversation ended. Your progress has been discarded.',
            'ended': True
        })
    
    if message.lower() in ['restart', 'start over']:
        session.current_question = 0
        session.answers = {}
        session.validation_attempts = {}
        session_manager.update_session(session)
        first_question = QUESTIONS[0]
        return create_response(200, {
            'message': f"Starting over. {first_question.question_text}",
            'question_id': first_question.question_id,
            'help_text': first_question.help_text
        })
    
    if message.lower() in ['help', '?']:
        current_question = QUESTIONS[session.current_question]
        return create_response(200, {
            'message': f"Help: {current_question.help_text}",
            'examples': current_question.examples,
            'question_id': current_question.question_id
        })
    
    # Process answer
    return process_answer(session, message)


def process_answer(session, message: str) -> Dict[str, Any]:
    """Process user's answer to current question."""
    current_question = QUESTIONS[session.current_question]
    field_name = current_question.field_name
    
    # Auto-correct the response
    correction = auto_corrector.correct_response(field_name, message)
    
    # If corrections were applied, ask for confirmation
    if correction.requires_confirmation and correction.corrections_applied:
        session.corrections_pending[field_name] = correction
        session_manager.update_session(session)
        
        return create_response(200, {
            'message': f"I noticed some formatting issues. I can auto-correct:\n"
                      f"Original: {correction.original_value}\n"
                      f"Corrected: {correction.corrected_value}\n"
                      f"Changes: {', '.join(correction.corrections_applied)}\n\n"
                      f"Accept this correction? (yes/no)",
            'requires_confirmation': True,
            'correction': {
                'original': correction.original_value,
                'corrected': correction.corrected_value,
                'changes': correction.corrections_applied
            }
        })
    
    # Use corrected value
    value_to_validate = correction.corrected_value
    
    # Validate the response
    validation = validation_engine.validate_response(field_name, value_to_validate)
    
    if not validation.is_valid:
        # Track validation attempts
        attempts = session.validation_attempts.get(field_name, 0) + 1
        session.validation_attempts[field_name] = attempts
        session_manager.update_session(session)
        
        if attempts >= 3:
            return create_response(200, {
                'message': f"You've reached the maximum validation attempts for this question. "
                          f"Error: {validation.error_message}\n\n"
                          f"Help: {current_question.help_text}\n"
                          f"Examples: {', '.join(current_question.examples)}\n\n"
                          f"Please try again.",
                'validation_error': validation.error_message,
                'help_text': current_question.help_text,
                'examples': current_question.examples
            })
        
        return create_response(200, {
            'message': f"Validation error: {validation.error_message}\n"
                      f"Attempt {attempts}/3. Please try again.",
            'validation_error': validation.error_message,
            'attempts_remaining': 3 - attempts
        })
    
    # Save answer and move to next question
    session.answers[field_name] = value_to_validate
    session.validation_attempts[field_name] = 0
    session.current_question += 1
    
    # Check if all questions answered
    if session.current_question >= len(QUESTIONS):
        return handle_completion(session)
    
    # Ask next question
    next_question = QUESTIONS[session.current_question]
    session_manager.update_session(session)
    
    return create_response(200, {
        'message': f"Great! Next question: {next_question.question_text}",
        'question_id': next_question.question_id,
        'help_text': next_question.help_text,
        'examples': next_question.examples,
        'progress': f"{session.current_question}/{len(QUESTIONS)}"
    })


def handle_completion(session) -> Dict[str, Any]:
    """Handle conversation completion and create GitHub Issue."""
    # Generate summary
    summary = generate_summary(session.answers)
    
    session.is_complete = True
    session_manager.update_session(session)
    
    # Create GitHub Issue
    try:
        issue_number = github_client.create_issue(session.answers)
        session.github_issue_number = issue_number
        session_manager.update_session(session)
        
        return create_response(200, {
            'message': f"Perfect! Here's your summary:\n\n{summary}\n\n"
                      f"Your AWS account request has been submitted as GitHub Issue #{issue_number}. "
                      f"The Account Factory will now provision your account. "
                      f"This typically takes 4-6 minutes. You'll receive updates via email.",
            'completed': True,
            'github_issue': issue_number,
            'summary': session.answers
        })
    except Exception as e:
        return create_response(500, {
            'error': f"Failed to create GitHub Issue: {str(e)}",
            'summary': session.answers
        })


def generate_summary(answers: Dict[str, Any]) -> str:
    """Generate human-readable summary of answers."""
    return f"""Team Name: {answers.get('team_name')}
Team Lead: {answers.get('team_lead')}
Email: {answers.get('email')}
Cost Center: {answers.get('cost_center')}
Data Classification: {answers.get('data_classification')}
Business Criticality: {answers.get('business_criticality')}
Use Case: {answers.get('use_case')}
Monthly Budget: ${answers.get('budget')}
AWS Services: {answers.get('aws_services', 'Not specified')}
Compliance: {answers.get('compliance', 'none')}"""


def handle_status(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GET /conversation/status - Get session status."""
    session_id = params.get('session_id')
    
    if not session_id:
        return create_response(400, {'error': 'session_id is required'})
    
    session = session_manager.get_session(session_id)
    if not session:
        return create_response(404, {'error': 'Session not found'})
    
    return create_response(200, {
        'session_id': session.session_id,
        'current_question': session.current_question,
        'total_questions': len(QUESTIONS),
        'is_complete': session.is_complete,
        'github_issue': session.github_issue_number,
        'time_remaining_minutes': session_manager.get_time_until_timeout(session)
    })


def handle_resume(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle POST /conversation/resume - Resume a timed-out session."""
    session_id = body.get('session_id')
    
    if not session_id:
        return create_response(400, {'error': 'session_id is required'})
    
    session = session_manager.get_session(session_id)
    if not session:
        return create_response(404, {'error': 'Session not found or expired'})
    
    current_question = QUESTIONS[session.current_question]
    
    return create_response(200, {
        'message': f"Welcome back! Let's continue. {current_question.question_text}",
        'question_id': current_question.question_id,
        'help_text': current_question.help_text,
        'progress': f"{session.current_question}/{len(QUESTIONS)}"
    })


def handle_end_conversation(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle DELETE /conversation/end - End conversation."""
    session_id = body.get('session_id')
    
    if not session_id:
        return create_response(400, {'error': 'session_id is required'})
    
    session_manager.delete_session(session_id)
    
    return create_response(200, {
        'message': 'Conversation ended successfully'
    })


def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """Create API Gateway response."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization'
        },
        'body': json.dumps(body)
    }
