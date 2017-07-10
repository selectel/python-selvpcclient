import responses

from selvpcclient.resources.quotas import QuotasManager
from tests.rest import client
from tests.util import answers, params


@responses.activate
def test_quotas_get():
    responses.add(responses.GET, 'http://api/v2/quotas',
                  json=answers.QUOTAS_LIST)

    manager = QuotasManager(client)

    quotas = manager.get_domain_quotas()

    assert quotas is not None


@responses.activate
def test_quotas_get_free():
    responses.add(responses.GET, 'http://api/v2/quotas/free',
                  json=answers.QUOTAS_LIST)

    manager = QuotasManager(client)

    quotas = manager.get_free_domain_quotas()

    assert quotas is not None


@responses.activate
def test_quotas_get_for_single_project():
    responses.add(responses.GET, 'http://api/v2/quotas/projects/123',
                  json=answers.QUOTAS_SHOW)

    manager = QuotasManager(client)

    quotas = manager.get_project_quotas(project_id=123)

    assert quotas is not None


@responses.activate
def test_quotas_projects_get():
    responses.add(responses.GET, 'http://api/v2/quotas/projects',
                  json=answers.QUOTAS_LIST)

    manager = QuotasManager(client)

    project_quotas = manager.get_projects_quotas()

    assert project_quotas is not None


@responses.activate
def test_quotas_projects_patch():
    responses.add(responses.PATCH, 'http://api/v2/quotas/projects/123',
                  json=answers.QUOTAS_SET)

    manager = QuotasManager(client)

    project_quotas = manager.update(project_id="123", quotas=params.quotas)

    assert project_quotas is not None


@responses.activate
def test_quotas_partial_response():
    responses.add(responses.PATCH, 'http://api/v2/quotas/projects/123',
                  json=answers.QUOTAS_PARTIAL,
                  status=207)

    manager = QuotasManager(client)

    project_quotas = manager.update(project_id="123", quotas=params.quotas)

    assert project_quotas._info == answers.QUOTAS_PARTIAL_RESULT


@responses.activate
def test_quotas_raw_get():
    responses.add(responses.GET, 'http://api/v2/quotas',
                  json=answers.QUOTAS_LIST)

    manager = QuotasManager(client)

    quotas = manager.get_domain_quotas(return_raw=True)

    assert quotas == answers.QUOTAS_LIST["quotas"]
