import unittest

from tests_config import (
  VALID_TFSTATE_CONTENT_WITH_RESOURCES,
  VALID_TFSTATE_CONTENT_NO_RESOURCES,
  NON_VALID_TFSTATE_CONTENT,
  VALID_MODULE_RESOURCE,
  VALID_NON_MODULE_RESOURCE,
  NON_VALID_RESOURCE
)
from tflens.model.tfstate import TfState
from tflens.model.tfstate_resource import TfStateResource

class TestTfState(unittest.TestCase):

  def setUp(self):
    self.valid_content = VALID_TFSTATE_CONTENT_WITH_RESOURCES
    self.valid_content_no_resources = VALID_TFSTATE_CONTENT_NO_RESOURCES
    self.non_valid_content = NON_VALID_TFSTATE_CONTENT

  def test_valid_tfstate_content(self):
    TfState(self.valid_content)

  def test_non_valid_tfstate_content(self):
    self.assertRaises(
      KeyError,
      TfState,
      self.non_valid_content
    )

  def test_count_tfstate_resources(self):
    tfstate = TfState(self.valid_content)

    self.assertEqual(tfstate.get_resources_count(), 2)

  def test_count_tfstate_empty_resources(self):
    tfstate = TfState(self.valid_content_no_resources)

    self.assertEqual(tfstate.get_resources_count(), 0)

  def test_get_tfstate_resources_list(self):
    tfstate = TfState(self.valid_content)

    self.assertIsInstance(tfstate.get_resources(), list)

class TestTfStateResource(unittest.TestCase):

  def setUp(self):
    self.valid_module_resource = VALID_MODULE_RESOURCE
    self.valid_non_module_resource = VALID_NON_MODULE_RESOURCE
    self.non_valid_resource = NON_VALID_RESOURCE

  def test_valid_module_resource(self):
    tfstate_resource = TfStateResource(self.valid_module_resource)

    self.assertEqual(tfstate_resource.get_parent_module(), 'test')

  def test_valid_non_module_resource(self):
    tfstate_resource = TfStateResource(self.valid_non_module_resource)

    self.assertEqual(tfstate_resource.get_parent_module(), '(None)')

  def test_non_valid_resource(self):
    self.assertRaises(
      KeyError,
      TfStateResource,
      self.non_valid_resource
    )

  def test_str_columns_length(self):
    tfstate_resource = TfStateResource(self.valid_module_resource)

    self.assertEqual(
      len(tfstate_resource.get_str_headers()),
      len(tfstate_resource.get_str_row())
    )

  def test_instances_count_empty_resource(self):
    tfstate_resource = TfStateResource(self.valid_module_resource)

    self.assertEqual(tfstate_resource.get_instances_count(), 0)
