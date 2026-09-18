from app.models import Finding


def calculate_severity(findings: list[Finding]) -> str:
    finding_types = {finding.type for finding in findings}

    if (
        "suspicious_login_sequence" in finding_types
        and "sensitive_api_access" in finding_types
    ):
        return "High"

    if finding_types:
        return "Medium"

    return "Low"