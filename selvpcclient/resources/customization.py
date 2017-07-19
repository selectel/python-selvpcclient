from selvpcclient import base
from selvpcclient.util import process_theme_params


class Customization(base.Resource):
    """Represents a customization."""

    def show(self, return_raw=False):
        """Show current theme parameters.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class 'Customization'
        """
        return self.manager.show(return_raw=return_raw)

    def update(self, color=None, logo=None, return_raw=False):
        """Set theme parameters.

        :param string color: Panel color (e.x: 00ffee)
        :param string logo: Path to logo or URL
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class 'Customization' with updated fields
        """
        return self.manager.update(color, logo, return_raw=return_raw)

    def delete(self):
        """Delete current customization (color and logo)."""
        return self.manager.delete()


class CustomizationManager(base.Manager):
    """Manager class for customization operations."""

    resource_class = Customization

    def show(self, return_raw=False):
        """Show current theme parameters.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class 'Customization'
        """
        return self._get('/theme', 'theme', return_raw=return_raw)

    @process_theme_params
    def update(self, color, logo, return_raw=False):
        """Set theme parameters.

        :param string color: Panel color (e.x: 00ffee)
        :param string logo: Path to logo or URL
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class 'Customization' with updated fields
        """
        body = {"theme": {}}
        if color:
            body["theme"]["color"] = color
        if logo:
            body["theme"]["logo"] = logo
        return self._post('/theme', body, 'theme', return_raw=return_raw)

    def delete(self):
        """Delete current customization (color and logo)."""
        return self._delete('/theme')
