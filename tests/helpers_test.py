import unittest

import io
import sys

from beautifultable import BeautifulTable
from tests_config import (
  DEFAULT_PRINT_TABLE_OUTPUT,
  MARKDOWN_PRINT_TABLE_OUTPUT,
  FILE_HTML_OUTPUT,
  VALID_MODULE_RESOURCE,
  VALID_NON_MODULE_RESOURCE,
  NON_VALID_RESOURCE
)
from tflens.model.tfstate_resource import TfStateResource
from tflens.helper.table import (
  TableHelper,
  MarkdownTableHelper,
  HtmlTableHelper
)
from tflens.helper.remote import RemoteHelper
from tflens.helper.location import (
  S3LocationHelper,
  HttpLocationHelper
)

class TestTableHelper(unittest.TestCase):

  def setUp(self):
    self.valid_module_resource = VALID_MODULE_RESOURCE
    self.valid_non_module_resource = VALID_NON_MODULE_RESOURCE
    self.non_valid_resource = NON_VALID_RESOURCE
    self.print_table_output = DEFAULT_PRINT_TABLE_OUTPUT

  def test_valid_table_with_one_row(self):
    TableHelper([TfStateResource(self.valid_module_resource)])

  def test_valid_table_with_multiple_rows(self):
    TableHelper([TfStateResource(self.valid_module_resource), TfStateResource(self.valid_non_module_resource)])

  def test_non_valid_table_with_non_valid_row(self):
    self.assertRaises(
      AttributeError,
      TableHelper,
      self.non_valid_resource
    )

  def test_set_table_valid_style(self):
    table = TableHelper([TfStateResource(self.valid_module_resource)])

    table.set_style(style=BeautifulTable.STYLE_MARKDOWN)

  def test_set_table_non_valid_style(self):
    table = TableHelper([TfStateResource(self.valid_module_resource)])

    self.assertRaises(
      ValueError,
      table.set_style,
      style="test"
    )

  def test_print_table(self):
    table = TableHelper([TfStateResource(self.valid_module_resource)])
    captured_output = io.StringIO()
    sys.stdout = captured_output
    table.print()

    self.assertEqual(captured_output.getvalue().replace('\n', ''), self.print_table_output.replace('\n', ''))

class TestMarkdownTableHelper(unittest.TestCase):

  def setUp(self):
    self.valid_module_resource = VALID_MODULE_RESOURCE
    self.print_markdowntable_output = MARKDOWN_PRINT_TABLE_OUTPUT

  def test_print_markdowntable(self):
    table = MarkdownTableHelper([TfStateResource(self.valid_module_resource)])
    captured_output = io.StringIO()
    sys.stdout = captured_output
    table.print()

    self.assertEqual(captured_output.getvalue().replace('\n', ''), self.print_markdowntable_output.replace('\n', ''))

  def test_write_markdowntable_file(self):
    table = MarkdownTableHelper([TfStateResource(self.valid_module_resource)])
    table.write_markdown_file()

    with open('.tflens/terraform.tfstate.md', 'r') as markdown_file:
      markdown_file_content = markdown_file.read()

    self.assertEqual(markdown_file_content.replace('\n', ''), self.print_markdowntable_output.replace('\n', ''))

class TestHtmlTableHelper(unittest.TestCase):

  def setUp(self):
    self.valid_module_resource = VALID_MODULE_RESOURCE
    self.print_htmltable_output = MARKDOWN_PRINT_TABLE_OUTPUT
    self.file_htmltable_output = FILE_HTML_OUTPUT

  def test_print_htmltable(self):
    table = HtmlTableHelper([TfStateResource(self.valid_module_resource)])
    captured_output = io.StringIO()
    sys.stdout = captured_output
    table.print()

    self.assertEqual(captured_output.getvalue().replace('\n', ''), self.print_htmltable_output.replace('\n', ''))

  def test_write_html_file(self):
    table = HtmlTableHelper([TfStateResource(self.valid_module_resource)])
    table.write_html_file()

    with open('.tflens/terraform.tfstate.html', 'r') as html_file:
      html_file_content = html_file.read()

    self.assertEqual(html_file_content.replace('\n', ''), self.file_htmltable_output.replace('\n', ''))

class TestRemoteHelper(unittest.TestCase):

  def setUp(self):
    self.local_file_location = 'local/terraform.tfstate'
    self.s3_file_location = 's3://local/terraform.tfstate'
    self.http_file_location = 'http://local/terraform.tfstate'
    self.https_file_location = 'https://local/terraform.tfstate'

  def test_invoke_local_remote_controller(self):
    remote_helper = RemoteHelper(self.local_file_location)

    self.assertEqual(
      remote_helper.get_remote_type(),
      "local"
    )

  def test_invoke_s3_remote_controller(self):
    remote_helper = RemoteHelper(self.s3_file_location)

    self.assertEqual(
      remote_helper.get_remote_type(),
      "s3"
    )

  def test_invoke_http_remote_controller(self):
    remote_helper = RemoteHelper(self.http_file_location)

    self.assertEqual(
      remote_helper.get_remote_type(),
      "http"
    )

  def test_invoke_https_remote_controller(self):
    remote_helper = RemoteHelper(self.https_file_location)

    self.assertEqual(
      remote_helper.get_remote_type(),
      "https"
    )

class TestLocationHelper(unittest.TestCase):

  def setUp(self):
    self.s3_file_location = 's3://local/terraform.tfstate'
    self.non_valid_s3_file_location = 's3:/local/terraform.tfstate'
    self.http_file_location = 'http://local/terraform.tfstate'
    self.non_valid_http_file_location = 'http:/local/terraform.tfstate'
    self.https_file_location = 'https://local/terraform.tfstate'
    self.non_valid_https_file_location = 'https:/local/terraform.tfstate'

  def test_valid_s3_remote_location(self):
    location_helper = S3LocationHelper(self.s3_file_location)

    self.assertTrue(location_helper.validate())

  def test_non_valid_s3_remote_location(self):
    location_helper = S3LocationHelper(self.non_valid_s3_file_location)

    self.assertFalse(location_helper.validate())

  def test_valid_http_remote_location(self):
    location_helper = HttpLocationHelper(self.http_file_location)

    self.assertTrue(location_helper.validate())

  def test_non_valid_http_remote_location(self):
    location_helper = HttpLocationHelper(self.non_valid_http_file_location)

    self.assertFalse(location_helper.validate())

  def test_valid_https_remote_location(self):
    location_helper = HttpLocationHelper(self.https_file_location)

    self.assertTrue(location_helper.validate())

  def test_non_valid_https_remote_location(self):
    location_helper = HttpLocationHelper(self.non_valid_https_file_location)

    self.assertFalse(location_helper.validate())
