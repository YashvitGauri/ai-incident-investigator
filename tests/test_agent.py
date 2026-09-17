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