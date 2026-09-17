from app.correlator import correlate_findings
from app.detectors.engine import run_detectors
from app.ai.agent import investigate_with_agent
from app.log_reader import read_logs


events = read_logs("data/raw/sample.log")
findings = run_detectors(events)
incidents = correlate_findings(findings)


for incident in incidents:
    print(f"\n=== INVESTIGATION {incident.id} ===\n")

    report = investigate_with_agent(
        incident,
        events,
    )

    print(f"Summary:\n{report.summary}\n")

    print(f"Severity:\n{report.severity}\n")

    print("Observed Evidence:")
    for evidence in report.observed_evidence:
        print(f"- {evidence}")

    print(f"\nAnalysis:\n{report.analysis}\n")

    print("Possible Explanations:")
    for explanation in report.possible_explanations:
        print(f"- {explanation}")

    print(f"\nConfidence:\n{report.confidence}\n")

    print("Recommended Actions:")
    for action in report.recommended_actions:
        print(f"- {action}")

    print(f"\nUncertainty:\n{report.uncertainty}")