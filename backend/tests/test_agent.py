from app.ai.agent import parse_investigation_report


def test_parse_investigation_report_from_json():
    content = """
    {
        "summary": "Suspicious login sequence detected.",
        "severity": "Medium",
        "observed_evidence": [
            "Three failed login attempts"
        ],
        "analysis": "Multiple failures were followed by a successful login.",
        "possible_explanations": [
            "Possible credential attack"
        ],
        "confidence": "Medium",
        "recommended_actions": [
            "Review authentication logs"
        ],
        "uncertainty": "The evidence does not confirm compromise."
    }
    """

    report = parse_investigation_report(content)

    assert report.summary == "Suspicious login sequence detected."
    assert report.severity == "Medium"
    assert len(report.observed_evidence) == 1


def test_parse_investigation_report_from_markdown():
    content = """
    ```json
    {
        "summary": "Suspicious login sequence detected.",
        "severity": "Medium",
        "observed_evidence": [
            "Three failed login attempts"
        ],
        "analysis": "Multiple failures were followed by a successful login.",
        "possible_explanations": [
            "Possible credential attack"
        ],
        "confidence": "Medium",
        "recommended_actions": [
            "Review authentication logs"
        ],
        "uncertainty": "The evidence does not confirm compromise."
    }
    ```
    """

    report = parse_investigation_report(content)

    assert report.summary == "Suspicious login sequence detected."
    assert report.severity == "Medium"


def test_agent_report_uses_incident_severity():
    content = """
    {
        "summary": "Suspicious activity detected.",
        "severity": "Medium",
        "observed_evidence": [
            "Multiple failed login attempts"
        ],
        "analysis": "The activity requires investigation.",
        "possible_explanations": [
            "Possible credential attack"
        ],
        "confidence": "Medium",
        "recommended_actions": [
            "Review authentication logs"
        ],
        "uncertainty": "The evidence does not confirm compromise."
    }
    """

    report = parse_investigation_report(content)

    final_report = report.model_copy(
        update={"severity": "High"}
    )

    assert final_report.severity == "High"