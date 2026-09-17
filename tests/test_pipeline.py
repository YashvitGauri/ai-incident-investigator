from app.pipeline import investigate_log_file


def test_investigate_log_file(monkeypatch):
    def fake_investigate(incident):
        return {
            "incident_id": incident.id,
            "finding_count": len(incident.findings),
        }

    monkeypatch.setattr(
        "app.pipeline.investigate",
        fake_investigate,
    )

    reports = investigate_log_file(
        "data/raw/sample.log"
    )

    assert len(reports) == 1

    incident, report = reports[0]

    assert incident.id == "INC-0001"
    assert len(incident.findings) == 2
    assert report["incident_id"] == "INC-0001"