# Akeyless Python Cloud Id
Retrieves cloud identity

Currently only AWS cloud supported. In order to get cloud identity you should import this package and call to generate method. 
If no aws access id/key and token provided they will be retrieved authomatically from default session.

```
pip install git+https://github.com/akeylesslabs/akeyless-python-cloud-id
```

```
from akeyless_cloud_id import CloudId

cloud_id = CloudId()
id = cloud_id.generate()
```

Such code can be used, for example, in order to retrieve secrets from Akeyless as part of AWS Code Pipeline:

```
pip install git+https://github.com/akeylesslabs/akeyless-python-sdk
```

```
import akeyless_api_gateway
from akeyless_cloud_id import CloudId

configuration = akeyless_api_gateway.Configuration()
configuration.host="http://<api-gateway-host>:<port>"

api_instance = akeyless_api_gateway.DefaultApi(akeyless_api_gateway.ApiClient(configuration))

cloud_id = CloudId()
id = cloud_id.generate()

access_id = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']

auth_response = api_instance.auth(access_id, access_type="aws_iam", cloud_id=id)
token = auth_response.token

postgresPassword = api_instance.get_secret_value("PostgresPassword", token)

```
