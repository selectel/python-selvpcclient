import copy
import logging

import requests

from selvpcclient.exceptions.base import ClientException
from selvpcclient.exceptions.http import get_http_exception
from selvpcclient.util import make_curl, update_json_error_message

logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, base_url, headers, timeout=60):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def request(self, method, url, **kwargs):
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

    def get(self, path, **kwargs):
        return self.request('GET', self.base_url + path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('POST', self.base_url + path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request('PATCH', self.base_url + path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request('DELETE', self.base_url + path, **kwargs)
