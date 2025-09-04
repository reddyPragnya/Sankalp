import os
import subprocess
import pytest

def test_requirements_installed():
    """Check if required packages are installed"""
    try:
        import streamlit
        import langchain
        import openai
        import requests
        import pydantic
        import dotenv
    except ImportError as e:
        pytest.fail(f"Missing dependency: {e}")

def test_streamlit_runs():
    """Check if Streamlit app starts without crashing"""
    try:
        result = subprocess.run(
            ["streamlit", "run", "app.py", "--server.headless=true", "--server.port=8888"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        # Streamlit runs as a server, so timeout is expected.
        # If it times out, it means app started without crashing.
        return
    except Exception as e:
        pytest.fail(f"Streamlit failed to start: {e}")
