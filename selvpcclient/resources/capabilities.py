from selvpcclient import base


class Capabilities(base.Resource):
    """Represents a capabilities."""


class CapabilitiesManager(base.Manager):
    """Manager class for getting possible values for different variables."""
    resource_class = Capabilities

    def get(self):
        """Get possible values for different variables

        :rtype: :class:`Capabilities`
        """
        return self._get('/capabilities', 'capabilities')
