import unittest

from tflens.model.tfstate import TfState
from tflens.model.tfstate_resource import TfStateResource

class TestTfState(unittest.TestCase):

  def setUp(self):
    self.valid_content = {
      'version': 4,
      'terraform_version': "0.12.18",
      'serial': 153,
      'lineage': "xxxxxx-xxxx-xxx-xxxx-xxxxxx",
      'outputs': {
        'test_output': {
          'value': 'test',
          'type': 'string'
        }
      },
      'resources': [
        {
          'module': 'module.test',
          'mode': 'data',
          'type': 'aws_caller_identity',
          'name': 'current_user',
          'provider': 'provider.aws',
          'instances': [
            {
              'schema_version': 0,
              'attributes': {
                'account_id': '123456789011',
                'arn': 'arn:aws:sts::123456789011:assumed-role/test/test_user_email',
                'id': '2020-02-20 22:10:40.720934 +0000 UTC',
                'user_id': 'XXXXXXXXXXXXX:test_user_email'
              }
            }
          ]
        },
        {
          'mode': 'managed',
          'type': 'aws_dynamodb_table',
          'name': 'dynamodb-terraform-state-lock',
          'provider': 'provider.aws',
          'instances': []
        }
      ]
    }
    self.valid_content_no_resources = {
      'version': 4,
      'terraform_version': "0.12.18",
      'serial': 153,
      'lineage': "xxxxxx-xxxx-xxx-xxxx-xxxxxx",
      'outputs': {
        'test_output': {
          'value': 'test',
          'type': 'string'
        }
      },
      'resources': []
    }
    self.non_valid_content = {
      'version': 4,
      'terraform_version': "0.12.18",
      'serial': 153,
      'lineage': "xxxxxx-xxxx-xxx-xxxx-xxxxxx",
      'outputs': {
        'test_output': {
          'value': 'test',
          'type': 'string'
        }
      }
    }

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
    self.valid_module_resource = {
      'module': 'module.test',
      'mode': 'data',
      'type': 'aws_caller_identity',
      'name': 'current_user',
      'provider': 'provider.aws',
      'instances': []
    }
    self.valid_non_module_resource = {
      'mode': 'managed',
      'type': 'aws_dynamodb_table',
      'name': 'dynamodb-terraform-state-lock',
      'provider': 'provider.aws',
      'instances': []
    }
    self.non_valid_resource = {
      'mode': 'managed',
      'name': 'dynamodb-terraform-state-lock',
      'provider': 'provider.aws',
      'instances': []
    }

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
