from tests.cli import make_client, run_cmd
from tests.util import answers


def test_quota_set():
    COUNT_OF_QUOTAS = 6
    client = make_client(return_value=answers.QUOTAS_SET)
    args = ['quota set',
            'c2383dc1894748b193031ae1bccf508a',
            '--resource=compute_cores',
            '--region=ru-2',
            '--zone=ru-2a',
            '--value=1']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_QUOTAS


def test_quota_show():
    count_of_quotas = len(answers.QUOTAS_SHOW['quotas'])
    client = make_client(return_value=answers.QUOTAS_SHOW)
    args = ['quota show',
            '--region=ru-1',
            '30bde559615740d28bb63ee626fd0f25']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == count_of_quotas


def test_quotas_partial_resp():
    client = make_client(return_value=answers.QUOTAS_PARTIAL)
    args = ['quota set',
            '30bde559615740d28bb63ee626fd0f25',
            '--resource', 'image_gigabytes',
            '--region', 'ru-1',
            '--value', '400']
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
