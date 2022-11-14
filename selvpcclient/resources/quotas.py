import logging
from typing import Union

from requests import Response

from selvpcclient.base import Manager, PartialResponse, Resource

log = logging.getLogger(__name__)


class Quotas(Resource):
    """Represents a quota."""


class QuotasManager(Manager):
    """Manager class for manipulating quota."""
    resource_class = Quotas

    SERVICE_NAME = 'quota-manager'
    RESPONSE_QUOTAS_KEY = 'quotas'
    RESPONSE_ERRORS_KEY = 'error'

    def _get(self, url: str, return_raw: bool = False,
             **kwargs) -> Union[Quotas, PartialResponse]:
        return self._handle_response(
            resp=self.client.get(url, **kwargs),
            return_raw=return_raw,
        )

    def _patch(self, url: str, body: dict = None, return_raw: bool = False,
               **kwargs) -> Union[Quotas, PartialResponse]:
        return self._handle_response(
            resp=self.client.patch(url, json=body, **kwargs),
            return_raw=return_raw,
        )

    def _handle_response(self, resp: Response, return_raw: bool = False
                         ) -> Union[Quotas, PartialResponse]:
        if return_raw:
            # JSON can have two keys: 'quotas' and 'error'
            return resp.json()

        quotas = resp.json()[self.RESPONSE_QUOTAS_KEY]

        if resp.status_code == 207:
            error = resp.json()[self.RESPONSE_ERRORS_KEY]

            log.warning(
                f'207 Multi-Status ({self.SERVICE_NAME}): \n\t'
                f'Request: {resp.request.method} {resp.request.url} \n\t'
                f'Errors: {error["errors"]}'
            )

            return PartialResponse(manager=self, ok=quotas, fail=error)

        return self.resource_class(self, quotas)

    def get_project_limits(self, project_id: str, region: str,
                           return_raw=False) -> Union[Quotas, PartialResponse]:
        """Show project limits.

        :param string project_id: Project id
        :param string region: name of region
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        """

        return self._get(
            url=f'/projects/{project_id}/limits',
            service=self.SERVICE_NAME,
            region=region,
            return_raw=return_raw,
        )

    def get_project_quotas(self, project_id: str, region: str,
                           return_raw=False) -> Union[Quotas, PartialResponse]:
        """Show quotas info for Project.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param string project_id: Project id
        :param string region: name of region
        """
        return self._get(
            url=f'/projects/{project_id}/quotas',
            service=self.SERVICE_NAME,
            region=region,
            return_raw=return_raw,
        )

    def update_project_quotas(self, project_id: str, region: str,
                              quotas: dict, return_raw=False
                              ) -> Union[Quotas, PartialResponse]:
        """Update Project's quotas.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param string project_id: Project id.
        :param string region: name of region
        :param dict quotas: Dict with key `quotas` and keys as dict
                            of items zone and value::

                                {
                                    "quotas": {
                                        "compute_cores": [
                                            {
                                                "zone": "ru-1a",
                                                "value": 10
                                            },
                                            {
                                                "zone": "ru-1b",
                                                "value": 10
                                            }
                                        ]
                                    }
                                }
        """

        return self._patch(
            url=f'/projects/{project_id}/quotas',
            body=quotas,
            service=self.SERVICE_NAME,
            region=region,
            return_raw=return_raw,
        )
