from app.ai.investigator import investigate
from app.correlator import correlate_findings
from app.detectors.engine import run_detectors
from app.log_reader import read_logs


def investigate_log_file(file_path: str):
    events = read_logs(file_path)

    findings = run_detectors(events)

    incidents = correlate_findings(findings)

    reports = []

    for incident in incidents:
        report = investigate(incident)
        reports.append((incident, report))

    return reports