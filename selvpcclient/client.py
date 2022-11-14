import os

from selvpcclient import __version__
from selvpcclient.httpclient import HTTPClient, RegionalHTTPClient
from selvpcclient.resources.capabilities import CapabilitiesManager
from selvpcclient.resources.customization import CustomizationManager
from selvpcclient.resources.floatingips import FloatingIPManager
from selvpcclient.resources.keypairs import KeyPairManager
from selvpcclient.resources.licenses import LicenseManager
from selvpcclient.resources.projects import ProjectsManager
from selvpcclient.resources.quotas import QuotasManager
from selvpcclient.resources.roles import RolesManager
from selvpcclient.resources.subnets import SubnetManager
from selvpcclient.resources.tokens import TokensManager
from selvpcclient.resources.users import UsersManager
from selvpcclient.resources.vrrp import VRRPManager


def setup_http_client(api_url, api_token=None, api_version=2,
                      custom_headers=None, timeout=60):
    """Initialize a new HTTPClient by provided arguments.

    :param string api_url: A user-supplied endpoint URL for the service.
    :param string api_token: Selectel VPC API token.
    :param string api_version: Selectel VPC API version. (default 2)
    :param dict custom_headers: Custom headers for each request. (optional)
    :param int timeout: Custom timeout value for requests. (default 60 seconds)
    :rtype: :class:`HTTPClient`
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'python-selvpcclient/{}'.format(__version__),
    }
    if api_token:
        headers["X-Token"] = api_token

    if custom_headers:
        headers.update(custom_headers)
    url = "{}/v{}".format(api_url.rstrip('/'), api_version)
    return HTTPClient(base_url=url, headers=headers, timeout=timeout)


class Client:
    """Client for the Selectel VPC API."""

    def __init__(
        self,
        client: HTTPClient,
        regional_client: RegionalHTTPClient = None
    ):
        if not regional_client:
            regional_client = RegionalHTTPClient(
                http_client=client,
                identity_url=os.environ.get(
                    'OS_AUTH_URL', 'https://api.selvpc.ru/identity/v3'
                )
            )

        self.projects = ProjectsManager(client, regional_client)
        self.quotas = QuotasManager(regional_client)
        self.users = UsersManager(client)
        self.licenses = LicenseManager(client)
        self.roles = RolesManager(client)
        self.floatingips = FloatingIPManager(client)
        self.subnets = SubnetManager(client)
        self.vrrp = VRRPManager(client)
        self.capabilities = CapabilitiesManager(client)
        self.tokens = TokensManager(client)
        self.customization = CustomizationManager(client)
        self.keypairs = KeyPairManager(client)
