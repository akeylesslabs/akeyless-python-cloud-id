#!/usr/bin/env python3
"""
Test script for GCP IAM authentication.

This script tests the generateGcp() method to ensure it works with:
1. Service account JSON files (via GOOGLE_APPLICATION_CREDENTIALS)
2. GCE metadata server (when running on GCE instance)
3. Application Default Credentials

Usage:
    # Test with service account JSON
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
    python test_gcp_auth.py

    # Test on GCE instance (no environment variable needed)
    python test_gcp_auth.py
"""

import os
import sys

import pytest

# Add the akeyless_cloud_id module to the path
sys.path.insert(0, os.path.dirname(__file__))

from akeyless_cloud_id import CloudId


# Live GCP test: requires real credentials and reaches the GCP token/metadata
# endpoint. Gated so it is skipped automatically in CI (which has no secrets).
# Set GOOGLE_APPLICATION_CREDENTIALS (or GCE_METADATA_HOST for a GCE instance)
# to run it.
@pytest.mark.skipif(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is None
    and os.getenv("GCE_METADATA_HOST") is None,
    reason="live GCP credentials not present (set GOOGLE_APPLICATION_CREDENTIALS to run)",
)
def test_gcp_authentication():
    """Test GCP authentication with different credential sources."""
    
    print("Testing GCP IAM Authentication...")
    print("-" * 50)
    
    # Check which credential source is being used
    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        print(f"Using service account JSON: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
    else:
        print("Using default credentials (metadata server or ADC)")
    
    print()
    
    try:
        # Create CloudId instance
        cloud_id = CloudId()
        
        # Test with default audience
        print("Generating GCP cloud ID with default audience (akeyless.io)...")
        token = cloud_id.generateGcp()
        print(f"✓ Success! Cloud ID generated (length: {len(token)} chars)")
        print(f"  First 50 chars: {token[:50]}...")
        print()
        
        # Test with custom audience
        custom_audience = "https://example.com"
        print(f"Generating GCP cloud ID with custom audience ({custom_audience})...")
        token_custom = cloud_id.generateGcp(audience=custom_audience)
        print(f"✓ Success! Cloud ID generated (length: {len(token_custom)} chars)")
        print(f"  First 50 chars: {token_custom[:50]}...")
        print()
        
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {str(e)}")
        print()
        print("Troubleshooting:")
        print("1. Make sure google-auth is installed: pip install google-auth")
        print("2. Set GOOGLE_APPLICATION_CREDENTIALS to a valid service account JSON")
        print("3. Or run on a GCE instance with proper IAM permissions")
        print()
        return False


if __name__ == "__main__":
    success = test_gcp_authentication()
    sys.exit(0 if success else 1)
