"""
Auto-corrector for intake form responses.
"""
import re
from typing import Optional
from src.models import CorrectionResult


class AutoCorrector:
    """Auto-corrects common formatting issues in user responses."""

    # AWS service name mappings
    AWS_SERVICE_MAPPINGS = {
        'ec2': 'EC2',
        's3': 'S3',
        'rds': 'RDS',
        'lambda': 'Lambda',
        'dynamodb': 'DynamoDB',
        'cloudwatch': 'CloudWatch',
        'iam': 'IAM',
        'vpc': 'VPC',
        'elb': 'ELB',
        'cloudfront': 'CloudFront',
        'route53': 'Route53',
        'sns': 'SNS',
        'sqs': 'SQS',
        'eks': 'EKS',
        'ecs': 'ECS',
        'fargate': 'Fargate',
        'sagemaker': 'SageMaker',
        'redshift': 'Redshift',
        'athena': 'Athena',
        'glue': 'Glue'
    }

    def correct_team_name(self, value: str) -> CorrectionResult:
        """Correct team name: lowercase, remove spaces, replace underscores."""
        original = value
        corrections = []
        
        # Convert to lowercase
        if value != value.lower():
            value = value.lower()
            corrections.append("converted to lowercase")
        
        # Replace spaces with hyphens
        if ' ' in value:
            value = value.replace(' ', '-')
            corrections.append("replaced spaces with hyphens")
        
        # Replace underscores with hyphens
        if '_' in value:
            value = value.replace('_', '-')
            corrections.append("replaced underscores with hyphens")
        
        # Remove special characters except hyphens and alphanumeric
        cleaned = re.sub(r'[^a-z0-9-]', '', value)
        if cleaned != value:
            value = cleaned
            corrections.append("removed special characters")
        
        # Remove consecutive hyphens
        while '--' in value:
            value = value.replace('--', '-')
        
        # Remove leading/trailing hyphens
        value = value.strip('-')
        
        return CorrectionResult(
            original_value=original,
            corrected_value=value,
            corrections_applied=corrections,
            requires_confirmation=len(corrections) > 0
        )

    def correct_email(self, value: str) -> CorrectionResult:
        """Correct email: lowercase."""
        original = value
        corrections = []
        
        value = value.strip()
        
        if value != value.lower():
            value = value.lower()
            corrections.append("converted to lowercase")
        
        return CorrectionResult(
            original_value=original,
            corrected_value=value,
            corrections_applied=corrections,
            requires_confirmation=len(corrections) > 0
        )

    def correct_cost_center(self, value: str) -> CorrectionResult:
        """Correct cost center: uppercase CC prefix and department."""
        original = value
        corrections = []
        
        value = value.strip()
        
        # Parse cost center format
        parts = value.split('-')
        if len(parts) == 3:
            prefix, dept, number = parts
            
            # Uppercase prefix
            if prefix != prefix.upper():
                prefix = prefix.upper()
                corrections.append("converted prefix to uppercase")
            
            # Uppercase department
            if dept != dept.upper():
                dept = dept.upper()
                corrections.append("converted department to uppercase")
            
            value = f"{prefix}-{dept}-{number}"
        else:
            # Try to fix common formats
            if value.upper() != value:
                value = value.upper()
                corrections.append("converted to uppercase")
        
        return CorrectionResult(
            original_value=original,
            corrected_value=value,
            corrections_applied=corrections,
            requires_confirmation=len(corrections) > 0
        )

    def correct_data_classification(self, value: str) -> CorrectionResult:
        """Correct data classification: lowercase."""
        original = value
        corrections = []
        
        value = value.strip()
        
        if value != value.lower():
            value = value.lower()
            corrections.append("converted to lowercase")
        
        return CorrectionResult(
            original_value=original,
            corrected_value=value,
            corrections_applied=corrections,
            requires_confirmation=len(corrections) > 0
        )

    def correct_business_criticality(self, value: str) -> CorrectionResult:
        """Correct business criticality: lowercase."""
        original = value
        corrections = []
        
        value = value.strip()
        
        if value != value.lower():
            value = value.lower()
            corrections.append("converted to lowercase")
        
        return CorrectionResult(
            original_value=original,
            corrected_value=value,
            corrections_applied=corrections,
            requires_confirmation=len(corrections) > 0
        )

    def correct_use_case(self, value: str) -> CorrectionResult:
        """Correct use case: lowercase, replace spaces with hyphens."""
        original = value
        corrections = []
        
        value = value.strip()
        
        # Convert to lowercase
        if value != value.lower():
            value = value.lower()
            corrections.append("converted to lowercase")
        
        # Replace spaces with hyphens
        if ' ' in value:
            value = value.replace(' ', '-')
            corrections.append("replaced spaces with hyphens")
        
        # Remove consecutive hyphens
        while '--' in value:
            value = value.replace('--', '-')
        
        return CorrectionResult(
            original_value=original,
            corrected_value=value,
            corrections_applied=corrections,
            requires_confirmation=len(corrections) > 0
        )

    def correct_budget(self, value: str) -> CorrectionResult:
        """Correct budget: expand shorthand (5k -> 5000), remove currency symbols."""
        original = value
        corrections = []
        
        value = value.strip()
        
        # Remove currency symbols
        if '$' in value or '€' in value or '£' in value:
            value = re.sub(r'[$€£]', '', value)
            corrections.append("removed currency symbols")
        
        # Remove commas
        if ',' in value:
            value = value.replace(',', '')
            corrections.append("removed commas")
        
        # Expand shorthand (k, K for thousands)
        if value.lower().endswith('k'):
            try:
                number = float(value[:-1])
                value = str(int(number * 1000))
                corrections.append("expanded 'k' to thousands")
            except ValueError:
                pass
        
        return CorrectionResult(
            original_value=original,
            corrected_value=value,
            corrections_applied=corrections,
            requires_confirmation=len(corrections) > 0
        )

    def correct_aws_services(self, value: Optional[str]) -> CorrectionResult:
        """Correct AWS services: normalize service names."""
        if not value or value.strip() == "":
            return CorrectionResult(
                original_value=value or "",
                corrected_value="",
                corrections_applied=[],
                requires_confirmation=False
            )
        
        original = value
        corrections = []
        
        services = [s.strip() for s in value.split(',')]
        corrected_services = []
        
        for service in services:
            service_lower = service.lower()
            if service_lower in self.AWS_SERVICE_MAPPINGS:
                corrected = self.AWS_SERVICE_MAPPINGS[service_lower]
                corrected_services.append(corrected)
                if corrected != service:
                    corrections.append(f"normalized '{service}' to '{corrected}'")
            else:
                corrected_services.append(service)
        
        value = ', '.join(corrected_services)
        
        return CorrectionResult(
            original_value=original,
            corrected_value=value,
            corrections_applied=corrections,
            requires_confirmation=len(corrections) > 0
        )

    def correct_compliance(self, value: Optional[str]) -> CorrectionResult:
        """Correct compliance: normalize framework names."""
        if not value or value.strip() == "" or value.strip().lower() == "none":
            return CorrectionResult(
                original_value=value or "",
                corrected_value="none" if value else "",
                corrections_applied=[],
                requires_confirmation=False
            )
        
        original = value
        corrections = []
        
        value = value.strip()
        
        # Normalize common variations
        replacements = {
            'HIPAA': 'hipaa',
            'Hipaa': 'hipaa',
            'PCI DSS': 'pci-dss',
            'PCI-DSS': 'pci-dss',
            'pci dss': 'pci-dss',
            'SOX': 'sox',
            'Sox': 'sox',
            'NONE': 'none',
            'None': 'none'
        }
        
        for old, new in replacements.items():
            if old in value:
                value = value.replace(old, new)
                corrections.append(f"normalized '{old}' to '{new}'")
        
        # Convert to lowercase if not already
        if value != value.lower():
            value = value.lower()
            if not corrections:
                corrections.append("converted to lowercase")
        
        return CorrectionResult(
            original_value=original,
            corrected_value=value,
            corrections_applied=corrections,
            requires_confirmation=len(corrections) > 0
        )

    def correct_response(self, field_name: str, value: str) -> CorrectionResult:
        """Correct a response based on field name."""
        correctors = {
            'team_name': self.correct_team_name,
            'team_lead': lambda v: CorrectionResult(v, v, [], False),  # No corrections
            'email': self.correct_email,
            'cost_center': self.correct_cost_center,
            'data_classification': self.correct_data_classification,
            'business_criticality': self.correct_business_criticality,
            'use_case': self.correct_use_case,
            'budget': self.correct_budget,
            'aws_services': self.correct_aws_services,
            'compliance': self.correct_compliance
        }
        
        corrector = correctors.get(field_name)
        if not corrector:
            return CorrectionResult(value, value, [], False)
        
        return corrector(value)
