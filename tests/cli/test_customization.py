import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers
from tests.util import params


def test_show_theme_b64():
    client = make_client(return_value=answers.CUSTOMIZATION_SHOW)
    args = ['customization show', '--show-base64']

    output = run_cmd(args, client, json_output=True)

    assert output["color"] == "00ffee"
    assert output["logo"] == params.LOGO_BASE64


def test_show_no_theme_b64():
    client = make_client(return_value=answers.CUSTOMIZATION_NO_THEME)
    args = ['customization show', '--show-base64']

    output = run_cmd(args, client, json_output=True)

    assert output["color"] == ""
    assert output["logo"] == ""


def test_show_theme_b64_short():
    client = make_client(return_value=answers.CUSTOMIZATION_SHOW)
    args = ['customization show', '--show-short-base64']

    output = run_cmd(args, client, json_output=True)

    assert output["color"] == "00ffee"
    assert output["logo"] == params.LOGO_BASE64_SHORTEN


def test_show_no_theme_b64_short():
    client = make_client(return_value=answers.CUSTOMIZATION_NO_THEME)
    args = ['customization show', '--show-short-base64']

    output = run_cmd(args, client, json_output=True)

    assert output["color"] == ""
    assert output["logo"] == ""


def test_show_theme():
    client = make_client(return_value=answers.CUSTOMIZATION_SHOW)
    args = ['customization show']

    output = run_cmd(args, client, json_output=True)

    assert output["color"] == "00ffee"
    assert output["logo"] is True


def test_show_no_theme():
    client = make_client(return_value=answers.CUSTOMIZATION_NO_THEME)
    args = ['customization show']

    output = run_cmd(args, client, json_output=True)

    assert output["color"] == ""
    assert output["logo"] is False


def test_update_theme():
    client = make_client(return_value=answers.CUSTOMIZATION_UPDATE)
    args = ['customization update', '--color', '00eeff']

    output = run_cmd(args, client, json_output=True)

    assert output["color"] == "00eeff"


def test_customization_delete_without_confirm_flag():
    client = make_client(return_value={})
    args = ['customization delete']

    with pytest.raises(SystemExit):
        run_cmd(args, client)
