import base64
import json
import pytest
import responses

from selvpcclient.util import (build_url,
                               sort_list_of_dicts,
                               try_parse_json,
                               update_json_error_message,
                               parse_headers,
                               resource_filter,
                               process_theme_params)
from tests.util.params import LOGO_BASE64
from tests.util.temp_files import get_temporary_logo, get_temporary_text_file


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


def test_process_theme_params_hex_to_color():
    @process_theme_params
    def function_that_takes_theme_params(logo=None, color=""):
        assert logo is None
        assert color == "#eeff00"

    function_that_takes_theme_params(logo=None, color='eeff00')


def test_process_theme_params_invalid_logo():
    @process_theme_params
    def function_that_takes_theme_params(logo=None, color=''):
        pass

    with pytest.raises(Exception):
        function_that_takes_theme_params(logo='is \' not path or url!!!',
                                         color='')


def test_process_theme_params_wrong_path():
    @process_theme_params
    def function_that_takes_theme_params(logo=None, color=''):
        pass

    with pytest.raises(Exception):
        function_that_takes_theme_params(logo='/wrong/path/logo.jpg',
                                         color='')


def test_process_theme_params_right_path():
    path_to_logo = get_temporary_logo()
    with open(path_to_logo, 'rb') as logo:
        encoded_logo = base64.b64encode(logo.read())

        @process_theme_params
        def function_that_takes_theme_params(logo=None, color=''):
            assert logo == encoded_logo
            assert color == '#eeff00'

    function_that_takes_theme_params(logo=path_to_logo, color='eeff00')


def test_process_theme_params_logo_from_txt():
    with get_temporary_text_file() as path_to_file:
        @process_theme_params
        def function_that_takes_theme_params(logo=None, color=''):
            assert logo == LOGO_BASE64.encode('utf-8')
            assert color == '#eeff00'

        function_that_takes_theme_params(logo=path_to_file, color='eeff00')


@responses.activate
def test_process_theme_params_logo_from_url():
    responses.add(responses.HEAD,
                  'http://somehost.no/rand_logo.png',
                  status=200)
    path = get_temporary_logo()
    with open(path, 'rb') as logo:
        responses.add(responses.GET,
                      'http://somehost.no/rand_logo.png',
                      content_type='image/png',
                      stream=True,
                      body=logo.read(),
                      status=200)

    @process_theme_params
    def function_that_takes_theme_params(logo=None, color=''):
        url = responses.calls[0].request.url

        assert len(responses.calls) == 2
        assert url == 'http://somehost.no/rand_logo.png'
        assert logo is not None

    function_that_takes_theme_params(logo='http://somehost.no/rand_logo.png')
