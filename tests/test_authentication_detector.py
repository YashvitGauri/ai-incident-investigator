from app.models import Event
from app.detectors.authentication import detect

def test_detect_suspicious_login_sequence():
    events = [
        Event(
            timestamp="2026-09-16 14:03:12",
            level="INFO",
            event_type="login_failed",
            user="alice",
            ip="192.168.1.20",
        ),
        Event(
            timestamp="2026-09-16 14:03:14",
            level="INFO",
            event_type="login_failed",
            user="alice",
            ip="192.168.1.20",
        ),
        Event(
            timestamp="2026-09-16 14:03:16",
            level="INFO",
            event_type="login_failed",
            user="alice",
            ip="192.168.1.20",
        ),
        Event(
            timestamp="2026-09-16 14:04:01",
            level="INFO",
            event_type="login_success",
            user="alice",
            ip="192.168.1.20",
        ),
    ]

    findings = detect(events)

    assert len(findings) == 1
    assert findings[0].type == "suspicious_login_sequence"


def test_ignore_normal_login():
    events = [
        Event(
            timestamp="2026-09-16 14:03:12",
            level="INFO",
            event_type="login_failed",
            user="alice",
            ip="192.168.1.20",
        ),
        Event(
            timestamp="2026-09-16 14:04:01",
            level="INFO",
            event_type="login_success",
            user="alice",
            ip="192.168.1.20",
        ),
    ]

    findings = detect(events)

    assert len(findings) == 0