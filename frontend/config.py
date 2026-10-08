import os
from uuid import uuid4

# ------------------------------------------------------------------
# Backend
# ------------------------------------------------------------------

BACKEND_URL = os.getenv(
	"BACKEND_URL",
	"http://127.0.0.1:8000/chat",
)

# ------------------------------------------------------------------
# Demo Customer
# ------------------------------------------------------------------

CUSTOMER_ID = "55b62f9d-e541-4397-851f-4a5428c8ae7e"

# ------------------------------------------------------------------
# Conversation Session
# ------------------------------------------------------------------
# A new session is generated every time the frontend starts.
# This allows each demo to begin with a fresh conversation.

SESSION_ID = str(uuid4())