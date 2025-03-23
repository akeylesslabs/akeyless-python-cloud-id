# Akeyless Python Cloud Id
Retrieves cloud identity

Currently, AWS, GCP and Azure clouds are supported.
In order to get cloud identity you should import this package and call the relevant method per your chosen CSP:
- AWS: "generate" (If no aws access id/key and token are provided they will be retrieved automatically from the default session.)
- GCP: "generateGcp"
- Azure: "generateAzure"

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

If you want to release a new version, make sure to do the following:

- Update the version (`__version__`) value in `akeyless_cloud_id/__init__.py` with accordance to https://semver.org
  - If anything changed in the dependency of packages, or in the description meant to be shown in PyPi, make sure to update the README.rst file accordingly!
- Open a PR, get an approval and merge to **master**.
- Locally checkout to **master** branch
- Build pypi expected artifacts:
```
python3 setup.py sdist bdist_wheel
```
- Validate artifacts:
```
twine check dist/*
```
- Upload artifacts to PyPi:
```
python3 -m twine upload dist/*
```