# flake8: noqa

import pkg_resources

from . import endpoints, entities
from .api_modes import ApiModes
from .client import Client

__version__ = pkg_resources.get_distribution(__package__).version
