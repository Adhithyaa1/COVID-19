"""Vercel entrypoint: expose the Dash Flask server as ``app``."""

import importlib

importlib.import_module("dash_callbacks")

from webapp import server as app
