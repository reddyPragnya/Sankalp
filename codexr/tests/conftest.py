import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def load_env():
    """
    Automatically load environment variables from .env for all tests.
    Runs once per test session.
    """
    load_dotenv()
    return os.environ

@pytest.fixture
def sample_query():
    """
    Provide a reusable sample AR/VR developer query for tests.
    """
    return "How do I add teleport locomotion in Unity VR?"

@pytest.fixture
def dummy_response():
    """
    Provide a reusable dummy JSON response in the required format.
    """
    return {
        "platform": "Unity",
        "topic": "Teleport locomotion",
        "steps": [
            "Install XR Interaction Toolkit",
            "Add Teleportation Area",
            "Configure Teleportation Provider"
        ],
        "code_snippet": "C# code snippet here",
        "gotchas": ["Ensure XR Rig prefab is set"],
        "difficulty": "Medium",
        "docs_link": "https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit"
    }
