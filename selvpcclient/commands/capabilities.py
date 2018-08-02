from selvpcclient.base import ListCommand
from selvpcclient.formatters import join_by_key
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

    columns = ['region', 'region_description', 'is_region_default',
               'zone', 'zone_description', 'is_zone_default',
               'is_zone_enabled', 'is_zone_private']
    sorting_support = True

    def reformat_regions_info(self, regions):
        result = []
        for region in regions:
            for zone in region["zones"]:
                result.append({
                    "region": region["name"],
                    "region_description": region["description"],
                    "is_region_default": region["is_default"],
                    "zone": zone["name"],
                    "zone_description": zone["description"],
                    "is_zone_enabled": zone["enabled"],
                    "is_zone_default": zone["is_default"],
                    "is_zone_private": zone["is_private"],
                })
        return result

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].capabilities.get()
        info = self.reformat_regions_info(result.regions)
        return self.setup_columns(info, parsed_args)


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
