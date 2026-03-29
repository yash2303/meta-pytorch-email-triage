"""FastAPI application for the Email Triage environment."""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openenv.core.env_server import create_fastapi_app
from models import EmailTriageAction, EmailTriageObservation
from server.environment import EmailTriageEnvironment

# create_fastapi_app expects a callable factory that returns an Environment.
# The HTTP server calls this factory for EVERY request (reset, step, state).
# We need all requests to share the same instance so that step() sees the
# state set by reset(). Solution: create one instance and always return it.
_shared_env = EmailTriageEnvironment()

app = create_fastapi_app(
    lambda: _shared_env,          # Always return the same instance
    EmailTriageAction,
    EmailTriageObservation,
)
