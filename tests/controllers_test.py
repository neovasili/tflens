import unittest

import io
import sys
import json

from tests_config import (
  MARKDOWN_PRINT_TABLE_OUTPUT,
  FILE_HTML_OUTPUT
)
from tflens.controller.tfstate import (
  TfStateController,
  LocalTfStateController
)

EXISTING_FILE = 'resources/tests/sample.terraform.tfstate'

with open(EXISTING_FILE, 'r') as tfstate_file:
  TFSTATE_CONTENT = json.loads(tfstate_file.read())

class TestTfStateController(unittest.TestCase):

  def setUp(self):
    self.tfstate_content = TFSTATE_CONTENT
    self.print_table_output = MARKDOWN_PRINT_TABLE_OUTPUT.replace('\n', '')
    self.file_htmltable_output = FILE_HTML_OUTPUT.replace('\n', '')

  def test_show_resources(self):
    tfstate_controller = TfStateController(self.tfstate_content)
    captured_output = io.StringIO()
    sys.stdout = captured_output
    tfstate_controller.show_resources()

    self.assertEqual(captured_output.getvalue().replace('\n', ''), self.print_table_output)

  def test_create_markdown_file(self):
    tfstate_controller = TfStateController(self.tfstate_content)
    tfstate_controller.create_markdown_file()

    with open('.tflens/terraform.tfstate.md', 'r') as markdown_file:
      markdown_file_content = markdown_file.read()

    self.assertEqual(markdown_file_content.replace('\n', ''), self.print_table_output)

  def test_create_html_file(self):
    tfstate_controller = TfStateController(self.tfstate_content)
    tfstate_controller.create_html_file()

    with open('.tflens/terraform.tfstate.html', 'r') as html_file:
      html_file_content = html_file.read()

    self.assertEqual(html_file_content.replace('\n', ''), self.file_htmltable_output)

class TestLocalTfStateController(unittest.TestCase):

  def setUp(self):
    self.existing_file = EXISTING_FILE
    self.tfstate_content = TFSTATE_CONTENT
    self.print_table_output = MARKDOWN_PRINT_TABLE_OUTPUT.replace('\n', '')
    self.file_htmltable_output = FILE_HTML_OUTPUT.replace('\n', '')

  def test_local_tfstate_controller(self):
    LocalTfStateController(self.existing_file)

  def test_local_show_resources(self):
    local_tfstate_controller = LocalTfStateController(self.existing_file)
    captured_output = io.StringIO()
    sys.stdout = captured_output
    local_tfstate_controller.show_resources()

    self.assertEqual(captured_output.getvalue().replace('\n', ''), self.print_table_output)

  def test_local_show_resources_matching_module_filter(self):
    local_tfstate_controller = LocalTfStateController(
      file_location=self.existing_file,
      module_filter_expression="test"
    )
    captured_output = io.StringIO()
    sys.stdout = captured_output
    local_tfstate_controller.show_resources()

    self.assertEqual(captured_output.getvalue().replace('\n', ''), self.print_table_output)

  def test_local_show_resources_not_matching_module_filter(self):
    local_tfstate_controller = LocalTfStateController(
      file_location=self.existing_file,
      module_filter_expression="Test"
    )
    captured_output = io.StringIO()
    sys.stdout = captured_output
    local_tfstate_controller.show_resources()

    self.assertEqual(captured_output.getvalue().replace('\n', ''), '')

  def test_local_show_resources_matching_name_filter(self):
    local_tfstate_controller = LocalTfStateController(
      file_location=self.existing_file,
      name_filter_expression="current_user"
    )
    captured_output = io.StringIO()
    sys.stdout = captured_output
    local_tfstate_controller.show_resources()

    self.assertEqual(captured_output.getvalue().replace('\n', ''), self.print_table_output)

  def test_local_show_resources_not_matching_name_filter(self):
    local_tfstate_controller = LocalTfStateController(
      file_location=self.existing_file,
      name_filter_expression="Current_user"
    )
    captured_output = io.StringIO()
    sys.stdout = captured_output
    local_tfstate_controller.show_resources()

    self.assertEqual(captured_output.getvalue().replace('\n', ''), '')

  def test_local_create_markdown_file(self):
    local_tfstate_controller = LocalTfStateController(self.existing_file)
    local_tfstate_controller.create_markdown_file()

    with open('.tflens/terraform.tfstate.md', 'r') as markdown_file:
      markdown_file_content = markdown_file.read()

    self.assertEqual(markdown_file_content.replace('\n', ''), self.print_table_output)

  def test_local_create_html_file(self):
    local_tfstate_controller = LocalTfStateController(self.existing_file)
    local_tfstate_controller.create_html_file()

    with open('.tflens/terraform.tfstate.html', 'r') as html_file:
      html_file_content = html_file.read()

    self.assertEqual(html_file_content.replace('\n', ''), self.file_htmltable_output)
