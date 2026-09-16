import re
from models import Event

def parse_message(message):
    event = {}

    if message.startswith("Login failed"):
        event["event_type"] = "login_failed"

    elif message.startswith("Login successful"):
        event["event_type"] = "login_success"

    elif message.startswith("API request"):
        event["event_type"] = "api_request"

    user_match = re.search(r"user=(\S+)", message)
    if user_match:
        event["user"] = user_match.group(1)

    ip_match = re.search(r"ip=(\S+)", message)
    if ip_match:
        event["ip"] = ip_match.group(1)

    endpoint_match = re.search(r"endpoint=(\S+)", message)
    if endpoint_match:
        event["endpoint"] = endpoint_match.group(1)

    return event


def parse_log_line(line):
    pattern = (
        r"(?P<timestamp>\S+ \S+) "
        r"(?P<level>\w+) "
        r"(?P<message>.*)"
    )

    match = re.match(pattern, line)

    if not match:
        return None

    parsed = match.groupdict()
    event = parse_message(parsed["message"])

    return Event(
    timestamp=parsed["timestamp"],
    level=parsed["level"],
    event_type=event.get("event_type", "unknown"),
    user=event.get("user"),
    ip=event.get("ip"),
    metadata={
        key: value
        for key, value in event.items()
        if key not in {"event_type", "user", "ip"}
    }
)


if __name__ == "__main__":
    log = "2026-09-16 14:04:13 INFO API request user=alice endpoint=/admin/users"

    print(parse_log_line(log))