import argparse
from pathlib import Path

from tflens.controller.tfstate import (
  RemoteS3TfStateController,
  LocalTfStateController
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

parser.add_argument('-r', '--remote',
  type=str,
  action="store",
  dest="remote",
  help="Defines if remote (s3) or local tfstate file. If empty local is used. \
    When remote is defined, you also need to specify --file-location with the tfstate location \
      according to the following pattern: bucket-name/tfstate-key",
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

args = parser.parse_args()

ARGS_REMOTE = args.remote
ARGS_FILE_LOCATION = args.file_location
ARGS_OUTPUT = args.output
ARGS_FILTER_MODULE = args.filter_module
ARGS_FILTER_NAME = args.filter_name
ARGS_FILTER_TYPE = args.filter_type
ARGS_FILTER_PROVIDER = args.filter_provider
ARGS_FILER_MODE = args.filter_mode

if not ARGS_FILE_LOCATION:
  ARGS_FILE_LOCATION = "{}/terraform.tfstate".format(Path().absolute())

def main():
  remote_router = {
    's3': RemoteS3TfStateController,
    '': LocalTfStateController
  }

  tfstate_controller = remote_router[ARGS_REMOTE](
    file_location=ARGS_FILE_LOCATION,
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

  output_router[ARGS_OUTPUT]()

if __name__ == "__main__":
  main()
