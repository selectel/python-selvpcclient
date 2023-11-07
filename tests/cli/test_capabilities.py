from tests.cli import make_client, run_cmd
from tests.util import answers


def test_capabilities_show_regions():
    count_of_zones = 3
    client = make_client(return_value=answers.CAPABILITIES_LIST)
    args = ['capabilities show regions']

    regions = run_cmd(args, client, json_output=True)

    assert len(regions) == count_of_zones


def test_capabilities_show_resources():
    count_of_resources = 10
    client = make_client(return_value=answers.CAPABILITIES_LIST)
    args = ['capabilities show resources']

    resources = run_cmd(args, client, json_output=True)

    assert len(resources) == count_of_resources
