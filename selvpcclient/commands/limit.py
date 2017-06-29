from selvpcclient.base import ListCommand
from selvpcclient.formatters import join_by_key, reformat_quotas
from selvpcclient.util import handle_http_error


class List(ListCommand):
    """Show domain quotas"""

    columns = ["resource", "region", "zone", "value"]
    _formatters = {
        "region": join_by_key("region"),
        "zone": join_by_key("zone"),
        "value": join_by_key("value")
    }
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].quotas.get_domain_quotas()
        return self.setup_columns(reformat_quotas(result._info), parsed_args)


class Free(ListCommand):
    """Show free domain quotas"""

    columns = ["resource", "region", "zone", "value"]
    _formatters = {
        "region": join_by_key("region"),
        "zone": join_by_key("zone"),
        "value": join_by_key("value")
    }
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].quotas.get_free_domain_quotas()
        return self.setup_columns(reformat_quotas(result._info), parsed_args)
