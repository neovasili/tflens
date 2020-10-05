import unittest

from tflens.service.local_tfstate import LocalTfStateService
from tflens.exception.exception import (
  CannotLoadLocalFile,
  CannotReadLocalFile
)

class TestLocalTfStateService(unittest.TestCase):

  def setUp(self):
    self.existing_file = 'resources/tests/terraform.tfstate.json'
    self.broken_file = 'resources/tests/broken_terraform.tfstate.json'
    self.non_existing_file = 'resources/tests/fake_terraform.tfstate.json'

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
