"""Modpack Changelogger - A powerful and customizable Python tool to generate a changelog between two Minecraft modpacks."""

from .main import generate_changelog
from .version import __version__

__all__ = ["__version__", "generate_changelog"]
