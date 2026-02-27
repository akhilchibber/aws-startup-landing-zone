"""
Unit tests for auto-corrector.
"""
import pytest
from src.auto_corrector import AutoCorrector


@pytest.fixture
def corrector():
    return AutoCorrector()


class TestTeamNameCorrection:
    def test_uppercase_to_lowercase(self, corrector):
        result = corrector.correct_team_name("Radiology-Team")
        assert result.corrected_value == "radiology-team"
        assert "converted to lowercase" in result.corrections_applied

    def test_spaces_to_hyphens(self, corrector):
        result = corrector.correct_team_name("radiology team")
        assert result.corrected_value == "radiology-team"
        assert "replaced spaces with hyphens" in result.corrections_applied

    def test_underscores_to_hyphens(self, corrector):
        result = corrector.correct_team_name("radiology_team")
        assert result.corrected_value == "radiology-team"
        assert "replaced underscores with hyphens" in result.corrections_applied

    def test_remove_special_chars(self, corrector):
        result = corrector.correct_team_name("radiology@team!")
        assert result.corrected_value == "radiologyteam"
        assert "removed special characters" in result.corrections_applied


class TestEmailCorrection:
    def test_uppercase_to_lowercase(self, corrector):
        result = corrector.correct_email("USER@EXAMPLE.COM")
        assert result.corrected_value == "user@example.com"
        assert "converted to lowercase" in result.corrections_applied


class TestBudgetCorrection:
    def test_expand_k_shorthand(self, corrector):
        result = corrector.correct_budget("5k")
        assert result.corrected_value == "5000"
        assert "expanded 'k' to thousands" in result.corrections_applied

    def test_remove_currency_symbols(self, corrector):
        result = corrector.correct_budget("$5000")
        assert result.corrected_value == "5000"
        assert "removed currency symbols" in result.corrections_applied

    def test_remove_commas(self, corrector):
        result = corrector.correct_budget("5,000")
        assert result.corrected_value == "5000"
        assert "removed commas" in result.corrections_applied

    def test_combined_corrections(self, corrector):
        result = corrector.correct_budget("$10,5k")
        assert result.corrected_value == "10500"
        assert len(result.corrections_applied) >= 2


class TestAWSServicesCorrection:
    def test_normalize_service_names(self, corrector):
        result = corrector.correct_aws_services("ec2, s3, lambda")
        assert result.corrected_value == "EC2, S3, Lambda"
        assert len(result.corrections_applied) > 0

    def test_empty_services(self, corrector):
        result = corrector.correct_aws_services("")
        assert result.corrected_value == ""
        assert result.requires_confirmation is False


class TestComplianceCorrection:
    def test_normalize_hipaa(self, corrector):
        result = corrector.correct_compliance("HIPAA")
        assert result.corrected_value == "hipaa"
        assert "normalized 'HIPAA' to 'hipaa'" in result.corrections_applied

    def test_normalize_pci_dss(self, corrector):
        result = corrector.correct_compliance("PCI DSS")
        assert result.corrected_value == "pci-dss"
        assert "normalized 'PCI DSS' to 'pci-dss'" in result.corrections_applied
