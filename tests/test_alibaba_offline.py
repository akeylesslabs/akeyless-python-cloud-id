"""Hermetic offline tests for CloudId.generateAlibaba()."""

import base64
import json
from urllib.parse import parse_qs, urlparse

from akeyless_cloud_id import CloudId
from akeyless_cloud_id import cloud_id as cloud_id_module


TEST_TIMESTAMP = "2026-05-11T10:00:00Z"
TEST_NONCE = "fixed-nonce"


def _decode_envelope(token):
    return json.loads(base64.b64decode(token))


def _query(url):
    return {k: v[0] for k, v in parse_qs(urlparse(url).query, keep_blank_values=True).items()}


def _cloud_id(region="cn-hangzhou", security_token=""):
    return CloudId().generateAlibaba(
        access_key_id="AKID",
        access_key_secret="SECRET",
        security_token=security_token,
        region=region,
        timestamp=TEST_TIMESTAMP,
        nonce=TEST_NONCE,
    )


def test_generate_alibaba_default_region():
    env = _decode_envelope(_cloud_id(region=""))
    assert env["sts_request_method"] == "POST"
    url = base64.b64decode(env["sts_request_url"]).decode()
    assert url.startswith("https://sts.aliyuncs.com/?")
    assert base64.b64decode(env["sts_request_body"]).decode() == ""
    query = _query(url)
    assert query["RegionId"] == cloud_id_module._ALIBABA_DEFAULT_REGION
    assert query["Action"] == cloud_id_module._ALIBABA_STS_API_ACTION
    assert query["Version"] == cloud_id_module._ALIBABA_STS_API_VERSION
    assert query["Signature"]


def test_generate_alibaba_configured_region():
    env = _decode_envelope(_cloud_id(region="cn-beijing"))
    url = base64.b64decode(env["sts_request_url"]).decode()
    assert _query(url)["RegionId"] == "cn-beijing"


def test_generate_alibaba_includes_security_token():
    env = _decode_envelope(_cloud_id(security_token="SESSION"))
    url = base64.b64decode(env["sts_request_url"]).decode()
    assert _query(url)["SecurityToken"] == "SESSION"


def test_generate_alibaba_payload_headers():
    env = _decode_envelope(_cloud_id())
    headers = json.loads(base64.b64decode(env["sts_request_headers"]))
    assert headers["Content-Type"][0] == "application/x-www-form-urlencoded"
    assert headers["X-Acs-Action"][0] == cloud_id_module._ALIBABA_STS_API_ACTION
    assert headers["X-Acs-Version"][0] == cloud_id_module._ALIBABA_STS_API_VERSION


def test_alibaba_rpc_string_to_sign_is_deterministic():
    query_params = {
        "AccessKeyId": "AKID",
        "Action": cloud_id_module._ALIBABA_STS_API_ACTION,
        "Format": cloud_id_module._ALIBABA_STS_API_FORMAT,
        "RegionId": cloud_id_module._ALIBABA_DEFAULT_REGION,
        "SignatureMethod": cloud_id_module._ALIBABA_SIGNATURE_METHOD,
        "SignatureNonce": TEST_NONCE,
        "SignatureType": "",
        "SignatureVersion": "1.0",
        "Timestamp": TEST_TIMESTAMP,
        "Version": cloud_id_module._ALIBABA_STS_API_VERSION,
    }
    string_to_sign = cloud_id_module._alibaba_rpc_string_to_sign("POST", query_params)
    signature = cloud_id_module._alibaba_sha_hmac1(string_to_sign, "SECRET&")
    assert string_to_sign == (
        "POST&%2F&AccessKeyId%3DAKID%26Action%3DGetCallerIdentity%26Format%3DJSON"
        "%26RegionId%3Dcn-hangzhou%26SignatureMethod%3DHMAC-SHA1%26SignatureNonce%3Dfixed-nonce"
        "%26SignatureType%3D%26SignatureVersion%3D1.0%26Timestamp%3D2026-05-11T10%253A00%253A00Z"
        "%26Version%3D2015-04-01"
    )
    assert signature == "dSCqL2sSKYDmcOcAj2Grhpar/wE="
