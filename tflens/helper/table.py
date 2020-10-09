import os
from pathlib import Path
import markdown
from beautifultable import BeautifulTable

from tflens.model.tfstate_resource import TfStateResource

class TableHelper():

  def __init__(self, rows: list):
    self.table = BeautifulTable(maxwidth=200)
    self.table.columns.header = TfStateResource.get_str_headers()

    for row in rows or []:
      self.table.rows.append(row.get_str_row())

    self.table.rows.sort('module')

  def set_style(self, style):
    self.table.set_style(style)

  def print(self):
    print(self.table)

class MarkdownTableHelper(TableHelper):

  def __init__(self, rows: list):
    super().__init__(rows=rows)
    self.set_style(style=BeautifulTable.STYLE_MARKDOWN)

  def write_markdown_file(self):
    Path('.tflens').mkdir(parents=True, exist_ok=True)
    markdown_file_path = '.tflens/terraform.tfstate.md'

    with open(markdown_file_path, 'w') as markdown_file:
      print(self.table, file=markdown_file)

class HtmlTableHelper(TableHelper):

  def __init__(self, rows: list):
    super().__init__(rows=rows)
    self.set_style(style=BeautifulTable.STYLE_MARKDOWN)

  def write_html_file(self):
    Path('.tflens').mkdir(parents=True, exist_ok=True)
    html_file_path = '.tflens/terraform.tfstate.html'

    markdown_file_path = '.tflens/temp.md'
    with open(markdown_file_path, 'w') as markdown_file:
      print(self.table, file=markdown_file)

    markdown.markdownFromFile(
      input=markdown_file_path,
      output=html_file_path,
      encoding='utf8',
      extensions=['markdown.extensions.tables']
    )

    os.remove(markdown_file_path)
