from app.ai.agent import investigate_with_agent
from app.correlator import correlate_findings
from app.detectors.engine import run_detectors
from app.log_reader import read_logs
from app.parser import parse_log_line


def investigate_log_file(file_path: str):
    events = read_logs(file_path)
    return investigate_events(events)


def investigate_log_text(log_text: str):
    events = []

    for line in log_text.splitlines():
        line = line.strip()

        if not line:
            continue

        event = parse_log_line(line)

        if event:
            events.append(event)

    return investigate_events(events)


def investigate_events(events):
    findings = run_detectors(events)
    incidents = correlate_findings(findings)

    reports = []

    for incident in incidents:
        report = investigate_with_agent(
            incident,
            events,
        )
        reports.append((incident, report))

    return reports