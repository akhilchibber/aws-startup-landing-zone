"""
Question definitions and validation rules for the intake form.
"""
from src.models import QuestionConfig

# All 10 intake questions with validation and correction rules
QUESTIONS = [
    QuestionConfig(
        question_id="q1",
        question_text="What is your team name? (lowercase, hyphens only, 3-30 characters)",
        field_name="team_name",
        validation_rules={
            "pattern": r"^[a-z0-9-]{3,30}$",
            "min_length": 3,
            "max_length": 30,
            "allowed_chars": "lowercase letters, numbers, hyphens"
        },
        correction_rules={
            "lowercase": True,
            "remove_spaces": True,
            "replace_underscores": True,
            "remove_special_chars": True
        },
        help_text="Team name must be lowercase with hyphens, 3-30 characters (e.g., radiology-team)",
        examples=["radiology-team", "cardiology-dept", "emergency-care"]
    ),
    QuestionConfig(
        question_id="q2",
        question_text="Who is the team lead? (full name)",
        field_name="team_lead",
        validation_rules={
            "min_length": 2,
            "max_length": 100,
            "allowed_chars": "letters, spaces, hyphens, apostrophes"
        },
        correction_rules={},
        help_text="Provide the full name of the team lead",
        examples=["Dr. Sarah Johnson", "John Smith", "Maria Garcia-Lopez"]
    ),
    QuestionConfig(
        question_id="q3",
        question_text="What is the team lead's email address?",
        field_name="email",
        validation_rules={
            "pattern": r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$",
            "domain_required": True
        },
        correction_rules={
            "lowercase": True
        },
        help_text="Provide a valid email address",
        examples=["sarah.johnson@hospital.com", "john.smith@healthcare.org"]
    ),
    QuestionConfig(
        question_id="q4",
        question_text="What is your cost center code? (format: CC-DEPT-XXXX)",
        field_name="cost_center",
        validation_rules={
            "pattern": r"^CC-[A-Z]{2,10}-\d{4}$",
            "format": "CC-DEPT-XXXX"
        },
        correction_rules={
            "uppercase_prefix": True,
            "uppercase_dept": True
        },
        help_text="Cost center must follow format CC-DEPT-XXXX (e.g., CC-RAD-1234)",
        examples=["CC-RAD-1234", "CC-CARDIO-5678", "CC-EMERG-9012"]
    ),
    QuestionConfig(
        question_id="q5",
        question_text="What is the data classification level? (public, internal, confidential, restricted)",
        field_name="data_classification",
        validation_rules={
            "enum": ["public", "internal", "confidential", "restricted"]
        },
        correction_rules={
            "lowercase": True
        },
        help_text="Choose: public, internal, confidential, or restricted",
        examples=["public", "internal", "confidential", "restricted"]
    ),
    QuestionConfig(
        question_id="q6",
        question_text="What is the business criticality? (low, medium, high, critical)",
        field_name="business_criticality",
        validation_rules={
            "enum": ["low", "medium", "high", "critical"]
        },
        correction_rules={
            "lowercase": True
        },
        help_text="Choose: low, medium, high, or critical",
        examples=["low", "medium", "high", "critical"]
    ),
    QuestionConfig(
        question_id="q7",
        question_text="What is your primary use case? (web-application, data-analytics, machine-learning, backup-storage, or describe custom)",
        field_name="use_case",
        validation_rules={
            "predefined": ["web-application", "data-analytics", "machine-learning", "backup-storage"],
            "allow_custom": True,
            "custom_min_length": 10,
            "custom_max_length": 200
        },
        correction_rules={
            "lowercase": True,
            "replace_spaces_with_hyphens": True
        },
        help_text="Choose a predefined use case or describe your custom use case (10-200 characters)",
        examples=["web-application", "data-analytics", "patient-records-management"]
    ),
    QuestionConfig(
        question_id="q8",
        question_text="What is your monthly budget in USD? (100-100000)",
        field_name="budget",
        validation_rules={
            "min": 100,
            "max": 100000,
            "type": "integer"
        },
        correction_rules={
            "expand_shorthand": True,  # 5k -> 5000
            "remove_currency_symbols": True,
            "remove_commas": True
        },
        help_text="Enter monthly budget between $100 and $100,000",
        examples=["5000", "10000", "50000"]
    ),
    QuestionConfig(
        question_id="q9",
        question_text="Which AWS services do you plan to use? (optional, comma-separated)",
        field_name="aws_services",
        validation_rules={
            "optional": True,
            "max_services": 20
        },
        correction_rules={
            "normalize_service_names": True,  # ec2 -> EC2, s3 -> S3
            "trim_whitespace": True
        },
        help_text="List AWS services you plan to use (optional)",
        examples=["EC2, S3, RDS", "Lambda, DynamoDB", ""]
    ),
    QuestionConfig(
        question_id="q10",
        question_text="Do you require compliance frameworks? (optional: hipaa, pci-dss, sox, none)",
        field_name="compliance",
        validation_rules={
            "optional": True,
            "valid_frameworks": ["hipaa", "pci-dss", "sox", "none"]
        },
        correction_rules={
            "lowercase": True,
            "normalize_framework_names": True  # HIPAA -> hipaa, PCI DSS -> pci-dss
        },
        help_text="Specify compliance frameworks if required (optional)",
        examples=["hipaa", "pci-dss", "hipaa, sox", "none"]
    )
]

# Question lookup by ID
QUESTIONS_BY_ID = {q.question_id: q for q in QUESTIONS}

# Question lookup by field name
QUESTIONS_BY_FIELD = {q.field_name: q for q in QUESTIONS}
