import json
import unittest
import requests_mock
import boto3

from moto import mock_s3

from tests_config import (
  VALID_TFSTATE_CONTENT_WITH_RESOURCES
)
from tflens.service.tfstate import (
  RemoteS3TfStateService,
  RemoteHttpTfStateService,
  LocalTfStateService
)
from tflens.exception.exception import (
  CannotLoadLocalFile,
  CannotReadLocalFile,
  CannotLoadRemoteFile
)

@mock_s3
class TestRemoteS3TfStateService(unittest.TestCase):

  def setUp(self):
    self.bucket = 'tflens-test-bucket'
    self.valid_content_key = 'tflens/terraform.tfstate'
    self.non_valid_key = 'none'

    self.valid_tfstate_file = "{}/{}".format(self.bucket, self.valid_content_key)
    self.non_existing_tfstate_file = "{}/{}".format(self.bucket, self.non_valid_key)

    with mock_s3():
      s3 = boto3.client("s3")
      s3.create_bucket(
        Bucket=self.bucket,
        CreateBucketConfiguration={
          'LocationConstraint': 'eu-west-1'
        }
      )
      s3.put_object(
        Bucket=self.bucket,
        Key=self.valid_content_key,
        Body=json.dumps(VALID_TFSTATE_CONTENT_WITH_RESOURCES)
      )

  def test_read_content_remote_s3_file(self):
    remote_s3_tfstate_service = RemoteS3TfStateService(self.valid_tfstate_file)
    content = remote_s3_tfstate_service.read_content()

    self.assertIsInstance(content, dict)

  def test_cannot_load_content_remote_s3_file(self):
    remote_s3_tfstate_service = RemoteS3TfStateService(self.non_existing_tfstate_file)
    self.assertRaises(
      CannotLoadRemoteFile,
      remote_s3_tfstate_service.read_content
    )

class TestRemoteHttpTfStateService(unittest.TestCase):

  @requests_mock.mock()
  def setUp(self, mock):
    self.valid_tfstate_file = "http://valid_tfstate_file"
    self.non_existing_tfstate_file = "http://non_existing_tfstate_file"
    self.user = "user"
    self.password = "password"

    mock.get(
      self.valid_tfstate_file,
      json=VALID_TFSTATE_CONTENT_WITH_RESOURCES
    )

    mock.get(
      self.non_existing_tfstate_file,
      json=""
    )
    self.remote_http_tfstate_service = RemoteHttpTfStateService(self.valid_tfstate_file, self.user, self.password)
    self.valid_content = self.remote_http_tfstate_service.read_content()

  def test_read_content_remote_http_file(self):
    self.assertIsInstance(self.valid_content, dict)

  def test_cannot_load_content_remote_http_file(self):
    remote_http_tfstate_service = RemoteHttpTfStateService(self.non_existing_tfstate_file)
    self.assertRaises(
      CannotLoadRemoteFile,
      remote_http_tfstate_service.read_content
    )

class TestLocalTfStateService(unittest.TestCase):

  def setUp(self):
    self.existing_file = 'resources/tests/terraform.tfstate'
    self.broken_file = 'resources/tests/broken_terraform.tfstate'
    self.non_existing_file = 'resources/tests/fake_terraform.tfstate'

  def test_open_existing_local_file(self):
    LocalTfStateService(self.existing_file)

  def test_fail_open_non_existing_local_file(self):
    self.assertRaises(
      CannotLoadLocalFile,
      LocalTfStateService,
      self.non_existing_file
    )

  def test_read_content_local_file(self):
    local_tfstate_service = LocalTfStateService(self.existing_file)
    content = local_tfstate_service.read_content()

    self.assertIsInstance(content, dict)

  def test_cannot_read_content_local_file(self):
    local_tfstate_service = LocalTfStateService(self.broken_file)

    self.assertRaises(
      CannotReadLocalFile,
      local_tfstate_service.read_content
    )
