from . import endpoints, entities
from .api_modes import ApiModes
from .client import Client

import pkg_resources

__version__ = pkg_resources.get_distribution(__package__).version
