# coding: utf-8
"""
    geny: an extendable file generator
"""
import os

__version__ = "0.1.0"
__license__ = "BSD 3-Clause"
__author__ = "Leo Neto"
__copyright__ = "Copyright 2024 Leo Neto"

COMMANDS_FOLDER = os.path.join(os.path.dirname(__file__), "commands")

PLUGINS_FOLDER = os.environ.get("GENY_PLUGINS", None)

VERSION = __version__
