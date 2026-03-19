# ---------------------------------------------
# conftest.py
# Shared test configuration for all test files
# ---------------------------------------------

import sys
import os

# Add project root to Python path
# This allows imports like "from main import app"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app


# ---------------------------------------------
# TEST CLIENT
# ---------------------------------------------
# This client simulates HTTP requests to the API

client = TestClient(app)