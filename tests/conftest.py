"""Shared pytest fixtures for the akeyless_cloud_id test suite.

All unit tests are hermetic: they must never touch the network. The autouse
fixture below disables the EC2 instance-metadata service (IMDS) for every test
so that any accidental boto3 credential lookup fails fast instead of hanging on
a metadata endpoint that is unreachable (or, worse, reachable) in CI.
"""

import pytest


@pytest.fixture(autouse=True)
def _disable_ec2_metadata(monkeypatch):
    # Belt-and-suspenders: even if a test forgets to provide credentials, boto3
    # must not reach out to the IMDS endpoint. This keeps the suite hermetic.
    monkeypatch.setenv("AWS_EC2_METADATA_DISABLED", "true")
    yield
