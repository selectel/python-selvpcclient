from selvpcclient.base import ListCommand
from selvpcclient.formatters import format_regions, join_by_key
from selvpcclient.util import handle_http_error


class Licenses(ListCommand):
    """Show available license values"""

    columns = ['type', 'availability']
    _formatters = {"availability": join_by_key("availability")}
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].capabilities.get()
        return self.setup_columns(result.licenses, parsed_args)


class Regions(ListCommand):
    """Show available region values"""

    columns = ['name', 'description', 'is_default', 'zones']
    _formatters = {"zones": format_regions}
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].capabilities.get()
        return self.setup_columns(result.regions, parsed_args)


class Resources(ListCommand):
    """Show available resource values"""

    columns = ['name', 'quota_scope', 'quotable', 'unbillable']
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].capabilities.get()
        return self.setup_columns(result.resources, parsed_args)


class Subnets(ListCommand):
    """Show available subnet values"""

    columns = ['type', 'prefix_length', 'availability']
    _formatters = {"availability": join_by_key("availability")}
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].capabilities.get()
        return self.setup_columns(result.subnets, parsed_args)


class Traffic(ListCommand):
    """Show available traffic values"""

    columns = ['granularity', 'timespan']
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].capabilities.get()
        return self.setup_columns(result.traffic["granularities"], parsed_args)
