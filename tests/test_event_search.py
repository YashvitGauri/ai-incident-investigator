from app.models import Event
from app.tools.event_search import create_event_search_tool


def test_search_events_by_user():
    events = [
        Event(
            timestamp="2026-09-16 14:03:12",
            level="INFO",
            event_type="login_failed",
            user="alice",
            ip="192.168.1.20",
        ),
        Event(
            timestamp="2026-09-16 14:06:21",
            level="WARN",
            event_type="login_failed",
            user="bob",
            ip="10.0.0.15",
        ),
    ]

    search_events = create_event_search_tool(events)

    results = search_events.invoke({
        "user": "alice"
    })

    assert len(results) == 1
    assert "user=alice" in results[0]


def test_search_events_by_ip():
    events = [
        Event(
            timestamp="2026-09-16 14:03:12",
            level="INFO",
            event_type="login_failed",
            user="alice",
            ip="192.168.1.20",
        ),
        Event(
            timestamp="2026-09-16 14:06:21",
            level="WARN",
            event_type="login_failed",
            user="bob",
            ip="10.0.0.15",
        ),
    ]

    search_events = create_event_search_tool(events)

    results = search_events.invoke({
        "ip": "10.0.0.15"
    })

    assert len(results) == 1
    assert "user=bob" in results[0]