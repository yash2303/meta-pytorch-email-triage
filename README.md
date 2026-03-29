---
title: Email Triage Agent
emoji: 📧
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000
---
# Email Triage Agent — OpenEnv Environment

An RL environment where an AI agent learns to **triage incoming emails** — classifying category, priority, and routing to the correct department.

Built with the [OpenEnv](https://github.com/meta-pytorch/OpenEnv) framework for the Meta PyTorch Hackathon.

## Environment Description

The agent receives emails one at a time and must classify each by:
- **Category**: `billing`, `technical`, `hr`, `sales`, `general`
- **Priority**: `low`, `medium`, `high`, `critical`
- **Department**: `engineering`, `finance`, `hr`, `sales`, `support`

### Tasks

| Task | Difficulty | Description | Emails |
|------|-----------|-------------|--------|
| `basic_triage` | Easy | Clear-cut emails with obvious classifications | 5 |
| `ambiguous_triage` | Medium | Emails requiring inference and reading between the lines | 5 |
| `complex_triage` | Hard | Multi-topic emails, edge cases, urgency buried in context | 5 |

### Reward Function

Each email is scored 0.0–1.0 using weighted components:
- **Category match**: 0.40 weight (exact match)
- **Priority match**: 0.30 weight (exact match; partial credit 0.15 for adjacent levels)
- **Department match**: 0.30 weight (exact match)

Final task score = average across all emails → **0.0–1.0 range**.

## Action / Observation Spaces

**Action** (`EmailTriageAction`):
```python
category: str    # one of: billing, technical, hr, sales, general
priority: str    # one of: low, medium, high, critical
department: str  # one of: engineering, finance, hr, sales, support
reasoning: str   # agent's explanation
```

**Observation** (`EmailTriageObservation`):
```python
email_subject: str
email_body: str
email_sender: str
email_metadata: dict    # e.g., {"has_attachment": true, "attachment_name": "..."}
task_name: str
task_difficulty: str    # easy / medium / hard
feedback: str           # grader feedback after each step
current_score: float
emails_remaining: int
done: bool
reward: float | None
```

## Setup

### Prerequisites
- Python 3.10+
- Docker (for containerized deployment)

### Install
```bash
# Create venv
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r server/requirements.txt
```

### Run Locally
```bash
# Start the environment server
source venv/bin/activate
uvicorn server.app:app --host 0.0.0.0 --port 8000

# Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/reset -H "Content-Type: application/json" -d '{"task_name": "basic_triage"}'
```

### Run Inference
```bash
# Set up environment variables
cp .env.example .env
# Edit .env with your API credentials

source venv/bin/activate
python inference.py
```

### Docker
```bash
docker build -t email-triage-env .
docker run -p 8000:8000 email-triage-env
```

### Deploy to Hugging Face Spaces
```bash
openenv push --repo-id your-username/email-triage-env
```

## Project Structure

```
├── models.py              ← Action, Observation, State types
├── client.py              ← HTTP client (what users import)
├── inference.py           ← Baseline inference with OpenAI client
├── openenv.yaml           ← Environment manifest
├── pyproject.toml         ← Package metadata
├── __init__.py            ← Package exports
├── .env.example           ← Example env vars
└── server/
    ├── environment.py     ← Triage logic (reset, step, state)
    ├── app.py             ← FastAPI server
    ├── email_data.py      ← Email datasets + ground truth
    ├── requirements.txt   ← Server dependencies
    └── Dockerfile         ← Container definition
```

## Environment Variables

| Variable | Description | Example |
|----------|------------|---------|
| `API_BASE_URL` | LLM API endpoint | `https://api-inference.huggingface.co/v1/` |
| `MODEL_NAME` | Model identifier | `meta-llama/Llama-3-8B-Instruct` |
| `HF_TOKEN` | Hugging Face API key | `hf_...` |
| `ENV_BASE_URL` | Running environment URL | `http://localhost:8000` |
