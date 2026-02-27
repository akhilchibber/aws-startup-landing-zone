"""
Core data models for the Bedrock Conversational Intake system.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class QuestionStatus(Enum):
    """Status of a question in the conversation flow."""
    PENDING = "pending"
    ANSWERED = "answered"
    VALIDATING = "validating"
    CORRECTING = "correcting"
    CONFIRMED = "confirmed"


class DataClassification(Enum):
    """Valid data classification levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class BusinessCriticality(Enum):
    """Valid business criticality levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UseCase(Enum):
    """Predefined use cases."""
    WEB_APPLICATION = "web-application"
    DATA_ANALYTICS = "data-analytics"
    MACHINE_LEARNING = "machine-learning"
    BACKUP_STORAGE = "backup-storage"
    CUSTOM = "custom"


@dataclass
class ValidationResult:
    """Result of validating a user response."""
    is_valid: bool
    error_message: Optional[str] = None
    field_name: Optional[str] = None


@dataclass
class CorrectionResult:
    """Result of auto-correcting a user response."""
    original_value: str
    corrected_value: str
    corrections_applied: List[str] = field(default_factory=list)
    requires_confirmation: bool = True


@dataclass
class QuestionConfig:
    """Configuration for a single intake question."""
    question_id: str
    question_text: str
    field_name: str
    validation_rules: Dict[str, Any]
    correction_rules: Dict[str, Any]
    help_text: str
    examples: List[str] = field(default_factory=list)


@dataclass
class SessionState:
    """State of a conversation session."""
    session_id: str
    user_id: str
    current_question: int
    answers: Dict[str, Any] = field(default_factory=dict)
    validation_attempts: Dict[str, int] = field(default_factory=dict)
    corrections_pending: Dict[str, CorrectionResult] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    ttl: int = 0  # Unix timestamp for DynamoDB TTL
    is_complete: bool = False
    github_issue_number: Optional[int] = None

    def to_dynamodb_item(self) -> Dict[str, Any]:
        """Convert session state to DynamoDB item format."""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'current_question': self.current_question,
            'answers': self.answers,
            'validation_attempts': self.validation_attempts,
            'corrections_pending': {k: {
                'original_value': v.original_value,
                'corrected_value': v.corrected_value,
                'corrections_applied': v.corrections_applied,
                'requires_confirmation': v.requires_confirmation
            } for k, v in self.corrections_pending.items()},
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'ttl': self.ttl,
            'is_complete': self.is_complete,
            'github_issue_number': self.github_issue_number
        }

    @classmethod
    def from_dynamodb_item(cls, item: Dict[str, Any]) -> 'SessionState':
        """Create session state from DynamoDB item."""
        corrections_pending = {}
        for k, v in item.get('corrections_pending', {}).items():
            corrections_pending[k] = CorrectionResult(
                original_value=v['original_value'],
                corrected_value=v['corrected_value'],
                corrections_applied=v['corrections_applied'],
                requires_confirmation=v['requires_confirmation']
            )
        
        return cls(
            session_id=item['session_id'],
            user_id=item['user_id'],
            current_question=item['current_question'],
            answers=item.get('answers', {}),
            validation_attempts=item.get('validation_attempts', {}),
            corrections_pending=corrections_pending,
            created_at=datetime.fromisoformat(item['created_at']),
            updated_at=datetime.fromisoformat(item['updated_at']),
            ttl=item.get('ttl', 0),
            is_complete=item.get('is_complete', False),
            github_issue_number=item.get('github_issue_number')
        )
