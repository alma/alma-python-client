from . import endpoints
from . import entities

from .client import Client
from .api_modes import ApiModes

import pkg_resources

__version__ = pkg_resources.get_distribution(__package__).version
