import os
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope='session')
def test_env():
    """Set test environment variables"""
    os.environ['ENVIRONMENT'] = 'test'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    yield
    os.environ['ENVIRONMENT'] = 'development'
