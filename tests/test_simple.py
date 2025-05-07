"""
Simple test file to verify pytest is working correctly.
"""

import pytest


def test_simple():
    """A simple test that always passes."""
    assert True


@pytest.mark.xfail(reason="This test is designed to fail")
def test_simple_fail():
    """A simple test that always fails."""
    assert False
