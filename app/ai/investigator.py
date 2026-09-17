import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

from app.models import Incident


class InvestigationReport(BaseModel):
    summary: str
    severity: str
    observed_evidence: list[str]
    analysis: str
    possible_explanations: list[str]
    confidence: str
    recommended_actions: list[str]
    uncertainty: str


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


def investigate(
    incident: Incident,
    client=client,
) -> InvestigationReport:

    evidence_text = []

    for finding in incident.findings:
        evidence_text.append(
            f"Finding type: {finding.type}\n"
            f"Description: {finding.description}\n"
            f"User: {finding.user}\n"
            f"IP: {finding.ip}\n"
        )

        for event in finding.evidence:
            evidence_text.append(
                f"Evidence event: "
                f"{event.timestamp} | "
                f"{event.level} | "
                f"{event.event_type} | "
                f"user={event.user} | "
                f"ip={event.ip} | "
                f"metadata={event.metadata}\n"
            )

    prompt = f"""
    You are a security incident investigator.

    Investigate incident {incident.id} using only the findings and evidence
    provided below.

    Produce a structured investigation report.

    Follow these rules strictly:

    1. observed_evidence:
    Include only facts directly supported by the provided evidence.

    2. analysis:
    Correlate the findings and explain what the observed sequence means.

    3. possible_explanations:
    List plausible explanations for the observed behavior.
    These are hypotheses, not confirmed facts.

    4. confidence:
    Reflect how strongly the provided evidence supports the analysis.

    5. recommended_actions:
    Recommend investigation or containment steps that would help validate
    the hypotheses or respond to the incident.

    6. uncertainty:
    Explicitly identify information that is missing or cannot be determined.

    Important:
    - Never invent events, users, IP addresses, timestamps, or actions.
    - Never claim an account was compromised unless the evidence proves it.
    - Never claim an action was unauthorized unless the evidence proves it.
    - Never present a hypothesis as a confirmed fact.
    - Use only the supplied findings and evidence.

    Security findings and evidence:

    {chr(10).join(evidence_text)}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": InvestigationReport,
        },
    )

    return response.parsed