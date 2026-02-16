# GCP Authentication - Additional Documentation

## Overview

The `generateGcp()` method now supports multiple credential sources, making it suitable for both local development and cloud environments.

## Credential Sources (Auto-detected)

The library automatically detects and uses credentials in the following order:

1. **Service Account JSON** - Via `GOOGLE_APPLICATION_CREDENTIALS` environment variable
2. **Application Default Credentials (ADC)** - From gcloud CLI or default locations
3. **GCE Metadata Server** - When running on Google Compute Engine instances
4. **Workload Identity** - When running on Google Kubernetes Engine (GKE)

## Usage Examples

### Local Development with Service Account

```python
import os
from akeyless_cloud_id import CloudId

# Set the path to your service account JSON file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/service-account.json'

# Generate cloud ID
cloud_id = CloudId()
token = cloud_id.generateGcp(audience="akeyless.io")
```

### On GCE Instance (Automatic)

```python
from akeyless_cloud_id import CloudId

# No configuration needed - automatically uses instance metadata
cloud_id = CloudId()
token = cloud_id.generateGcp(audience="akeyless.io")
```

### With gcloud CLI Authentication

```bash
# Authenticate with gcloud
gcloud auth application-default login
```

```python
from akeyless_cloud_id import CloudId

# Uses Application Default Credentials from gcloud
cloud_id = CloudId()
token = cloud_id.generateGcp(audience="akeyless.io")
```

### Custom Audience

```python
from akeyless_cloud_id import CloudId

cloud_id = CloudId()
token = cloud_id.generateGcp(audience="https://my-custom-audience.com")
```

## Installation

Install with GCP support:

```bash
pip install akeyless-cloud-id[gcp]
```

## Dependencies

- `google-auth>=2.0.0` - Included in the `gcp` extras

## Troubleshooting

### "Failed to retrieve http://metadata.google.internal/..."

This error occurs when:
- Running locally without `GOOGLE_APPLICATION_CREDENTIALS` set
- Not authenticated with gcloud CLI
- No Application Default Credentials available

**Solution**: Set up credentials using one of these methods:

1. **Service Account JSON**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
   ```

2. **gcloud CLI**:
   ```bash
   gcloud auth application-default login
   ```

3. **Run on GCE instance** - No configuration needed

### Permission Denied

Ensure your service account or instance has the required permissions:
- `iam.serviceAccounts.getAccessToken` (for service accounts)
- Proper IAM bindings configured in GCP

## Migration from Old Version

The new implementation is **100% backward compatible**. If you were using `generateGcp()` on GCE instances, it will continue to work without any code changes.

The only difference is that it now **also works** with service account JSON files and other credential sources for local development.

## Comparison with AWS Authentication

Both AWS and GCP authentication methods now work consistently:

```python
from akeyless_cloud_id import CloudId

cloud_id = CloudId()

# AWS - Auto-detects credentials (boto3 session, environment variables, etc.)
aws_token = cloud_id.generate()

# GCP - Auto-detects credentials (service account, ADC, metadata server, etc.)
gcp_token = cloud_id.generateGcp()
```

Both methods automatically detect and use available credentials without requiring explicit configuration in most cases.
