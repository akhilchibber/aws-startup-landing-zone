"""
Validation engine for intake form responses.
"""
import re
from typing import Optional
from src.models import ValidationResult, DataClassification, BusinessCriticality


class ValidationEngine:
    """Validates user responses against intake form requirements."""

    def validate_team_name(self, value: str) -> ValidationResult:
        """Validate team name: lowercase, hyphens only, 3-30 characters."""
        if not value or not isinstance(value, str):
            return ValidationResult(False, "Team name is required", "team_name")
        
        value = value.strip()
        
        if len(value) < 3:
            return ValidationResult(False, "Team name must be at least 3 characters", "team_name")
        
        if len(value) > 30:
            return ValidationResult(False, "Team name must be at most 30 characters", "team_name")
        
        if not re.match(r'^[a-z0-9-]+$', value):
            return ValidationResult(
                False, 
                "Team name must contain only lowercase letters, numbers, and hyphens", 
                "team_name"
            )
        
        return ValidationResult(True)

    def validate_team_lead(self, value: str) -> ValidationResult:
        """Validate team lead name: letters, spaces, hyphens, apostrophes."""
        if not value or not isinstance(value, str):
            return ValidationResult(False, "Team lead name is required", "team_lead")
        
        value = value.strip()
        
        if len(value) < 2:
            return ValidationResult(False, "Team lead name must be at least 2 characters", "team_lead")
        
        if len(value) > 100:
            return ValidationResult(False, "Team lead name must be at most 100 characters", "team_lead")
        
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", value):
            return ValidationResult(
                False,
                "Team lead name must contain only letters, spaces, hyphens, apostrophes, and periods",
                "team_lead"
            )
        
        return ValidationResult(True)

    def validate_email(self, value: str) -> ValidationResult:
        """Validate email address with domain check."""
        if not value or not isinstance(value, str):
            return ValidationResult(False, "Email address is required", "email")
        
        value = value.strip().lower()
        
        email_pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        if not re.match(email_pattern, value):
            return ValidationResult(False, "Invalid email address format", "email")
        
        return ValidationResult(True)

    def validate_cost_center(self, value: str) -> ValidationResult:
        """Validate cost center: format CC-DEPT-XXXX."""
        if not value or not isinstance(value, str):
            return ValidationResult(False, "Cost center is required", "cost_center")
        
        value = value.strip().upper()
        
        cost_center_pattern = r'^CC-[A-Z]{2,10}-\d{4}$'
        if not re.match(cost_center_pattern, value):
            return ValidationResult(
                False,
                "Cost center must follow format CC-DEPT-XXXX (e.g., CC-RAD-1234)",
                "cost_center"
            )
        
        return ValidationResult(True)

    def validate_data_classification(self, value: str) -> ValidationResult:
        """Validate data classification: public, internal, confidential, restricted."""
        if not value or not isinstance(value, str):
            return ValidationResult(False, "Data classification is required", "data_classification")
        
        value = value.strip().lower()
        
        valid_values = [e.value for e in DataClassification]
        if value not in valid_values:
            return ValidationResult(
                False,
                f"Data classification must be one of: {', '.join(valid_values)}",
                "data_classification"
            )
        
        return ValidationResult(True)

    def validate_business_criticality(self, value: str) -> ValidationResult:
        """Validate business criticality: low, medium, high, critical."""
        if not value or not isinstance(value, str):
            return ValidationResult(False, "Business criticality is required", "business_criticality")
        
        value = value.strip().lower()
        
        valid_values = [e.value for e in BusinessCriticality]
        if value not in valid_values:
            return ValidationResult(
                False,
                f"Business criticality must be one of: {', '.join(valid_values)}",
                "business_criticality"
            )
        
        return ValidationResult(True)

    def validate_use_case(self, value: str) -> ValidationResult:
        """Validate use case: predefined or custom (10-200 chars)."""
        if not value or not isinstance(value, str):
            return ValidationResult(False, "Use case is required", "use_case")
        
        value = value.strip().lower()
        
        predefined = ["web-application", "data-analytics", "machine-learning", "backup-storage"]
        
        if value in predefined:
            return ValidationResult(True)
        
        # Custom use case validation
        if len(value) < 10:
            return ValidationResult(
                False,
                "Custom use case must be at least 10 characters",
                "use_case"
            )
        
        if len(value) > 200:
            return ValidationResult(
                False,
                "Custom use case must be at most 200 characters",
                "use_case"
            )
        
        return ValidationResult(True)

    def validate_budget(self, value: str) -> ValidationResult:
        """Validate budget: integer between 100 and 100000."""
        if not value:
            return ValidationResult(False, "Budget is required", "budget")
        
        try:
            budget_int = int(value)
        except (ValueError, TypeError):
            return ValidationResult(False, "Budget must be a valid number", "budget")
        
        if budget_int < 100:
            return ValidationResult(False, "Budget must be at least $100", "budget")
        
        if budget_int > 100000:
            return ValidationResult(False, "Budget must be at most $100,000", "budget")
        
        return ValidationResult(True)

    def validate_aws_services(self, value: Optional[str]) -> ValidationResult:
        """Validate AWS services: optional, max 20 services."""
        if not value or value.strip() == "":
            return ValidationResult(True)  # Optional field
        
        services = [s.strip() for s in value.split(',') if s.strip()]
        
        if len(services) > 20:
            return ValidationResult(
                False,
                "Maximum 20 AWS services allowed",
                "aws_services"
            )
        
        return ValidationResult(True)

    def validate_compliance(self, value: Optional[str]) -> ValidationResult:
        """Validate compliance frameworks: optional, valid frameworks."""
        if not value or value.strip() == "" or value.strip().lower() == "none":
            return ValidationResult(True)  # Optional field
        
        value = value.strip().lower()
        valid_frameworks = ["hipaa", "pci-dss", "sox", "none"]
        
        frameworks = [f.strip() for f in value.split(',') if f.strip()]
        
        for framework in frameworks:
            if framework not in valid_frameworks:
                return ValidationResult(
                    False,
                    f"Invalid compliance framework: {framework}. Valid options: {', '.join(valid_frameworks)}",
                    "compliance"
                )
        
        return ValidationResult(True)

    def validate_response(self, field_name: str, value: str) -> ValidationResult:
        """Validate a response based on field name."""
        validators = {
            'team_name': self.validate_team_name,
            'team_lead': self.validate_team_lead,
            'email': self.validate_email,
            'cost_center': self.validate_cost_center,
            'data_classification': self.validate_data_classification,
            'business_criticality': self.validate_business_criticality,
            'use_case': self.validate_use_case,
            'budget': self.validate_budget,
            'aws_services': self.validate_aws_services,
            'compliance': self.validate_compliance
        }
        
        validator = validators.get(field_name)
        if not validator:
            return ValidationResult(False, f"Unknown field: {field_name}", field_name)
        
        return validator(value)
