import mock

from datetime import datetime, timedelta

from selvpcclient.httpclient import HTTPClient, RegionalHTTPClient


x_token = "aaaaaaaaaaaaaaaaaaaaaaaaa_000000"

client = HTTPClient(base_url="http://api/v2", headers={"X-Token": x_token})
regional_client = RegionalHTTPClient(client, "http://identity/v3")


class KeystoneTokenInfoMock:
    def __init__(self):
        self.expires = datetime.now() + timedelta(hours=24)

        self.service_catalog = mock.Mock()
        self.service_catalog.url_for = mock.Mock(
            return_value="http://ru-1.api")
