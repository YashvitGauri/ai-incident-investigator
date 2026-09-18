from app.ai.investigator import InvestigationReport, investigate
from app.models import Event, Finding, Incident


class FakeResponse:
    def __init__(self, report):
        self.parsed = report


class FakeModels:
    def generate_content(self, **kwargs):
        return FakeResponse(
            InvestigationReport(
                summary="Suspicious login sequence detected.",
                severity="High",
                observed_evidence=[
                    "2026-09-16 14:03:12 login_failed user=alice"
                ],
                analysis="Multiple failed logins were followed by a successful login.",
                possible_explanations=[
                    "Possible credential attack."
                ],
                confidence="High",
                recommended_actions=[
                    "Review authentication logs."
                ],
                uncertainty="The evidence does not confirm account compromise.",
            )
        )


class FakeClient:
    def __init__(self):
        self.models = FakeModels()


def test_investigate_returns_report():
    event = Event(
        timestamp="2026-09-16 14:03:12",
        level="INFO",
        event_type="login_failed",
        user="alice",
        ip="192.168.1.20",
    )

    finding = Finding(
        type="suspicious_login_sequence",
        user="alice",
        ip="192.168.1.20",
        description="Multiple failed logins followed by a successful login.",
        evidence=[event],
    )

    incident = Incident(
        id="INC-0001",
        findings=[finding],
    )

    report = investigate(
        incident,
        client=FakeClient(),
    )

    assert isinstance(report, InvestigationReport)
    assert report.summary == "Suspicious login sequence detected."
    assert report.severity == "High"
    assert report.confidence == "High"
    assert len(report.observed_evidence) == 1