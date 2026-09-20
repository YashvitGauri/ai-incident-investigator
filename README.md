# AI Incident Investigator

An AI-assisted security incident investigation system that analyzes security logs, detects suspicious activity, correlates related findings into incidents, determines incident severity using deterministic application logic, and uses an agentic AI workflow to investigate incidents and produce structured investigation reports.

## Overview

Security logs often contain large amounts of low-level activity that require analysts to manually correlate before understanding what happened.

```text
Raw Security Logs
        ↓
      Parser
        ↓
 Structured Events
        ↓
    Detection
        ↓
     Findings
        ↓
    Correlation
        ↓
     Incident
        ↓
Deterministic Severity
        ↓
 Agentic Investigation
        ↓
      Gemini
        ↓
 Read-only Event Search
        ↓
 Investigation Report
        ↓
      FastAPI
        ↓
 React Frontend
```

The system intentionally separates deterministic security logic from AI reasoning. The application determines findings and severity, while the AI investigates evidence, explains possible causes, describes uncertainty, and recommends proportionate actions.

## Key Features

### Security Event Parsing

Converts raw log lines into structured events containing:

- Timestamp
- Log level
- Event type
- User
- IP address
- Additional metadata

### Suspicious Activity Detection

The current detection engine identifies:

- Suspicious authentication sequences
- Repeated failed login attempts followed by successful authentication
- Sensitive administrative API access

### Incident Correlation

Related findings are grouped into incidents using:

- User identity
- IP address
- Temporal proximity

The correlation logic avoids merging unrelated users simply because their events occurred close together.

### Deterministic Severity

Incident severity is calculated by application rules rather than by the LLM.

```text
Suspicious authentication
        +
Sensitive API access
        ↓
       High
```

This prevents the AI model from arbitrarily changing a security-critical classification.

### Agentic AI Investigation

The investigation uses a LangChain agent with Gemini.

The agent can decide when additional evidence is required and use a read-only event search tool before producing its final report.

```text
Incident Evidence
       ↓
   AI Investigator
       ↓
Need more evidence?
   ↙           ↘
 Yes            No
  ↓              ↓
Search Events   Final Report
  ↓
Additional Evidence
  ↓
Further Reasoning
```

### Evidence-Aware AI

The workflow distinguishes between:

- Observed evidence
- Analysis
- Possible explanations
- Uncertainty
- Recommended actions

The AI is instructed not to invent missing information or treat assumptions as facts.

### Structured Investigation Reports

AI output is validated against a Pydantic schema before being returned by the API.

Reports contain:

- Summary
- Severity
- Observed evidence
- Analysis
- Possible explanations
- Confidence
- Recommended actions
- Uncertainty

### Log File Upload

The frontend supports uploading `.log` and `.txt` files and sending their contents to the investigation API.

### REST API

FastAPI exposes the investigation functionality through a simple HTTP API.

## Architecture

### Backend

```text
backend/
├── app/
│   ├── ai/
│   │   ├── agent.py
│   │   └── investigator.py
│   ├── api/
│   │   └── main.py
│   ├── detectors/
│   │   ├── authentication.py
│   │   ├── api_abuse.py
│   │   └── engine.py
│   ├── tools/
│   │   └── event_search.py
│   ├── correlator.py
│   ├── log_reader.py
│   ├── models.py
│   ├── parser.py
│   ├── pipeline.py
│   └── severity.py
├── tests/
└── data/
    └── raw/
```

### Frontend

```text
frontend/
└── src/
    ├── components/
    │   ├── layout/
    │   ├── investigation/
    │   └── incidents/
    ├── services/
    │   └── api.js
    ├── App.jsx
    └── main.jsx
```

## Security Design Principles

### 1. Severity is not controlled by the LLM

The application calculates severity before the AI investigation begins. The AI receives that severity as authoritative.

### 2. Logs are treated as untrusted data

Log contents can contain arbitrary usernames, endpoints, metadata, or other strings. Event data is treated as evidence, not as instructions.

### 3. Missing information remains unknown

For example:

```text
IP address: not recorded
```

does not become:

```text
IP address: same as previous login
```

### 4. Evidence is traceable

Investigation reports preserve individual observed events wherever possible so conclusions can be traced back to the underlying evidence.

### 5. Recommendations account for uncertainty

When evidence cannot establish whether an action was authorized or whether an account was compromised, the AI is instructed to recommend verification and further investigation rather than presenting assumptions as facts.

## Example Investigation

