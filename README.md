# Akeyless Python Cloud Id
Retrieves cloud identity

Currently, AWS, GCP, Azure and Alibaba Cloud are supported.
In order to get cloud identity you should import this package and call the relevant method per your chosen CSP:
- AWS: "generate" (If no aws access id/key and token are provided they will be retrieved automatically from the default session.)
- GCP: "generateGcp"
- Azure: "generateAzure"
- Alibaba Cloud: "generateAlibaba" (If no access key/secret are provided they will be retrieved from environment variables or an ECS RAM role.)

## Installing
```
pip install git+https://github.com/akeylesslabs/akeyless-python-cloud-id

# if using on AWS
pip install git+https://github.com/akeylesslabs/akeyless-python-cloud-id[aws]

# if using on GCP
pip install git+https://github.com/akeylesslabs/akeyless-python-cloud-id[gcp]

# if using on Azure
pip install git+https://github.com/akeylesslabs/akeyless-python-cloud-id[azure]
```

## Usage
```
from akeyless_cloud_id import CloudId

cloud_id = CloudId()
# for AWS:
id = cloud_id.generate()
# for Azure:
id = cloud_id.generateAzure()
# for GCP:
id = cloud_id.generateGcp()
# for Alibaba Cloud:
id = cloud_id.generateAlibaba()
```

Such code can be used, for example, in order to retrieve secrets from Akeyless as part of AWS Code Pipeline:

```
import akeyless_api_gateway
from akeyless_cloud_id import CloudId

configuration = akeyless_api_gateway.Configuration()
configuration.host="http://<api-gateway-host>:<port>"

api_instance = akeyless_api_gateway.DefaultApi(akeyless_api_gateway.ApiClient(configuration))

cloud_id = CloudId()
id = cloud_id.generate()
# for Azure use: id = cloud_id.generateAzure()
# for GCP use: id = cloud_id.generateGcp()


access_id = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']

auth_response = api_instance.auth(access_id, access_type="aws_iam", cloud_id=id)
token = auth_response.token

postgresPassword = api_instance.get_secret_value("PostgresPassword", token)

```

# Build & Release

The release process is automated via GitHub Actions. There are two ways to release:

## Method 1: Tag-based Release (Recommended for Production)

1. **Update the version** in `akeyless_cloud_id/__init__.py` according to [Semantic Versioning](https://semver.org)
   - If anything changed in the dependency of packages, or in the description meant to be shown in PyPi, make sure to update the `README.rst` file accordingly!

2. **Open a PR** with your changes, get an approval and merge to **master**.

3. **Create and push a version tag** from the master branch:
   ```bash
   git checkout master
   git pull
   git tag v0.3.1  # Use the same version as in __init__.py
   git push origin v0.3.1
   ```

4. **Automated CI/CD** will validate, build, and publish to PyPI.

## Method 2: Manual Trigger from GitHub UI

1. **Go to Actions tab**: https://github.com/akeylesslabs/akeyless-python-cloud-id/actions/workflows/release.yml

2. **Click "Run workflow"**

3. **Fill in the details**:
   - **Branch**: `master` (or your target branch)
   - **Version**: `0.3.1` (or `v0.3.1` - both formats work)
   - **Auto-update version**: 
     - ☑️ **Checked**: Automatically updates `__init__.py` and commits the change
     - ☐ **Unchecked**: Validates that version in `__init__.py` already matches

4. **Click "Run workflow"** - The CI will build and publish to PyPI

### What the CI Does:

- Validates version (or auto-updates if checkbox is checked)
- Builds the distribution packages (sdist and wheel)
- Validates the artifacts with twine
- Publishes to PyPI (requires `publish-pypi` secret configured)
- Creates a GitHub release with the artifacts

## Manual Release (if needed)

If you need to release manually:

- Build pypi expected artifacts:
  ```bash
  python3 setup.py sdist bdist_wheel
  ```
- Validate artifacts:
  ```bash
  twine check dist/*
  ```
- Upload artifacts to PyPi:
  ```bash
  python3 -m twine upload dist/*
  ```