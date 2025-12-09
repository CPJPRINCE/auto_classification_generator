"""
auto_classification_generator package definitions

Author: Christopher Prince
license: Apache License 2.0"
"""

from .common import *
from .reference_generator import ReferenceGenerator
from .cli import parse_args,run_cli
import importlib.metadata

__author__ = "Christopher Prince (c.pj.prince@gmail.com)"
__license__ = "Apache License Version 2.0"
__version__ = importlib.metadata.version("auto_reference_generator")