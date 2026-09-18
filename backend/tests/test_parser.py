from app.parser import parse_log_line


def test_parse_login_failed():
    log = "2026-09-16 14:03:12 INFO Login failed user=alice ip=192.168.1.20"

    event = parse_log_line(log)

    assert event.event_type == "login_failed"
    assert event.user == "alice"
    assert event.ip == "192.168.1.20"
    assert event.level == "INFO"


def test_parse_api_request():
    log = "2026-09-16 14:04:13 INFO API request user=alice endpoint=/admin/users"

    event = parse_log_line(log)

    assert event.event_type == "api_request"
    assert event.user == "alice"
    assert event.metadata["endpoint"] == "/admin/users"