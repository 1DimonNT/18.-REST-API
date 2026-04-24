import pytest
import config

@pytest.fixture(scope='session')
def base_url():
    return config.settings.api_base_url
