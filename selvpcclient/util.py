import base64
import hashlib
import json
import logging
import os
import sys
from typing import Dict, Optional, Tuple

import requests

from selvpcclient.exceptions.base import ClientException

log = logging.getLogger(__name__)

SENSITIVE_HEADERS = ['X-Token', 'X-Auth-Token', 'X-Subject-Token']

FILES_EXTENSIONS = ("png", "jpg", "svg", "txt")


def parse_headers(headers):
    result = {}
    for header in headers:
        if ':' in header:
            header = header.replace(' ', '')
            parts = header.split(':')
            result[parts[0]] = parts[1]
    return result


def handle_http_error(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            log.error(err)
            sys.exit(2)

    return wrap


def resource_filter(func):
    """This decorator allows to you filter answer from RESOURCE.list() by
    project_id and region.
    Both params are optional and may be used separately.

    Example:
        selvpc --debug floatingip list
        selvpc --debug floatingip list --project=UUID
        selvpc --debug floatingip list --region=REGION
        selvpc --debug floatingip list --project=UUID --region=REGION

        client.subnets.list(project=UUID)
        client.subnets.list(region=REGION)
        client.subnets.list(project=UUID, region=REGION)
    """

    def wrap(*args, **kwargs):
        project_id = kwargs.pop("project_id", None)
        region = kwargs.pop("region", None)
        resources = func(*args, **kwargs)

        if project_id:
            resources = [r for r in resources if r["project_id"] == project_id]

        if region:
            resources = [r for r in resources if r["region"] == region]

        return resources

    return wrap


def add_resource_filter_arguments(parser, add_region=True, add_project=True):
    if add_project:
        parser.add_argument(
            '-p',
            '--project',
            dest="project_id",
            required=False,
            default=None,
            type=str,
        )
    if add_region:
        parser.add_argument(
            '-r',
            '--region',
            required=False,
            default=None,
            type=str,
        )


def confirm_action(action):
    """Func must be a take_action func."""

    def wrap(func):
        def wrap(*args, **kwargs):
            if not hasattr(args[1], "yes_i_really_want_to_" + action):
                log.error("Please add confirm argument into parser.")
                sys.exit(-1)

            accept = getattr(args[1], "yes_i_really_want_to_" + action)
            if not accept:
                log.warning("Confirm action by --yes-i-really-want-to-%s",
                            action)
                sys.exit(-1)

            return func(*args, **kwargs)

        return wrap

    return wrap


def get_item_properties(item, fields, mixed_case_fields=(), formatters=None):
    """Return a tuple containing the item properties.

    :param item: a single item resource (e.g. Server, Tenant, etc)
    :param fields: tuple of strings with the desired field names
    :param mixed_case_fields: tuple of field names to preserve case
    :param formatters: dictionary mapping field names to callables
       to format the values
    """
    if formatters is None:
        formatters = {}

    row = []

    for field in fields:
        if field in formatters:
            row.append(formatters[field](item))
        else:
            if field in mixed_case_fields:
                field_name = field.replace(' ', '_')
            else:
                field_name = field.lower().replace(' ', '_')
            if not hasattr(item, field_name) and isinstance(item, dict):
                data = item[field_name]
            else:
                data = getattr(item, field_name, '')
            if data is None:
                data = ''
            row.append(data)
    return tuple(row)


def sort_list_of_dicts(list_, dict_key):
    """Sort list of dicts by dict key

    :param list list_: List of dicts,
    :param string dict_key: Dict key for sorting.
    :rtype: list
    """

    # NOTE: Python 3 introduced new rules for ordering comparisons:
    # See detailed here (chapter ordering-comparisons)
    # https://docs.python.org/release/3.0.1/whatsnew/3.0.html
    items = []
    for item in list_:
        if item[dict_key] is None:
            item[dict_key] = str()
        items.append(item)

    return sorted(items, key=lambda item: item[dict_key])


def build_url(*args):
    """Build URL by provided parts of url.
    Also this method strip all right slashes.

    :param args: Parts of url.
    :rtype: str
    """
    return "/".join([part.rstrip('/') for part in args])


def update_json_error_message(content):
    """Converts and capitalize JSON error to normal message.

    :param str content: JSON-answer from server.
    :rtype: str
    """
    if 'error' in content:
        try:
            message = json.loads(content)['error']
            return message.capitalize().replace('_', ' ')
        except Exception:
            return content


def try_parse_json(json_):
    """Converts the string representation of JSON to JSON.

    :param str json_: JSON in str representation.
    :rtype: :class:`dict` if converted successfully, otherwise False.
    """
    if not json_:
        return False

    try:
        return json.loads(json_)
    except ValueError:
        return False


def make_curl(url, method, data):
    string_parts = ['curl -i', ' -X{} "{}"'.format(method, url)]

    for key, value in data.get('headers', {}).items():
        if key in SENSITIVE_HEADERS:
            v = str()
            if value:
                v = value.encode('utf-8')
            h = hashlib.sha1(v)
            d = h.hexdigest()
            value = "{SHA1}%s" % d
        header = ' -H "%s: %s"' % (key, value)
        string_parts.append(header)

    if data.get('json', None):
        string_parts.append(" -d '%s'" % (json.dumps(data['json'])))
    return "".join(string_parts)


def is_url(data):
    """Checks if getting value is valid url and path exists."""
    try:
        r = requests.head(data)
    except Exception:
        return False
    return r.status_code == requests.codes.ok


def process_logo_by_url(url):
    """Download and encode image by url."""
    res = requests.get(url)
    encoded_logo = base64.b64encode(res.content)
    return encoded_logo


def process_theme_params(func):
    """This decorator allows to enter path to logo/url to logo
     and adds hash to color value."""

    def inner(*args, **kwargs):
        color = kwargs.get("color", None)
        if color and not color.startswith("#"):
            kwargs["color"] = "#" + color
        brand_color = kwargs.get("brand_color", None)
        if brand_color and not brand_color.startswith("#"):
            kwargs["brand_color"] = "#" + brand_color
        path = kwargs.get("logo", None)
        if path:
            if os.path.isfile(path) and path.endswith(FILES_EXTENSIONS):
                with open(path, "rb") as image_file:
                    if not path.endswith("txt"):
                        encoded_logo = base64.b64encode(image_file.read())
                    else:
                        encoded_logo = image_file.read()
                    kwargs["logo"] = encoded_logo
            elif is_url(path):
                kwargs["logo"] = process_logo_by_url(path)
            else:
                raise Exception("Invalid path/url or file")
        return func(*args, **kwargs)

    return inner


def process_pair_params(func):
    """This decorator allows to enter path to ~/.ssh/id_rsa.pub or provide
    id_rsa.pub as plain-text.
    """

    def inner(*args, **kwargs):
        path = kwargs["keypair"]["keypair"]["public_key"]
        if os.path.isfile(path):
            with open(path, "r") as sr:
                kwargs["keypair"]["keypair"]["public_key"] = sr.read().rstrip()
        return func(*args, **kwargs)

    return inner


def convert_to_short(logo_b64):
    if len(logo_b64) >= 50:
        logo_b64 = logo_b64[:15] + ' ... ' + logo_b64[len(logo_b64) - 15:]
    return logo_b64


def unserialize_quota_error(content: str) -> Tuple[str, Optional[Dict]]:
    """Extract general error message and list of errors.

    :param str content: serialized dictionary

    Example input data: str({
        "error": {
            "message": "Bad Request",
            "code": 400,
            "errors": [
                {
                    "resource": "compute_ram",
                    "zone": "ru-1a",
                    "message": "Value doesn't divisible 256.",
                    "code": 400
                }
            ]
        }
    })
    """
    if 'error' in content:
        try:
            error = json.loads(content)['error']
            return error['message'], error['errors']
        except Exception:
            return content, None

    return content, None


def extract_single_quota_error(e: ClientException) -> str:
    """Extract single error from quotas error list.

    :param ClientException e: Client Exception (400-599 HTTP error)

    This is used for pretty output in CLI (quota set). It is assumed that when
    setting a quota through the CLI, there can be only one error.
    """
    if isinstance(e.errors, list):
        return e.errors[0]['message']

    return e.args[0].message
