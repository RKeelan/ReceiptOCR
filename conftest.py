"""Pytest configuration file."""
import pytest


def pytest_configure(config):
    """Configure pytest to ignore specific warnings."""
    # Suppress the ccache warning from PaddlePaddle
    config.addinivalue_line(
        "filterwarnings",
        "ignore:No ccache found:UserWarning"
    ) 