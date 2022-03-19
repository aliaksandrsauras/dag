from pathlib import Path

import pytest

RESOURCES = Path(__file__).parents[1] / "resources"


@pytest.fixture
def resources():
    yield RESOURCES
