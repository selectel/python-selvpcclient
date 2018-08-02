from tests.cli import make_client, run_cmd
from tests.util import answers


def test_capabilities_show_licenses():
    count_of_licenses = 1
    client = make_client(return_value=answers.CAPABILITIES_LIST)
    args = ['capabilities show licenses']

    licenses = run_cmd(args, client, json_output=True)

    assert len(licenses) == count_of_licenses
    assert licenses[0]['type'] == 'license_windows_2012_standard'


def test_capabilities_show_regions():
    count_of_regions = 2
    client = make_client(return_value=answers.CAPABILITIES_LIST)
    args = ['capabilities show regions']

    licenses = run_cmd(args, client, json_output=True)

    assert len(licenses) == count_of_regions


def test_capabilities_show_resources():
    count_of_resources = 10
    client = make_client(return_value=answers.CAPABILITIES_LIST)
    args = ['capabilities show resources']

    licenses = run_cmd(args, client, json_output=True)

    assert len(licenses) == count_of_resources


def test_capabilities_show_subnets():
    count_of_subnets = 1
    client = make_client(return_value=answers.CAPABILITIES_LIST)
    args = ['capabilities show subnets']

    licenses = run_cmd(args, client, json_output=True)

    assert len(licenses) == count_of_subnets
    assert licenses[0]['type'] == 'ipv4'
    assert licenses[0]['prefix_length'] == '29'
    assert 'availability' in licenses[0]


def test_capabilities_show_traffic():
    count_of_granularities = 3
    client = make_client(return_value=answers.CAPABILITIES_LIST)
    args = ['capabilities show traffic']

    licenses = run_cmd(args, client, json_output=True)

    assert len(licenses) == count_of_granularities
