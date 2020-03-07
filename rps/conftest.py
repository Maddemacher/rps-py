import os
import tempfile

import pytest

import rps


@pytest.fixture
def client():
    rps.app.config['TESTING'] = True

    with rps.app.test_client() as client:
        yield client
