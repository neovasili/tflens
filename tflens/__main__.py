import sys
import argparse

from pathlib import Path

from tflens.helper.config import VERSION
from tflens.helper.remote import RemoteHelper

from tflens.exception.exception import (
  NotExistingColumn,
  NotEmptyColumnsToShow,
)

parser = argparse.ArgumentParser(
  description='Terraform lens is a CLI tool that enables developers have a summarized view of tfstate resources.'
)

parser.add_argument('-f', '--file-location',
  type=str,
  action="store",
  dest="file_location",
  help="Defines the location (remote or local) of the tfstate file. \
    Mandatory if remote tfstate is selected. \
      If empty then use the current_folder/terraform.tfstate",
  default="")

parser.add_argument('-o', '--output',
  type=str,
  action="store",
  dest="output",
  help="Defines output type (markdown|html). If empty outputs in terminal",
  default="")

parser.add_argument('-s', '--show-columns',
  type=str,
  action="store",
  dest="show_columns",
  help="Comma separated string list with columns to show in output. \
    Default list is: 'provider,type,mode,name,module'",
  default="")

parser.add_argument('-m', '--filter-module',
  type=str,
  action="store",
  dest="filter_module",
  help="Applies a regular expression to the module field in order to \
    filter the resources list to output",
  default="")

parser.add_argument('-n', '--filter-name',
  type=str,
  action="store",
  dest="filter_name",
  help="Applies a regular expression to the name field in order to \
    filter the resources list to output",
  default="")

parser.add_argument('-t', '--filter-type',
  type=str,
  action="store",
  dest="filter_type",
  help="Applies a regular expression to the type field in order to \
    filter the resources list to output",
  default="")

parser.add_argument('-p', '--filter-provider',
  type=str,
  action="store",
  dest="filter_provider",
  help="Applies a regular expression to the provider field in order to \
    filter the resources list to output",
  default="")

parser.add_argument('-d', '--filter-mode',
  type=str,
  action="store",
  dest="filter_mode",
  help="Applies a regular expression to the mode field in order to \
    filter the resources list to output",
  default="")

parser.add_argument('-u', '--http-user',
  type=str,
  action="store",
  dest="http_user",
  help="User for http remote backend basic auth",
  default="")

parser.add_argument('-w', '--http-password',
  type=str,
  action="store",
  dest="http_password",
  help="Password for http remote backend basic auth",
  default="")

parser.add_argument('-v', '--version',
  action='version',
  help="Show program version",
  version=VERSION)

args = parser.parse_args()

ARGS_FILE_LOCATION = args.file_location
ARGS_OUTPUT = args.output
ARGS_SHOW_COLUMNS = args.show_columns
ARGS_FILTER_MODULE = args.filter_module
ARGS_FILTER_NAME = args.filter_name
ARGS_FILTER_TYPE = args.filter_type
ARGS_FILTER_PROVIDER = args.filter_provider
ARGS_FILER_MODE = args.filter_mode
ARGS_HTTP_USER = args.http_user if args.http_user else None
ARGS_HTTP_PASSWORD = args.http_password if args.http_password else None

if not ARGS_FILE_LOCATION:
  ARGS_FILE_LOCATION = "{}/terraform.tfstate".format(Path().absolute())

def main():
  remote_helper = RemoteHelper(ARGS_FILE_LOCATION)

  tfstate_controller = remote_helper.invoke_remote_controller(
    file_location=ARGS_FILE_LOCATION,
    user=ARGS_HTTP_USER,
    password=ARGS_HTTP_PASSWORD,
    name_filter_expression=ARGS_FILTER_NAME,
    type_filter_expression=ARGS_FILTER_TYPE,
    provider_filter_expression=ARGS_FILTER_PROVIDER,
    module_filter_expression=ARGS_FILTER_MODULE,
    mode_filter_expression=ARGS_FILER_MODE
  )

  output_router = {
    'markdown': tfstate_controller.create_markdown_file,
    'html': tfstate_controller.create_html_file,
    '': tfstate_controller.show_resources,
  }

  show_columns = None

  if ARGS_SHOW_COLUMNS != "":
    show_columns = ARGS_SHOW_COLUMNS.split(',')

  try:
    output_router[ARGS_OUTPUT](show_columns=show_columns)

  except (NotExistingColumn, NotEmptyColumnsToShow) as error:
    print(str(error))
    sys.exit(1)

if __name__ == "__main__":
  main()
