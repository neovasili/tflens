from tflens.model.tfstate import TfState
from tflens.service.tfstate import (
  RemoteS3TfStateService,
  RemoteHttpTfStateService,
  LocalTfStateService
)
from tflens.helper.table import (
  MarkdownTableHelper,
  HtmlTableHelper
)
from tflens.helper.filter import TfStateFilterHelper

class TfStateController():

  def __init__(
    self,
    tfstate_content: dict,
    name_filter_expression: str=None,
    type_filter_expression: str=None,
    provider_filter_expression: str=None,
    module_filter_expression: str=None,
    mode_filter_expression: str=None
  ):
    self.__tfstate = TfState(
      content=tfstate_content
    )
    self.__resources = TfStateFilterHelper(
      name_filter_expression=name_filter_expression,
      type_filter_expression=type_filter_expression,
      provider_filter_expression=provider_filter_expression,
      module_filter_expression=module_filter_expression,
      mode_filter_expression=mode_filter_expression,
      resources=self.__tfstate.get_resources()
    ).apply_filter()

  def show_resources(self, show_columns: list = None):
    table = MarkdownTableHelper(
      rows=self.__resources,
      show_columns=show_columns,
    )

    table.print()

  def create_markdown_file(self, show_columns: list = None):
    table = MarkdownTableHelper(
      rows=self.__resources,
      show_columns=show_columns,
    )

    table.write_markdown_file()

  def create_html_file(self, show_columns: list = None):
    table = HtmlTableHelper(
      rows=self.__resources,
      show_columns=show_columns,
    )

    table.write_html_file()

class LocalTfStateController(TfStateController):

  def __init__(
    self,
    file_location: str,
    user: str=None,
    password: str=None,
    module_filter_expression: str=None,
    type_filter_expression: str=None,
    provider_filter_expression: str=None,
    name_filter_expression: str=None,
    mode_filter_expression: str=None
  ):
    self.__local_tfstate_service = LocalTfStateService(
      file_location=file_location
    )
    user = str(user)
    password = str(password)

    super().__init__(
      tfstate_content=self.__local_tfstate_service.read_content(),
      name_filter_expression=name_filter_expression,
      type_filter_expression=type_filter_expression,
      provider_filter_expression=provider_filter_expression,
      module_filter_expression=module_filter_expression,
      mode_filter_expression=mode_filter_expression
    )

class RemoteS3TfStateController(TfStateController):

  def __init__(
    self,
    file_location: str,
    user: str=None,
    password: str=None,
    module_filter_expression: str=None,
    type_filter_expression: str=None,
    provider_filter_expression: str=None,
    name_filter_expression: str=None,
    mode_filter_expression: str=None
  ):
    self.__remote_s3_tfstate_service = RemoteS3TfStateService(
      file_location=file_location
    )
    user = str(user)
    password = str(password)

    super().__init__(
      tfstate_content=self.__remote_s3_tfstate_service.read_content(),
      name_filter_expression=name_filter_expression,
      type_filter_expression=type_filter_expression,
      provider_filter_expression=provider_filter_expression,
      module_filter_expression=module_filter_expression,
      mode_filter_expression=mode_filter_expression
    )

class RemoteHttpTfStateController(TfStateController):

  def __init__(
    self,
    file_location: str,
    user: str=None,
    password: str=None,
    module_filter_expression: str=None,
    type_filter_expression: str=None,
    provider_filter_expression: str=None,
    name_filter_expression: str=None,
    mode_filter_expression: str=None
  ):
    self.__remote_http_tfstate_service = RemoteHttpTfStateService(
      file_location=file_location,
      user=user,
      password=password
    )

    super().__init__(
      tfstate_content=self.__remote_http_tfstate_service.read_content(),
      name_filter_expression=name_filter_expression,
      type_filter_expression=type_filter_expression,
      provider_filter_expression=provider_filter_expression,
      module_filter_expression=module_filter_expression,
      mode_filter_expression=mode_filter_expression
    )
