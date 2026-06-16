"""Pytest configuration for pylynqa tests."""

from pylynqa.models import TestRunsFilter


def pytest_configure(config):
    """Pytest configuration for pylynqa acceptance tests."""
    # Prevent pytest from collecting these model classes as test suites
    # (their names start with "Test" but they are domain objects, not test cases).
    TestRunsFilter.__test__ = False  # ty: ignore[unresolved-attribute]
