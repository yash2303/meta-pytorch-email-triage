"""HTTP client for the Email Triage environment."""

from typing import Any, Optional
from openenv.core.env_client import EnvClient
from openenv.core.client_types import StepResult
from models import EmailTriageAction, EmailTriageObservation, EmailTriageState


class EmailTriageEnv(EnvClient[EmailTriageAction, EmailTriageObservation, EmailTriageState]):
    """Client for the Email Triage environment server (WebSocket-based)."""

    def _step_payload(self, action: EmailTriageAction) -> dict:
        return {
            "category": action.category,
            "priority": action.priority,
            "department": action.department,
            "reasoning": action.reasoning,
        }

    def _parse_result(self, payload: dict) -> StepResult[EmailTriageObservation]:
        obs_data = payload.get("observation", {})
        return StepResult(
            observation=EmailTriageObservation(
                done=payload.get("done", False),
                reward=payload.get("reward"),
                email_subject=obs_data.get("email_subject", ""),
                email_body=obs_data.get("email_body", ""),
                email_sender=obs_data.get("email_sender", ""),
                email_metadata=obs_data.get("email_metadata", {}),
                task_name=obs_data.get("task_name", ""),
                task_difficulty=obs_data.get("task_difficulty", ""),
                feedback=obs_data.get("feedback", ""),
                current_score=obs_data.get("current_score", 0.0),
                emails_remaining=obs_data.get("emails_remaining", 0),
            ),
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: dict) -> EmailTriageState:
        return EmailTriageState(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
            task_name=payload.get("task_name", ""),
            total_emails=payload.get("total_emails", 0),
            processed_emails=payload.get("processed_emails", 0),
            cumulative_score=payload.get("cumulative_score", 0.0),
        )
