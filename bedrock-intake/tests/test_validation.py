"""
Unit tests for validation engine.
"""
import pytest
from src.validation_engine import ValidationEngine


@pytest.fixture
def validator():
    return ValidationEngine()


class TestTeamNameValidation:
    def test_valid_team_name(self, validator):
        result = validator.validate_team_name("radiology-team")
        assert result.is_valid is True

    def test_uppercase_rejected(self, validator):
        result = validator.validate_team_name("Radiology-Team")
        assert result.is_valid is False
        assert "lowercase" in result.error_message

    def test_too_short(self, validator):
        result = validator.validate_team_name("ab")
        assert result.is_valid is False
        assert "at least 3" in result.error_message

    def test_too_long(self, validator):
        result = validator.validate_team_name("a" * 31)
        assert result.is_valid is False
        assert "at most 30" in result.error_message

    def test_special_chars_rejected(self, validator):
        result = validator.validate_team_name("radiology@team")
        assert result.is_valid is False


class TestEmailValidation:
    def test_valid_email(self, validator):
        result = validator.validate_email("user@example.com")
        assert result.is_valid is True

    def test_invalid_format(self, validator):
        result = validator.validate_email("not-an-email")
        assert result.is_valid is False

    def test_missing_domain(self, validator):
        result = validator.validate_email("user@")
        assert result.is_valid is False


class TestCostCenterValidation:
    def test_valid_cost_center(self, validator):
        result = validator.validate_cost_center("CC-RAD-1234")
        assert result.is_valid is True

    def test_invalid_format(self, validator):
        result = validator.validate_cost_center("RAD-1234")
        assert result.is_valid is False

    def test_lowercase_rejected(self, validator):
        result = validator.validate_cost_center("cc-rad-1234")
        assert result.is_valid is False


class TestBudgetValidation:
    def test_valid_budget(self, validator):
        result = validator.validate_budget("5000")
        assert result.is_valid is True

    def test_too_low(self, validator):
        result = validator.validate_budget("50")
        assert result.is_valid is False
        assert "at least $100" in result.error_message

    def test_too_high(self, validator):
        result = validator.validate_budget("150000")
        assert result.is_valid is False
        assert "at most $100,000" in result.error_message

    def test_non_numeric(self, validator):
        result = validator.validate_budget("five thousand")
        assert result.is_valid is False
