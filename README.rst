########################
Akeyless Python Cloud Id
########################

Retrieves cloud identity

Currently, AWS, GCP and Azure clouds are supported.
In order to get cloud identity you should import this package and call the relevant method per your chosen CSP:
- AWS: "generate" (If no aws access id/key and token are provided they will be retrieved automatically from the default session.)
- GCP: "generateGcp"
- Azure: "generateAzure"

Minimum requirements
====================

* Python 3.5+
* urllib3 >= 1.15
* requests

Optional Dependencies
====================

* boto3
* google-auth
* azure-identity

Installation
============

.. code::
    pip install akeyless-python-cloud-id

**AWS:**

To install with AWS:

.. code::

    pip install akeyless-python-cloud-id[aws]

The following additional packages will be installed:

* boto3

**GCP:**

To install with GCP:

.. code::

    pip install akeyless-python-cloud-id[gcp]

The following additional packages will be installed:

* google-auth

To install with Azure:

.. code::

    pip install akeyless-python-cloud-id[azure]

The following additional packages will be installed:

* azure-identity

*****
Usage
*****

Such code can be used, for example, in order to retrieve secrets from Akeyless as part of AWS Code Pipeline:

.. code::
    pip install git+https://github.com/akeylesslabs/akeyless-python-sdk

    import akeyless_api_gateway
    from akeyless_cloud_id import CloudId

    configuration = akeyless_api_gateway.Configuration()
    configuration.host="http://<api-gateway-host>:<port>"

    api_instance = akeyless_api_gateway.DefaultApi(akeyless_api_gateway.ApiClient(configuration))

    cloud_id = CloudId()
    # for AWS use:
    id = cloud_id.generate()
    # For Azure use:
    id = cloud_id.generateAzure()
    # For GCP use:
    id = cloud_id.generateGcp()

    access_id = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']

    auth_response = api_instance.auth(access_id, access_type="aws_iam", cloud_id=id)
    token = auth_response.token

    postgresPassword = api_instance.get_secret_value("PostgresPassword", token)


GCP Authentication Requirements
================================

The ``generateGcp()`` method requires one of the following credential types:

**Supported:**

* ✅ **Service Account JSON**: Set ``GOOGLE_APPLICATION_CREDENTIALS`` environment variable

  .. code::

      export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

* ✅ **GCE Metadata Server**: Automatic when running on Google Compute Engine
* ✅ **Workload Identity**: Automatic when running on Google Kubernetes Engine (GKE) with Workload Identity enabled

**Not Supported:**

* ❌ **User Credentials from ADC**: Running ``gcloud auth application-default login`` creates user credentials that cannot generate ID tokens

**Workaround for User Credentials:**

If you need to use user credentials for local development, use service account impersonation:

.. code::

    gcloud auth application-default login --impersonate-service-account=SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com

This requires the ``roles/iam.serviceAccountTokenCreator`` role on the service account.


*******
License
*******
This SDK is distributed under the `Apache License, Version 2.0`_ see LICENSE.txt for more information.


.. _Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
