from app.models import Finding
from app.severity import calculate_severity


def test_no_findings_is_low():
    assert calculate_severity([]) == "Low"


def test_single_finding_is_medium():
    finding = Finding(
        type="suspicious_login_sequence",
        description="Suspicious login sequence.",
    )

    assert calculate_severity([finding]) == "Medium"


def test_login_and_sensitive_api_is_high():
    login_finding = Finding(
        type="suspicious_login_sequence",
        description="Suspicious login sequence.",
    )

    api_finding = Finding(
        type="sensitive_api_access",
        description="Sensitive API access.",
    )

    assert calculate_severity(
        [login_finding, api_finding]
    ) == "High"