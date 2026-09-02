# -*- coding: utf-8 -*-

"""Top-level package for igv-reports."""

from importlib.metadata import PackageNotFoundError, version

__author__ = """Jim Robinson"""
__email__ = 'igv-team@broadinstitute.org'

try:
    # Single source of truth is the "version" field of pyproject.toml
    __version__ = version("igv-reports")
except PackageNotFoundError:
    # Running from a source checkout that was never installed
    __version__ = "unknown"
