"""
Session manager for conversation state persistence.
"""
import boto3
import uuid
from datetime import datetime, timedelta
from typing import Optional
from src.models import SessionState


class SessionManager:
    """Manages conversation session state in DynamoDB."""

    def __init__(self, table_name: str):
        """Initialize session manager with DynamoDB table name."""
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        self.session_timeout_minutes = 30
        self.session_ttl_hours = 24

    def create_session(self, user_id: str) -> SessionState:
        """Create a new conversation session."""
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()
        ttl = int((now + timedelta(hours=self.session_ttl_hours)).timestamp())
        
        session = SessionState(
            session_id=session_id,
            user_id=user_id,
            current_question=0,
            created_at=now,
            updated_at=now,
            ttl=ttl
        )
        
        # Persist to DynamoDB
        self.table.put_item(Item=session.to_dynamodb_item())
        
        return session

    def get_session(self, session_id: str) -> Optional[SessionState]:
        """Retrieve an existing session from DynamoDB."""
        try:
            response = self.table.get_item(Key={'session_id': session_id})
            
            if 'Item' not in response:
                return None
            
            return SessionState.from_dynamodb_item(response['Item'])
        except Exception as e:
            print(f"Error retrieving session {session_id}: {e}")
            return None

    def update_session(self, session: SessionState) -> bool:
        """Update session state in DynamoDB."""
        try:
            session.updated_at = datetime.utcnow()
            self.table.put_item(Item=session.to_dynamodb_item())
            return True
        except Exception as e:
            print(f"Error updating session {session.session_id}: {e}")
            return False

    def check_timeout(self, session: SessionState) -> bool:
        """Check if session has timed out due to inactivity."""
        now = datetime.utcnow()
        time_since_update = now - session.updated_at
        
        return time_since_update > timedelta(minutes=self.session_timeout_minutes)

    def delete_session(self, session_id: str) -> bool:
        """Delete a session from DynamoDB."""
        try:
            self.table.delete_item(Key={'session_id': session_id})
            return True
        except Exception as e:
            print(f"Error deleting session {session_id}: {e}")
            return False

    def get_time_until_timeout(self, session: SessionState) -> int:
        """Get minutes remaining until session timeout."""
        now = datetime.utcnow()
        time_since_update = now - session.updated_at
        remaining = timedelta(minutes=self.session_timeout_minutes) - time_since_update
        
        return max(0, int(remaining.total_seconds() / 60))
