from selvpcclient import base
from selvpcclient.util import process_theme_params


class Customization(base.Resource):
    """Represents a customization."""

    def show(self):
        """Show current theme parameters.

        :rtype: :class 'Customization'
        """
        return self.manager.show()

    def update(self, color=None, logo=None):
        """Set theme parameters.

        :param string color: Panel color (e.x: 00ffee)
        :param string logo: Path to logo or base64 string
        :rtype: :class 'Customization' with updated fields
        """
        return self.manager.update(color, logo)

    def delete(self):
        """Delete current customization (color and logo)."""
        return self.manager.delete()


class CustomizationManager(base.Manager):
    """Manager class for customization operations."""

    resource_class = Customization

    def show(self):
        """Show current theme parameters.

        :rtype: :class 'Customization'
        """
        return self._get('/theme', 'theme')

    @process_theme_params
    def update(self, color, logo):
        """Set theme parameters.

        :param string color: Panel color (e.x: 00ffee)
        :param string logo: Path to logo or base64 string
        :rtype: :class 'Customization' with updated fields
        """
        body = {"theme": {}}
        if color:
            body["theme"]["color"] = color
        if logo:
            body["theme"]["logo"] = logo
        return self._post('/theme', body, 'theme')

    def delete(self):
        """Delete current customization (color and logo)."""
        return self._delete('/theme')
