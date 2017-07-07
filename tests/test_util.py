import json
import pytest
from selvpcclient.util import (build_url,
                               sort_list_of_dicts,
                               try_parse_json,
                               update_json_error_message,
                               parse_headers,
                               resource_filter)


def test_resource_filter():
    @resource_filter
    def list(detailed=False):
        return [{"project_id": "id", "region": "1", "detailed": detailed},
                {"project_id": "xxx", "region": "2", "detailed": detailed}]

    result = list()
    assert len(result) == 2
    assert result[0]["detailed"] is False

    result = list(detailed=True, project_id="id")
    assert len(result) == 1
    assert result[0]["detailed"] is True

    result = list(detailed=True, region="1")
    assert len(result) == 1
    assert result[0]["detailed"] is True

    result = list(detailed=True, project_id="id", region="1")
    assert len(result) == 1
    assert result[0]["detailed"] is True


def test_is_json_true():
    assert try_parse_json('{"key": "awesome_value"}')


def test_perse_headers():
    headers = ["some: value", "foo: bar", "broken header"]

    result = parse_headers(headers)

    assert len(result) == 2
    assert result["some"] == "value"
    assert result["foo"] == "bar"


@pytest.mark.parametrize('json_', ["{'key': 'awesome_value'}", None])
def test_is_json_false(json_):
    assert try_parse_json(json_) is False


def test_build_url():
    assert build_url('http://api', 'v2') == 'http://api/v2'
    assert build_url('http://api', 'v', '2') == 'http://api/v/2'


def test_update_response_error_message():
    new_content = update_json_error_message(
        content=json.dumps({'error': 'already_exists'})
    )

    assert new_content == 'Already exists'


def test_sort_list_of_dicts():
    input = [
        {"name": "zzz", "value": 333},
        {"name": "www", "value": 333},
        {"name": "aaa", "value": 333},
        {"name": "bbb", "value": 333},
    ]

    result = sort_list_of_dicts(input, dict_key="name")

    assert result[0]["name"] == 'aaa'
    assert result[1]["name"] == 'bbb'
    assert result[2]["name"] == 'www'
    assert result[3]["name"] == 'zzz'
