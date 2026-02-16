#!/usr/bin/env python3
"""
Test script for GCP IAM authentication.

This script tests the generateGcp() method to ensure it works with:
1. Service account JSON files (via GOOGLE_APPLICATION_CREDENTIALS)
2. GCE metadata server (when running on GCE instance)
3. Detects and reports user ADC credentials (not supported for ID tokens)

Usage:
    # Test with service account JSON
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
    python test_gcp_auth.py

    # Test on GCE instance (no environment variable needed)
    python test_gcp_auth.py
"""

import os
import sys

# Add the akeyless_cloud_id module to the path
sys.path.insert(0, os.path.dirname(__file__))

from akeyless_cloud_id import CloudId


def detect_credential_type():
    """Detect and display the type of GCP credentials being used."""
    try:
        import google.auth
        credentials, project = google.auth.default()
        cred_type = type(credentials).__name__
        return cred_type, project
    except Exception as e:
        return f"Error: {e}", None


def test_gcp_authentication():
    """Test GCP authentication with different credential sources."""
    
    print("Testing GCP IAM Authentication...")
    print("-" * 50)
    
    # Detect credential type
    cred_type, project = detect_credential_type()
    print(f"Detected credential type: {cred_type}")
    if project:
        print(f"Project: {project}")
    
    # Check which credential source is being used
    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        print(f"Credential source: GOOGLE_APPLICATION_CREDENTIALS")
        print(f"  Path: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
    else:
        print("Credential source: Default credentials (metadata server or ADC)")
    
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
        
    except ValueError as e:
        # Expected error for unsupported credential types
        print(f"✗ ValueError: {str(e)}")
        print()
        return False
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
