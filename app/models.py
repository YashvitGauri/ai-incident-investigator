from dataclasses import dataclass, field


@dataclass
class Event:
    timestamp: str
    level: str
    event_type: str
    user: str | None = None
    ip: str | None = None
    metadata: dict = field(default_factory=dict)