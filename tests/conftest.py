"""
conftest.py

This file sets up the test environment.
It also ensures Python can find the 'app' module.
"""
# to run teh test 
#     pytest
# to run the tests coverge 
#    pytest --cov=app



import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

# Create a test client
client = TestClient(app)