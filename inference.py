"""
Baseline inference script for the Email Triage environment.

Uses the OpenAI client to talk to an LLM, triaging emails across 3 tasks.

Required environment variables:
  API_BASE_URL  — LLM API endpoint (e.g. https://api-inference.huggingface.co/v1/)
  MODEL_NAME    — Model identifier (e.g. meta-llama/Llama-3-8B-Instruct)
  HF_TOKEN      — Hugging Face / API key
"""

import json
import os
import sys
import time
from typing import Optional

import requests

from dotenv import load_dotenv
from openai import OpenAI

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import EmailTriageAction, EmailTriageObservation

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")

TASKS = ["basic_triage", "ambiguous_triage", "complex_triage"]

# The base URL of the running environment server
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:8000")


def build_prompt(obs: EmailTriageObservation) -> str:
    """Build the LLM prompt for a single email triage decision."""
    return f"""You are an expert email triage agent. Your job is to classify incoming emails.

For the email below, provide your classification in strict JSON format:
{{
    "category": "<one of: billing, technical, hr, sales, general>",
    "priority": "<one of: low, medium, high, critical>",
    "department": "<one of: engineering, finance, hr, sales, support>",
    "reasoning": "<brief explanation of your classification>"
}}

IMPORTANT: Return ONLY the JSON object. No extra text.

--- EMAIL ---
From: {obs.email_sender}
Subject: {obs.email_subject}

{obs.email_body}

Attachments: {json.dumps(obs.email_metadata)}
--- END EMAIL ---

Your classification (JSON only):"""


def parse_llm_response(response_text: str) -> Optional[EmailTriageAction]:
    """Parse the LLM's JSON response into an EmailTriageAction."""
    text = response_text.strip()
    # Try to find JSON in the response
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    # Find first { and last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start : end + 1]

    try:
        data = json.loads(text)
        return EmailTriageAction(
            category=data.get("category", "general").lower().strip(),
            priority=data.get("priority", "medium").lower().strip(),
            department=data.get("department", "support").lower().strip(),
            reasoning=data.get("reasoning", ""),
        )
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"  ⚠ Failed to parse LLM response: {e}")
        print(f"  Raw response: {response_text[:200]}")
        # Return a safe fallback
        return EmailTriageAction(
            category="general",
            priority="medium",
            department="support",
            reasoning="Failed to parse LLM response — using defaults.",
        )


def call_llm(prompt: str, client: OpenAI) -> str:
    """Call the LLM and return the response text."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert email triage classifier. "
                    "Always respond with valid JSON only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.1,
    )
    return response.choices[0].message.content or ""


def run_inference():
    """Run inference across all 3 tasks and report scores."""
    assert API_BASE_URL, "Set API_BASE_URL env var"
    assert MODEL_NAME, "Set MODEL_NAME env var"
    assert HF_TOKEN, "Set HF_TOKEN env var"

    llm_client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN,
    )

    results = {}
    total_start = time.time()

    for task_name in TASKS:
        print(f"\n{'='*60}")
        print(f"Task: {task_name}")
        print(f"{'='*60}")

        # Reset with task_name via HTTP

        reset_resp = requests.post(
            f"{ENV_BASE_URL}/reset",
            json={"task_name": task_name},
            timeout=30,
        )
        reset_resp.raise_for_status()
        reset_data = reset_resp.json()
        obs = EmailTriageObservation(
            done=reset_data.get("done", False),
            reward=reset_data.get("reward"),
            **reset_data.get("observation", {}),
        )

        step_num = 0
        while not obs.done:
            step_num += 1
            print(f"\n  📧 Email {step_num}: {obs.email_subject}")

            # Build prompt and call LLM
            prompt = build_prompt(obs)
            llm_response = call_llm(prompt, llm_client)
            action = parse_llm_response(llm_response)

            print(f"  🤖 → category={action.category}, priority={action.priority}, department={action.department}")

            # Step with action via direct HTTP (to pass action fields)
            step_resp = requests.post(
                f"{ENV_BASE_URL}/step",
                json={"action": {
                    "category": action.category,
                    "priority": action.priority,
                    "department": action.department,
                    "reasoning": action.reasoning,
                }},
                timeout=30,
            )
            step_resp.raise_for_status()
            step_data = step_resp.json()
            obs = EmailTriageObservation(
                done=step_data.get("done", False),
                reward=step_data.get("reward"),
                **step_data.get("observation", {}),
            )

            print(f"  📊 Feedback: {obs.feedback[:100]}")

        final_score = obs.reward if obs.reward is not None else obs.current_score
        results[task_name] = final_score
        print(f"\n  🏁 Final score for {task_name}: {final_score:.4f}")

    elapsed = time.time() - total_start

    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    for task, score in results.items():
        print(f"  {task:25s} → {score:.4f}")
    avg = sum(results.values()) / len(results) if results else 0
    print(f"  {'Average':25s} → {avg:.4f}")
    print(f"  Total time: {elapsed:.1f}s")
    print(f"{'='*60}")


if __name__ == "__main__":
    run_inference()
