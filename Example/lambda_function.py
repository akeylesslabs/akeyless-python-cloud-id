import json
import logging
import os
import time
from pprint import pprint
from urllib import request

import akeyless_api_gateway
import boto3
from akeyless_api_gateway.rest import ApiException
from akeyless_cloud_id import CloudId

# Defining the host is optional and defaults to https://127.0.0.1:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = akeyless_api_gateway.Configuration()
configuration.host="http://<api-gateway-host>:<port>"

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    codepipeline = boto3.client('codepipeline')
    job_id = "123"

    try:
        logger.info('Akeyless doing cool stuff!')
        job_id = event['CodePipeline.job']['id']

        session = boto3.session.Session()
        credentials = session.get_credentials()
        aws_access_id = credentials.access_key
        aws_secret_access_key = credentials.secret_key
        security_token = credentials.token

        api_instance = akeyless_api_gateway.DefaultApi(akeyless_api_gateway.ApiClient(configuration))

        user_parameters = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
        params = user_parameters.split(':')
        access_id = params[0]
        secret_name = params[1]
        access_type = 'aws_iam'

        cloud_id = CloudId()
        # you can also call this function with empty parameters so it will retrieve credentials by itself: cloud_id.generate()
        id = cloud_id.generate(aws_access_id, aws_secret_access_key, security_token)

        auth_response = api_instance.auth(access_id, access_type=access_type, cloud_id=id)
        token = auth_response.token

        secret_val_res = api_instance.get_secret_value(secret_name, token)
        logger.info('Secret value: ' + secret_val_res.response[0])

        response = codepipeline.put_job_success_result(jobId=job_id)

        logger.info('Akeyless doing cool stuff - Done!')
    except Exception as error:
        logger.exception(error)
        response = codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                'type': 'JobFailed',
                'message': f'{error.__class__.__name__}: {str(error)}'
            }
        )
