from datetime import datetime

from app.models import Finding, Incident
from app.severity import calculate_severity


CORRELATION_WINDOW_MINUTES = 10


def _parse_timestamp(timestamp: str) -> datetime | None:
    try:
        return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def _finding_time_range(finding: Finding):
    timestamps = [
        _parse_timestamp(event.timestamp)
        for event in finding.evidence
    ]

    timestamps = [timestamp for timestamp in timestamps if timestamp is not None]

    if not timestamps:
        return None, None

    return min(timestamps), max(timestamps)


def _findings_are_related(
    finding_a: Finding,
    finding_b: Finding,
) -> bool:
    start_a, end_a = _finding_time_range(finding_a)
    start_b, end_b = _finding_time_range(finding_b)

    # If we cannot determine timing, don't make a correlation
    # based on time.
    if start_a is None or start_b is None:
        return False

    # Findings are temporally related if their time ranges
    # are within the configured correlation window.
    if end_a < start_b:
        time_gap = start_b - end_a
    elif end_b < start_a:
        time_gap = start_a - end_b
    else:
        time_gap = 0

    if time_gap.total_seconds() > CORRELATION_WINDOW_MINUTES * 60:
        return False

    # Same user is a strong correlation signal.
    if (
        finding_a.user is not None
        and finding_b.user is not None
        and finding_a.user == finding_b.user
    ):
        return True

    # Same IP is another correlation signal.
    if (
        finding_a.ip is not None
        and finding_b.ip is not None
        and finding_a.ip == finding_b.ip
    ):
        return True

    return False


def _incident_is_related(
    finding: Finding,
    incident: Incident,
) -> bool:
    return any(
        _findings_are_related(finding, existing_finding)
        for existing_finding in incident.findings
    )


def correlate_findings(findings: list[Finding]) -> list[Incident]:
    incidents: list[Incident] = []

    for finding in findings:
        matching_incident = None

        for incident in incidents:
            if _incident_is_related(finding, incident):
                matching_incident = incident
                break

        if matching_incident:
            matching_incident.findings.append(finding)
            matching_incident.severity = calculate_severity(
                matching_incident.findings
            )
        else:
            incidents.append(
                Incident(
                    id=f"INC-{len(incidents) + 1:04d}",
                    findings=[finding],
                    severity=calculate_severity([finding]),
                )
            )

    return incidents