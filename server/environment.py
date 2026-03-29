"""Email Triage Agent — OpenEnv Environment implementation."""

import uuid
from typing import Any, Optional

from openenv.core.env_server import Environment

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import EmailTriageAction, EmailTriageObservation, EmailTriageState
from server.email_data import (
    TASKS,
    PRIORITY_ORDER,
    VALID_CATEGORIES,
    VALID_PRIORITIES,
    VALID_DEPARTMENTS,
    EmailSample,
)


class EmailTriageEnvironment(Environment):
    """
    An RL environment where an AI agent triages emails by classifying
    category, priority, and department. Supports 3 tasks (easy/medium/hard).
    """

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._state = EmailTriageState()
        self._task_name = ""
        self._emails = []
        self._current_idx = 0
        self._scores = []

    def reset(
        self,
        seed: Optional[int] = None,
        task_name: str = "basic_triage",
        **kwargs: Any,
    ) -> EmailTriageObservation:
        """Reset the environment and present the first email for the given task."""
        if task_name not in TASKS:
            raise ValueError(
                f"Unknown task '{task_name}'. Choose from: {list(TASKS.keys())}"
            )

        task = TASKS[task_name]
        self._task_name = task_name
        self._emails = task["emails"]
        self._current_idx = 0
        self._scores = []

        self._state = EmailTriageState(
            episode_id=str(uuid.uuid4()),
            step_count=0,
            task_name=task_name,
            total_emails=len(self._emails),
            processed_emails=0,
            cumulative_score=0.0,
        )

        email = self._emails[0]
        return EmailTriageObservation(
            done=False,
            reward=None,
            email_subject=email.subject,
            email_body=email.body,
            email_sender=email.sender,
            email_metadata=email.metadata,
            task_name=task_name,
            task_difficulty=task["difficulty"],
            feedback="New episode started. Triage the email below.",
            current_score=0.0,
            emails_remaining=len(self._emails) - 1,
        )

    def step(
        self,
        action: EmailTriageAction,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> EmailTriageObservation:
        """Grade the agent's triage decision and return the next email (or end)."""
        email = self._emails[self._current_idx]
        score, feedback = self._grade(action, email)
        self._scores.append(score)

        self._state.step_count += 1
        self._state.processed_emails += 1
        self._state.cumulative_score = sum(self._scores) / len(self._scores)

        self._current_idx += 1
        done = self._current_idx >= len(self._emails)

        if done:
            final_score = sum(self._scores) / len(self._scores)
            return EmailTriageObservation(
                done=True,
                reward=round(final_score, 4),
                email_subject="",
                email_body="",
                email_sender="",
                email_metadata={},
                task_name=self._task_name,
                task_difficulty=TASKS[self._task_name]["difficulty"],
                feedback=(
                    f"Episode complete! Final score: {final_score:.2%}\n"
                    f"Last email feedback: {feedback}"
                ),
                current_score=round(final_score, 4),
                emails_remaining=0,
            )

        # Present next email
        next_email = self._emails[self._current_idx]
        running_avg = sum(self._scores) / len(self._scores)
        return EmailTriageObservation(
            done=False,
            reward=round(score, 4),
            email_subject=next_email.subject,
            email_body=next_email.body,
            email_sender=next_email.sender,
            email_metadata=next_email.metadata,
            task_name=self._task_name,
            task_difficulty=TASKS[self._task_name]["difficulty"],
            feedback=feedback,
            current_score=round(running_avg, 4),
            emails_remaining=len(self._emails) - self._current_idx - 1,
        )

    @property
    def state(self) -> EmailTriageState:
        return self._state

    # ------------------------------------------------------------------
    # Grading logic
    # ------------------------------------------------------------------
    def _grade(self, action: EmailTriageAction, email: EmailSample) -> tuple:
        """
        Compute a score in [0.0, 1.0] for the agent's triage decision.

        Weights:
          - category:   0.40
          - priority:   0.30
          - department: 0.30

        Partial credit for priority: adjacent levels get 0.5 credit.
        """
        details = []
        score = 0.0

        # --- Category (exact match, 0.4 weight) ---
        pred_cat = action.category.lower().strip()
        if pred_cat == email.category:
            score += 0.4
            details.append(f"✅ Category '{pred_cat}' correct (+0.40)")
        else:
            details.append(
                f"❌ Category '{pred_cat}' incorrect (expected '{email.category}', +0.00)"
            )

        # --- Priority (partial credit, 0.3 weight) ---
        pred_pri = action.priority.lower().strip()
        if pred_pri == email.priority:
            score += 0.3
            details.append(f"✅ Priority '{pred_pri}' correct (+0.30)")
        elif pred_pri in VALID_PRIORITIES and email.priority in VALID_PRIORITIES:
            dist = abs(
                PRIORITY_ORDER.index(pred_pri) - PRIORITY_ORDER.index(email.priority)
            )
            if dist == 1:
                score += 0.15  # half credit for adjacent
                details.append(
                    f"⚠️ Priority '{pred_pri}' close (expected '{email.priority}', +0.15)"
                )
            else:
                details.append(
                    f"❌ Priority '{pred_pri}' incorrect (expected '{email.priority}', +0.00)"
                )
        else:
            details.append(
                f"❌ Priority '{pred_pri}' invalid (expected '{email.priority}', +0.00)"
            )

        # --- Department (exact match, 0.3 weight) ---
        pred_dept = action.department.lower().strip()
        if pred_dept == email.department:
            score += 0.3
            details.append(f"✅ Department '{pred_dept}' correct (+0.30)")
        else:
            details.append(
                f"❌ Department '{pred_dept}' incorrect (expected '{email.department}', +0.00)"
            )

        feedback = f"Score: {score:.2f}/1.00 | " + " | ".join(details)
        return score, feedback
