from app.models import Finding, Incident


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
        else:
            incidents.append(
                Incident(
                    id=f"INC-{len(incidents) + 1:04d}",
                    findings=[finding],
                )
            )

    return incidents