from app.models import Event
from app.pipeline import investigate_log_file


def test_investigate_log_file(monkeypatch):
    def fake_investigate_events(events):
        assert len(events) == 7

        assert events[0] == Event(
            timestamp="2026-09-16 14:03:12",
            level="INFO",
            event_type="login_failed",
            user="alice",
            ip="192.168.1.20",
        )

        assert events[3].event_type == "login_success"
        assert events[4].event_type == "api_request"

        return ["fake-report"]

    monkeypatch.setattr(
        "app.pipeline.investigate_events",
        fake_investigate_events,
    )

    result = investigate_log_file("data/raw/sample.log")

    assert result == ["fake-report"]