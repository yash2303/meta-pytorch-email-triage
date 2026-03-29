"""Typed models for the Email Triage Agent environment."""

from typing import Dict, List, Any, Optional
from openenv.core.env_server import Action, Observation, State


class EmailTriageAction(Action):
    """Agent's triage decision for a single email."""
    category: str       # "billing", "technical", "hr", "sales", "general"
    priority: str       # "low", "medium", "high", "critical"
    department: str     # "engineering", "finance", "hr", "sales", "support"
    reasoning: str = "" # Agent's chain-of-thought explanation


class EmailTriageObservation(Observation):
    """What the agent sees — one email at a time plus feedback."""
    # Inherited: done (bool), reward (float|None), metadata (dict)
    email_subject: str = ""
    email_body: str = ""
    email_sender: str = ""
    email_metadata: Dict[str, Any] = {}
    task_name: str = ""
    task_difficulty: str = ""  # "easy", "medium", "hard"
    feedback: str = ""
    current_score: float = 0.0
    emails_remaining: int = 0


class EmailTriageState(State):
    """Episode tracking for the triage environment."""
    # Inherited: episode_id (str|None), step_count (int)
    task_name: str = ""
    total_emails: int = 0
    processed_emails: int = 0
    cumulative_score: float = 0.0
