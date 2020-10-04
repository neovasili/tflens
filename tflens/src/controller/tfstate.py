from tflens.src.model.tfstate import TfState
from tflens.src.service.local_tfstate import LocalTfStateService

from tflens.src.helper.table import (
  MarkdownTableHelper,
  HtmlTableHelper
)

class TfStateController():

  def __init__(self, tfstate_content: dict):
    self.__tfstate = TfState(
      content=tfstate_content
    )

  def show_resources(self):
    table = MarkdownTableHelper(
      rows=self.__tfstate.get_resources()
    )

    table.print()

  def create_markdown_file(self):
    table = MarkdownTableHelper(
      rows=self.__tfstate.get_resources()
    )

    table.write_markdown_file()

  def create_html_file(self):
    table = HtmlTableHelper(
      rows=self.__tfstate.get_resources()
    )

    table.write_html_file()

class LocalTfStateController(TfStateController):

  def __init__(self, file_location: str):
    self.__local_tfstate_service = LocalTfStateService(
      file_location=file_location
    )

    super().__init__(
      tfstate_content=self.__local_tfstate_service.read_content()
    )
