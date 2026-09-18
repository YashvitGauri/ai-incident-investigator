from app.models import Finding, Incident
from app.severity import calculate_severity


def correlate_findings(findings: list[Finding]) -> list[Incident]:
    incidents = []

    for finding in findings:
        matching_incident = None

        for incident in incidents:
            if any(
                existing.user == finding.user
                and existing.user is not None
                for existing in incident.findings
            ):
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