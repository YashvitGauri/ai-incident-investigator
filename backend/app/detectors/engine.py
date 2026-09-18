from app.detectors import authentication
from app.detectors import api_abuse


def run_detectors(events):
    detectors = [
        authentication.detect,
        api_abuse.detect,
    ]

    findings = []

    for detector in detectors:
        findings.extend(detector(events))

    return findings

if __name__ == "__main__":
    from app.log_reader import read_logs

    events = read_logs("data/raw/sample.log")

    findings = run_detectors(events)

    for finding in findings:
        print(finding)