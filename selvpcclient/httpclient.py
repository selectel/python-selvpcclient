import copy
import logging
from dataclasses import dataclass
from datetime import datetime as dt
from datetime import timedelta
from typing import Dict, Optional

import requests
from keystoneauth1.session import Session as KeystoneSession
from keystoneauth1.token_endpoint import Token as KeystoneToken
from keystoneclient.v3.client import Client as KeystoneClient
from requests import Response as Resp

from selvpcclient.exceptions.base import ClientException
from selvpcclient.exceptions.http import get_http_exception
from selvpcclient.util import make_curl
from selvpcclient.util import unserialize_quota_error
from selvpcclient.util import update_json_error_message

logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, base_url: str, headers: Dict[str, str],
                 timeout: int = 60):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def request(self, method: str, url: str, **kwargs) -> Resp:
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        kwargs.update(headers=self.headers)
        logger.debug("REQ: %s" % make_curl(url, method, copy.deepcopy(kwargs)))
        response = None
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.Timeout as err:
            raise err
        except requests.exceptions.MissingSchema as err:
            raise err
        except requests.exceptions.ConnectionError as err:
            raise err
        except requests.exceptions.RequestException:
            raise ClientException(
                status_code=response.status_code,
                message=get_http_exception(
                    status_code=response.status_code,
                    content=update_json_error_message(response.text))
            )
        logger.debug("RESP: %(code)s %(headers)s %(body)s",
                     {'code': response.status_code,
                      'headers': response.headers,
                      'body': response.text})
        return response

    def get(self, path: str, **kwargs) -> Resp:
        return self.request('GET', self.base_url + path, **kwargs)

    def post(self, path: str, **kwargs) -> Resp:
        return self.request('POST', self.base_url + path, **kwargs)

    def patch(self, path: str, **kwargs) -> Resp:
        return self.request('PATCH', self.base_url + path, **kwargs)

    def delete(self, path: str, **kwargs) -> Resp:
        return self.request('DELETE', self.base_url + path, **kwargs)


class RegionalHTTPClient:
    def __init__(self, http_client: HTTPClient, identity_url: str):
        self.identity = IdentityManager(http_client, identity_url)

        self.http_client = copy.deepcopy(http_client)
        self.http_client.headers.pop('X-Token', None)

    def request(self, method: str, url: str, **kwargs) -> Resp:
        x_auth_token = self.identity.get_x_auth_token()
        self.http_client.headers['X-Auth-Token'] = x_auth_token

        try:
            response = self.http_client.request(method, url, **kwargs)
        except ClientException as e:
            e.message, e.errors = unserialize_quota_error(e.args[0].message)
            raise e

        return response

    def get(self, path: str, service: str, region: str, **kwargs) -> Resp:
        return self.request(
            'GET', self.make_url(service, region, path), **kwargs
        )

    def post(self, path: str, service: str, region: str, **kwargs) -> Resp:
        return self.request(
            'POST', self.make_url(service, region, path), **kwargs
        )

    def patch(self, path: str, service: str, region: str, **kwargs) -> Resp:
        return self.request(
            'PATCH', self.make_url(service, region, path), **kwargs
        )

    def delete(self, path: str, service: str, region: str, **kwargs) -> Resp:
        return self.request(
            'DELETE', self.make_url(service, region, path), **kwargs
        )

    def make_url(self, service: str, region: str, path: str) -> str:
        region_service_url = self.identity.get_url_by_service(service, region)
        return f'{region_service_url}{path}'


@dataclass
class XAuthToken:
    token: str
    expires: Optional[dt] = None


class IdentityManager:
    MIN_TOKEN_TTL: timedelta = timedelta(seconds=180)

    def __init__(
        self,
        cloud_management: HTTPClient,
        identity_url: str
    ):
        self.cloud_management = cloud_management
        self.identity_url = identity_url

        self.account_name: Optional[str] = None
        self._x_auth_token: Optional[XAuthToken] = None
        self.keystone: Optional[KeystoneClient] = None

    def get_x_auth_token(self) -> str:
        if not self._x_auth_token:
            self._x_auth_token = self._issue_x_auth_token()
            return self._x_auth_token.token

        ttl = self._x_auth_token.expires.timestamp() - dt.now().timestamp()
        if ttl < self.MIN_TOKEN_TTL.seconds:
            self._x_auth_token = self._issue_x_auth_token()
            return self._x_auth_token.token

        return self._x_auth_token.token

    def get_url_by_service(self, service: str, region: str) -> str:
        x_auth_token = self.get_x_auth_token()
        token_info = self.keystone.tokens.validate(token=x_auth_token)

        return token_info.service_catalog.url_for(
            service_type=service,
            region_name=region,
        )

    def _issue_x_auth_token(self) -> XAuthToken:
        resp = self.cloud_management.post(
            path='/tokens',
            json={'token': {'account_name': self._get_account_name()}},
        )
        x_auth_token = resp.json()['token']['id']

        # Re-initialize keystone client because the token has been refreshed.
        self._init_keystone_client(token=x_auth_token)

        token_info = self.keystone.tokens.validate(token=x_auth_token)

        return XAuthToken(token=x_auth_token, expires=token_info.expires)

    def _get_account_name(self) -> str:
        if self.account_name:
            return self.account_name

        resp = self.cloud_management.get(path='/accounts')
        self.account_name = resp.json()['account']['name']

        return self.account_name

    def _init_keystone_client(self, token: str):
        auth_token = KeystoneToken(self.identity_url, token)
        session = KeystoneSession(auth=auth_token)
        self.keystone = KeystoneClient(session=session)
