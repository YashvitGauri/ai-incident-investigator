from dataclasses import dataclass, field


@dataclass
class Event:
    timestamp: str
    level: str
    event_type: str
    user: str | None = None
    ip: str | None = None
    metadata: dict = field(default_factory=dict)

@dataclass
class Finding:
    type: str
    user: str | None = None
    ip: str | None = None
    description: str = ""
    evidence: list[Event] = field(default_factory=list)

@dataclass
class Incident:
    id: str
    findings: list[Finding] = field(default_factory=list)
    severity: str = "Low"