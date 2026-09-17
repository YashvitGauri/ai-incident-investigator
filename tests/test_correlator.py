from app.correlator import correlate_findings
from app.models import Event, Finding


def test_correlate_findings_by_user():
    login_event = Event(
        timestamp="2026-09-16 14:03:12",
        level="INFO",
        event_type="login_failed",
        user="alice",
        ip="192.168.1.20",
    )

    api_event = Event(
        timestamp="2026-09-16 14:04:13",
        level="INFO",
        event_type="api_request",
        user="alice",
        metadata={"endpoint": "/admin/users"},
    )

    login_finding = Finding(
        type="suspicious_login_sequence",
        user="alice",
        ip="192.168.1.20",
        description="Suspicious login sequence.",
        evidence=[login_event],
    )

    api_finding = Finding(
        type="sensitive_api_access",
        user="alice",
        description="Sensitive API access.",
        evidence=[api_event],
    )

    incidents = correlate_findings(
        [login_finding, api_finding]
    )

    assert len(incidents) == 1
    assert incidents[0].id == "INC-0001"
    assert len(incidents[0].findings) == 2


def test_keep_different_users_separate():
    alice_finding = Finding(
        type="suspicious_login_sequence",
        user="alice",
    )

    bob_finding = Finding(
        type="sensitive_api_access",
        user="bob",
    )

    incidents = correlate_findings(
        [alice_finding, bob_finding]
    )

    assert len(incidents) == 2