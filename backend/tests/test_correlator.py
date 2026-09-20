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
    assert incidents[0].severity == "High"


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

def test_keep_same_user_separate_when_findings_are_far_apart():
    login_event = Event(
        timestamp="2026-09-16 14:03:12",
        level="INFO",
        event_type="login_failed",
        user="alice",
        ip="192.168.1.20",
    )

    api_event = Event(
        timestamp="2026-09-16 18:30:00",
        level="INFO",
        event_type="api_request",
        user="alice",
        metadata={"endpoint": "/admin/users"},
    )

    login_finding = Finding(
        type="suspicious_login_sequence",
        user="alice",
        ip="192.168.1.20",
        evidence=[login_event],
    )

    api_finding = Finding(
        type="sensitive_api_access",
        user="alice",
        evidence=[api_event],
    )

    incidents = correlate_findings(
        [login_finding, api_finding]
    )

    assert len(incidents) == 2


def test_correlate_findings_by_ip():
    first_event = Event(
        timestamp="2026-09-16 14:03:12",
        level="INFO",
        event_type="login_failed",
        ip="192.168.1.20",
    )

    second_event = Event(
        timestamp="2026-09-16 14:04:13",
        level="INFO",
        event_type="api_request",
        ip="192.168.1.20",
        metadata={"endpoint": "/admin/users"},
    )

    first_finding = Finding(
        type="suspicious_login_sequence",
        ip="192.168.1.20",
        evidence=[first_event],
    )

    second_finding = Finding(
        type="sensitive_api_access",
        ip="192.168.1.20",
        evidence=[second_event],
    )

    incidents = correlate_findings(
        [first_finding, second_finding]
    )

    assert len(incidents) == 1
    assert len(incidents[0].findings) == 2