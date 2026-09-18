from langchain_core.tools import tool

from app.models import Event


def create_event_search_tool(events: list[Event]):
    @tool
    def search_events(
        user: str | None = None,
        ip: str | None = None,
    ) -> list[str]:
        """
        Search parsed security events by user or IP address.

        Use this tool when additional event evidence is needed.
        """

        results = []

        for event in events:
            if user is not None and event.user != user:
                continue

            if ip is not None and event.ip != ip:
                continue

            results.append(
                f"{event.timestamp} | "
                f"{event.level} | "
                f"{event.event_type} | "
                f"user={event.user} | "
                f"ip={event.ip} | "
                f"metadata={event.metadata}"
            )

        search_scope = []

        if user is not None:
            search_scope.append(f"user={user}")

        if ip is not None:
            search_scope.append(f"ip={ip}")

        scope = ", ".join(search_scope) if search_scope else "all events"

        return [
            f"Search scope: {scope}",
            f"Matching events: {len(results)}",
            "Events:",
            *results,
        ]

    return search_events