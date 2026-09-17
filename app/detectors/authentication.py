from datetime import datetime, timedelta
from app.models import Finding


def detect(events):
    events = sorted(events, key=lambda event: event.timestamp)

    suspicious_sequences = []

    for i, event in enumerate(events):
        if event.event_type != "login_success":
            continue

        failed_logins = []

        for previous_event in events[:i]:
            if (
                previous_event.event_type == "login_failed"
                and previous_event.user == event.user
                and previous_event.ip == event.ip
            ):
                failed_logins.append(previous_event)

        if not failed_logins:
            continue

        success_time = datetime.fromisoformat(event.timestamp)

        recent_failures = [
            failed
            for failed in failed_logins
            if success_time - datetime.fromisoformat(failed.timestamp)
            <= timedelta(minutes=5)
        ]

        if len(recent_failures) >= 3:
            suspicious_sequences.append(
                Finding(
                    type="suspicious_login_sequence",
                    user=event.user,
                    ip=event.ip,
                    description=(
                        f"{event.user} had {len(recent_failures)} failed login attempts "
                        f"from {event.ip} followed by a successful login."
                    ),
                    evidence=recent_failures + [event],
                )
            )

    return suspicious_sequences


if __name__ == "__main__":
    from app.log_reader import read_logs

    events = read_logs("data/raw/sample.log")

    findings = detect(events)

    for finding in findings:
        print(finding)