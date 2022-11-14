from unittest.mock import patch

import responses

from selvpcclient.base import PartialResponse
from selvpcclient.resources.quotas import Quotas, QuotasManager
from tests.rest import KeystoneTokenInfoMock
from tests.rest import regional_client
from tests.util import answers, params


@responses.activate
def test_limits_get():
    responses.add(responses.GET, 'http://api/v2/accounts',
                  json=answers.ACCOUNT_INFO)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)
    responses.add(responses.GET,
                  'http://ru-1.api'
                  '/projects/30bde559615740d28bb63ee626fd0f25/limits',
                  json=answers.LIMITS_SHOW)

    manager = QuotasManager(regional_client)

    with patch('keystoneclient.v3.tokens.TokenManager.validate',
               return_value=KeystoneTokenInfoMock()):
        limits = manager.get_project_limits(
            project_id='30bde559615740d28bb63ee626fd0f25', region='ru-1')

    assert limits is not None
    assert isinstance(limits, Quotas) is True


@responses.activate
def test_quotas_get_for_single_project():
    responses.add(responses.GET, 'http://api/v2/accounts',
                  json=answers.ACCOUNT_INFO)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)
    responses.add(responses.GET,
                  'http://ru-1.api'
                  '/projects/30bde559615740d28bb63ee626fd0f25/quotas',
                  json=answers.QUOTAS_SHOW)

    manager = QuotasManager(regional_client)

    with patch('keystoneclient.v3.tokens.TokenManager.validate',
               return_value=KeystoneTokenInfoMock()):
        quotas = manager.get_project_quotas(
            project_id='30bde559615740d28bb63ee626fd0f25', region='ru-1')

    assert quotas is not None
    assert isinstance(quotas, Quotas) is True


@responses.activate
def test_quotas_projects_patch():
    responses.add(responses.GET, 'http://api/v2/accounts',
                  json=answers.ACCOUNT_INFO)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)
    responses.add(responses.PATCH,
                  'http://ru-1.api'
                  '/projects/30bde559615740d28bb63ee626fd0f25/quotas',
                  json=answers.QUOTAS_SET)

    manager = QuotasManager(regional_client)

    with patch('keystoneclient.v3.tokens.TokenManager.validate',
               return_value=KeystoneTokenInfoMock()):
        project_quotas = manager.update_project_quotas(
            project_id="30bde559615740d28bb63ee626fd0f25", region='ru-1',
            quotas=params.quotas)

    assert project_quotas is not None
    assert isinstance(project_quotas, Quotas) is True


@responses.activate
def test_quotas_partial_response():
    responses.add(responses.GET, 'http://api/v2/accounts',
                  json=answers.ACCOUNT_INFO)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)
    responses.add(responses.PATCH,
                  'http://ru-1.api'
                  '/projects/30bde559615740d28bb63ee626fd0f25/quotas',
                  json=answers.QUOTAS_PARTIAL,
                  status=207)

    manager = QuotasManager(regional_client)

    with patch('keystoneclient.v3.tokens.TokenManager.validate',
               return_value=KeystoneTokenInfoMock()):
        project_quotas = manager.update_project_quotas(
            project_id="30bde559615740d28bb63ee626fd0f25", region='ru-1',
            quotas=params.quotas)

    assert isinstance(project_quotas, PartialResponse) is True
    assert project_quotas._info == answers.QUOTAS_PARTIAL["quotas"]
    assert project_quotas._fail == answers.QUOTAS_PARTIAL["error"]


@responses.activate
def test_limits_raw_get():
    responses.add(responses.GET, 'http://api/v2/accounts',
                  json=answers.ACCOUNT_INFO)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)
    responses.add(responses.GET,
                  'http://ru-1.api'
                  '/projects/30bde559615740d28bb63ee626fd0f25/limits',
                  json=answers.LIMITS_SHOW)

    manager = QuotasManager(regional_client)

    with patch('keystoneclient.v3.tokens.TokenManager.validate',
               return_value=KeystoneTokenInfoMock()):
        limits = manager.get_project_limits(
            project_id='30bde559615740d28bb63ee626fd0f25', region='ru-1',
            return_raw=True)

    assert limits == answers.LIMITS_SHOW
    assert isinstance(limits, dict) is True
