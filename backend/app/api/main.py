from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from app.pipeline import investigate_log_text


app = FastAPI(
    title="AI Incident Investigator",
    description="AI-assisted security incident investigation API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvestigationRequest(BaseModel):
    log_text: str


class IncidentReport(BaseModel):
    incident_id: str
    title: str
    severity: str
    summary: str
    observed_evidence: list[str]
    analysis: str
    possible_explanations: list[str]
    confidence: str
    recommended_actions: list[str]
    uncertainty: str


class InvestigationResponse(BaseModel):
    incidents: list[IncidentReport]


def get_incident_title(incident) -> str:
    finding_types = {finding.type for finding in incident.findings}

    if (
        "suspicious_login_sequence" in finding_types
        and "sensitive_api_access" in finding_types
    ):
        return "Suspicious authentication + sensitive API access"

    if "suspicious_login_sequence" in finding_types:
        return "Suspicious authentication activity"

    if "sensitive_api_access" in finding_types:
        return "Sensitive API access"

    return "Security activity requiring investigation"


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/investigate", response_model=InvestigationResponse)
def investigate(request: InvestigationRequest):
    reports = investigate_log_text(request.log_text)

    incidents = [
        IncidentReport(
            incident_id=incident.id,
            title=get_incident_title(incident),
            severity=report.severity,
            summary=report.summary,
            observed_evidence=report.observed_evidence,
            analysis=report.analysis,
            possible_explanations=report.possible_explanations,
            confidence=report.confidence,
            recommended_actions=report.recommended_actions,
            uncertainty=report.uncertainty,
        )
        for incident, report in reports
    ]

    return InvestigationResponse(incidents=incidents)