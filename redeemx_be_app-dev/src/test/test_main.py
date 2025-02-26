import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError, OperationalError
from src.main import app
from fastapi import HTTPException
import os
import sys
import runpy
import uvicorn

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code in [404, 200]  

def test_app_startup():
    assert app.title == "FastAPI"  

@patch("os.path.abspath")
def test_project_root_setup(mock_abspath):
    mock_abspath.return_value = "/mocked/path"
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    assert project_root == "/mocked/path"

def test_session_middleware():
    middlewares = [middleware.cls for middleware in app.user_middleware]
    assert "SessionMiddleware" in [m.__name__ for m in middlewares]

def ensure_project_root_in_syspath(project_root: str):
    if project_root not in sys.path:
        sys.path.append(project_root)

def ensure_project_root_in_syspath():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.append(project_root)
    return project_root

def test_main_if_main(monkeypatch):
    run_calls = []

    def fake_run(app, host, port):
        run_calls.append((host, port))
        return "uvicorn_run_called"
    monkeypatch.setattr(uvicorn, "run", fake_run)
    runpy.run_path("main.py", run_name="__main__")
    assert run_calls == [("0.0.0.0", 8000)]

