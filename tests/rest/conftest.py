import pytest


@pytest.fixture(autouse=True)
def set_envs(monkeypatch):
    monkeypatch.setenv("SEL_URL", "http://api")
