import abc
import logging

from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from selvpcclient.util import get_item_properties

log = logging.getLogger(__name__)


class PartialResponse(object):
    """Class represents a partial response for created objects (floating ips,
    subnets, quotas and etc)."""

    def __init__(self, manager, ok, fail):
        if manager.resource_class.__name__ == "Quotas":
            self.resources = Resource(manager, ok)
            self._info = self.resources._info
        else:
            self._info = ok
            self.resources = [Resource(manager, res) for res in ok if res]
        self._fail = fail

    def __iter__(self):
        return self.resources.__iter__()

    def __len__(self):
        return self.resources.__len__()

    def __getitem__(self, item):
        return self.resources[item]

    def get_fail_info(self):
        return self._fail


class Manager(object):
    """Basic manager type providing common operations.

    Provide HTTP operations (post, get, patch etc.) and convert to type.

    :param client: instance of HTTPClient.
    """
    resource_class = None

    def __init__(self, client):
        self.client = client

    def _list(self, url, response_key, obj_class=None, body=None,
              return_raw=False, **kwargs):
        """List the collection.

        :param url: a partial URL, e.g., '/servers'
        :param response_key: the key to be looked up in response dictionary,
                e.g., 'servers'
        :param obj_class: class for constructing the returned objects
                (self.resource_class will be used by default)
        :param body: data that will be encoded as JSON and passed in POST
                request (GET will be sent by default)
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param kwargs: Additional arguments will be passed to the request.
        """
        if body:
            resp = self.client.post(url, json=body, **kwargs)
        else:
            resp = self.client.get(url, **kwargs)
        if return_raw:
            return resp.json()[response_key]
        data = resp.json()[response_key]
        if obj_class is None:
            obj_class = self.resource_class
        if "ok" in data:
            log.warning("207 Multi-Status: %s/%s %s has been created. "
                        "More details: %s",
                        len(data["ok"]),
                        len(data["ok"]) + len(data["fail"]),
                        response_key,
                        data["fail"])
            return PartialResponse(manager=self,
                                   ok=data["ok"],
                                   fail=data["fail"])
        return [obj_class(self, res) for res in data if res]

    def _get(self, url, response_key, return_raw=False, **kwargs):
        """Get an object from collection.

        :param url: a partial URL, e.g., '/servers'
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'server'
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param kwargs: Additional arguments will be passed to the request.
        """

        resp = self.client.get(url, **kwargs)
        if return_raw:
            return resp.json()[response_key]
        return self.resource_class(self, resp.json()[response_key])

    def _post(self, url, body, response_key, return_raw=False, **kwargs):
        """Create an object.

        :param url: a partial URL, e.g., '/servers'
        :param body: data that will be encoded as JSON and passed in POST
                request (GET will be sent by default)
        :param response_key: the key to be looked up in response dictionary,
                e.g., 'servers'
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param kwargs: Additional arguments will be passed to the request.
        """
        resp = self.client.post(url, json=body, **kwargs)
        if return_raw:
            return resp.json()[response_key]
        return self.resource_class(self, resp.json()[response_key])

    def _patch(self, url, body=None, response_key=None, return_raw=False,
               **kwargs):
        """Update an object with PATCH method.

        :param url: a partial URL, e.g., '/servers'
        :param body: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'servers'
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param kwargs: Additional arguments will be passed to the request.
        """
        resp = self.client.patch(url, json=body, **kwargs)
        if return_raw:
            return resp.json()[response_key] if response_key else resp.json()
        if response_key:
            data = resp.json()[response_key]
            if "ok" in data:
                log.warning("207 Multi-Status: %s/%s %s has been created. "
                            "More details: %s",
                            len(data["ok"]),
                            len(data["ok"]) + len(data["fail"]),
                            response_key,
                            data["fail"])
                return PartialResponse(manager=self,
                                       ok=data["ok"],
                                       fail=data["fail"])
            return self.resource_class(self, data)
        else:
            return self.resource_class(self, resp.json())

    def _delete(self, url):
        """Delete an object.

        :param url: a partial URL, e.g., '/servers/my-server'
        """
        return self.client.delete(url)


class Resource(object):
    """Base class for VPC resources (project, user, etc.).

    This is pretty much just a bag for attributes.
    """

    def __init__(self, manager, info):
        self.manager = manager
        self._info = info
        self._add_details(info)

    def __repr__(self):
        reprkeys = sorted(k for k in self.__dict__.keys()
                          if k[0] != '_' and k != 'manager')
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)

    def _add_details(self, info):
        for k, v in info.items():
            setattr(self, k, v)

    def __getattr__(self, k):
        return self.__dict__[k]

    def __getitem__(self, item):
        return self.__dict__[item]


class CLICommand(Command):
    logger = logging.getLogger(__name__)

    def add_known_arguments(self, parser):
        pass

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        self.add_known_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        pass


class DisplayCommand(CLICommand, metaclass=abc.ABCMeta):
    columns = []
    _formatters = {}

    def setup_columns(self, info, parsed_args):
        pass


class ShowCommand(DisplayCommand, ShowOne):
    def setup_columns(self, info, parsed_args):
        row = []
        if parsed_args.columns:
            self.columns = [
                x for x in parsed_args.columns if x in self.columns
            ]

        for field in self.columns:
            if field in self._formatters:
                row.append(self._formatters[field](info))
            else:
                field_name = field.lower().replace(' ', '_')
                if not hasattr(info, field_name) and isinstance(info, dict):
                    data = info[field_name]
                else:
                    data = getattr(info, field_name, '')
                if data is None:
                    data = ''
                row.append(data)
        return self.columns, row


class ListCommand(DisplayCommand, Lister):
    sorting_support = False

    def add_known_arguments(self, parser):
        if self.sorting_support:
            parser.add_argument(
                '--sort-key',
                dest='sort_key',
                metavar='FIELD',
                help=(
                    "Sorts the list by the specified fields in the specified "
                    "directions. "
                    "Missing sort_dir options use the default asc value."),
                default=None
            )
            parser.add_argument(
                '--sort-dir',
                dest='sort_dir',
                metavar='{asc,desc}',
                help="Sort the list in the specified direction.",
                default='asc',
                choices=['asc', 'desc']
            )
            parser.add_argument(
                '--count',
                dest='count',
                metavar='TABLE_LINES_COUNT',
                help="Max count of lines in table. Zero for all lines",
                default=0,
                type=int,
            )

    def setup_columns(self, info, parsed_args):
        if not hasattr(parsed_args, "count") or parsed_args.count <= 0:
            parsed_args.count = len(info)

        if parsed_args.columns:
            self.columns = [
                x for x in parsed_args.columns if x in self.columns
            ]
        generator = (get_item_properties(
            s,
            self.columns,
            formatters=self._formatters, ) for s in info[0:parsed_args.count])

        if self.sorting_support and parsed_args.sort_key:
            sort_key = parsed_args.sort_key
            reverse = parsed_args.sort_dir == 'desc'
            items = [item for item in generator]
            items.sort(
                key=lambda tup: tup[self.columns.index(sort_key)],
                reverse=reverse)
        else:
            items = generator
        return self.columns, items