Example input:

```text
2026-09-18 14:03:12 INFO Login failed user=alice ip=192.168.1.20
2026-09-18 14:03:14 INFO Login failed user=alice ip=192.168.1.20
2026-09-18 14:03:16 INFO Login failed user=alice ip=192.168.1.20
2026-09-18 14:04:01 INFO Login successful user=alice ip=192.168.1.20
2026-09-18 14:04:13 INFO API request user=alice endpoint=/admin/users
```

The system detects a suspicious authentication sequence combined with sensitive API access and assigns the incident a deterministic **High** severity.

The AI then investigates the evidence and produces a structured report while preserving uncertainty around information that is not present in the logs.

## Test Scenarios

| Scenario | Purpose |
|---|---|
| `scenario_01_bruteforce.log` | Suspicious authentication sequence |
| `scenario_02_sensitive_access.log` | Sensitive administrative API access |
| `scenario_03_benign_login.log` | Benign activity / false-positive validation |
| `scenario_04_multiple_incidents.log` | Multiple users and incident correlation |
| `scenario_05_incomplete_logs.log` | Missing identity and IP information |

These scenarios were also verified through the actual FastAPI `/investigate` endpoint.

Current validation includes:

- 18 automated tests passing
- Benign activity producing no incidents
- Multiple incidents remaining correctly separated
- Deterministic severity
- Missing fields remaining unknown
- AI investigation producing structured reports

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- LangChain
- LangChain Google GenAI
- Gemini

### Frontend

- React
- Vite
- Tailwind CSS

### Testing

- Pytest

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/YashvitGauri/ai-incident-investigator.git
cd ai-incident-investigator
```

### 2. Create the Python environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Configure Gemini

Create:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit `.env` to Git.

### 4. Start the backend

From the project root:

```bash
uvicorn app.api.main:app --reload --app-dir backend
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "ok"
}
```

### 5. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

## API

### Health Check

```http
GET /health
```

### Investigate Logs

```http
POST /investigate
```

Request:

```json
{
  "log_text": "2026-09-18 14:03:12 INFO Login failed user=alice ip=192.168.1.20"
}
```

Response:

```json
{
  "incidents": [
    {
      "incident_id": "INC-0001",
      "title": "Suspicious authentication activity",
      "severity": "Medium",
      "summary": "...",
      "observed_evidence": [],
      "analysis": "...",
      "possible_explanations": [],
      "confidence": "Medium",
      "recommended_actions": [],
      "uncertainty": "..."
    }
  ]
}
```

## Testing

Run the complete automated test suite:

```bash
pytest
```

Current test suite:

```text
18 passed
```

The project also contains five realistic log scenarios for end-to-end validation.

## Engineering Decisions

### Why deterministic severity?

Severity can influence operational response, so it should not depend on probabilistic LLM output. The application therefore determines severity using explicit rules.

### Why use an agent?

A fixed prompt-response pipeline would require providing every available event to the model. The agent can instead decide when additional evidence is useful and retrieve relevant events through a controlled read-only tool.

### Why not use a vector database?

The current problem does not require semantic retrieval over a large historical dataset. The event search tool is intentionally simple and deterministic.

### Why not use multiple AI agents?

The current investigation workflow does not require multiple independent reasoning agents. A single investigator with controlled evidence retrieval is sufficient for the current scope.

## Current Limitations

- Log parsing currently supports a limited log format.
- Detection rules cover a limited set of suspicious behaviors.
- Event search operates over events loaded for the investigation.
- Gemini is currently the AI provider.
- Authentication and multi-user access control are not implemented.
- The system is not intended to replace a production SIEM or SOC platform.

## Future Improvements

Potential future extensions include:

- Additional detection rules
- Support for more log formats
- Historical event storage
- More advanced event correlation
- Authentication and role-based access control
- Additional investigation tools
- Streaming investigation updates
- Cloud deployment
- Additional AI model providers

These are intentionally outside the current v1 scope.

## Project Status

**v1 — Core implementation complete**

The current version includes:

- Structured log parsing
- Security detections
- Incident correlation
- Deterministic severity
- Agentic AI investigation
- Read-only evidence search
- Structured investigation reports
- FastAPI backend
- React frontend
- Log file upload
- Automated tests
- End-to-end scenario validation

## Author

Built as a hands-on security engineering and AI systems project, with emphasis on understanding the architecture, implementation decisions, testing, and boundaries between deterministic security logic and AI-assisted reasoning.
