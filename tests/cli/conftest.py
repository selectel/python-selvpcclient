import pytest


@pytest.fixture(autouse=True)
def set_envs(monkeypatch):
    monkeypatch.setenv("SEL_URL", "http://selvpcapi")
    monkeypatch.setenv("SEL_TOKEN", "5ba50055-ff2e-4145-a8cf-f03e9fbd5ee6")
