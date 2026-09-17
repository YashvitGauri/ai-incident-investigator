from app.models import Finding


SENSITIVE_ENDPOINTS = {
    "/admin/users",
    "/admin/export",
    "/admin/settings",
}


def detect(events):
    findings = []

    for event in events:
        if event.event_type != "api_request":
            continue

        endpoint = event.metadata.get("endpoint")

        if endpoint in SENSITIVE_ENDPOINTS:
            findings.append(
                Finding(
                    type="sensitive_api_access",
                    user=event.user,
                    description=(
                        f"{event.user} accessed sensitive endpoint "
                        f"{endpoint}."
                    ),
                    evidence=[event],
                )
            )

    return findings


if __name__ == "__main__":
    from app.log_reader import read_logs

    events = read_logs("data/raw/sample.log")
    findings = detect(events)

    for finding in findings:
        print(finding)