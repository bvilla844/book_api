from src.db.main import get_session
from src import app
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock
import pytest

mock_session = Mock()
mock_user_service = Mock()

def get_mock_session():
    yield mock_session

# Sobrescribir dependencias
app.dependency_overrides[get_session] = get_mock_session

@pytest.fixture
def fake_session():
    return mock_session

@pytest.fixture
def fake_user_service():
    return mock_user_service

@pytest.fixture
def test_client():
    return TestClient(app)
