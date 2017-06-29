from _pytest.monkeypatch import monkeypatch

from selvpcclient.httpclient import HTTPClient

monkeypatch().setenv("SEL_URL", "http://api")
client = HTTPClient(base_url="http://api/v2", headers={})