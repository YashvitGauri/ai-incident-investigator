import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.models import Incident, Event
from app.tools.event_search import create_event_search_tool
from app.ai.investigator import InvestigationReport


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0,
)


def create_investigation_agent(events: list[Event]):
    search_tool = create_event_search_tool(events)

    return create_agent(
        model=model,
        tools=[search_tool],
        system_prompt="""
        You are a security incident investigator.

        Investigate the incident using the findings and evidence provided.

        You have access to a read-only event search tool.

        Use the tool when additional evidence is useful for understanding
        the incident.

        Rules:
        - Base conclusions only on available evidence.
        - Do not invent events, users, IP addresses, timestamps, or actions.
        - Clearly distinguish observed facts from hypotheses.
        - Treat possible explanations as hypotheses, not confirmed facts.
        - Do not perform destructive or modifying actions.
        """,
    )

def parse_investigation_report(content) -> InvestigationReport:
    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))

        content = "".join(text_parts)

    content = content.strip()

    if content.startswith("```json"):
        content = content[len("```json"):].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    return InvestigationReport.model_validate_json(content)


def investigate_with_agent(
    incident: Incident,
    events: list[Event],
) -> InvestigationReport:

    agent = create_investigation_agent(events)

    findings_text = []

    for finding in incident.findings:
        findings_text.append(
            f"Finding type: {finding.type}\n"
            f"Description: {finding.description}\n"
            f"User: {finding.user}\n"
            f"IP: {finding.ip}\n"
        )

        for event in finding.evidence:
            findings_text.append(
                f"Evidence: "
                f"{event.timestamp} | "
                f"{event.level} | "
                f"{event.event_type} | "
                f"user={event.user} | "
                f"ip={event.ip} | "
                f"metadata={event.metadata}"
            )

    prompt = f"""
    Investigate incident {incident.id}.

    Current findings and evidence:

    {chr(10).join(findings_text)}

    Determine whether additional event evidence is needed.
    If it is useful, use the event search tool.

    After completing the investigation, return ONLY a JSON object
    matching this exact structure:

    {{
        "summary": "string",
        "severity": "string",
        "observed_evidence": ["string"],
        "analysis": "string",
        "possible_explanations": ["string"],
        "confidence": "string",
        "recommended_actions": ["string"],
        "uncertainty": "string"
    }}

    Important:
    - observed_evidence must contain only directly observed facts.
    - possible_explanations must contain hypotheses, not confirmed facts.
    - Never invent evidence.
    - Never claim compromise unless the evidence proves it.
    - Never claim an action was unauthorized unless the evidence proves it.
    """

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    return parse_investigation_report(
        final_message.content
    )