from selvpcclient import base


class Capabilities(base.Resource):
    """Represents a capabilities."""


class CapabilitiesManager(base.Manager):
    """Manager class for getting possible values for different variables."""
    resource_class = Capabilities

    def get(self, return_raw=False):
        """Get possible values for different variables

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Capabilities`
        """
        return self._get('/capabilities', 'capabilities',
                         return_raw=return_raw)
