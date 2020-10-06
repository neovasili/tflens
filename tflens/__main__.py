import argparse
from pathlib import Path

from tflens.controller.tfstate import (
  RemoteS3TfStateController,
  LocalTfStateController
)

parser = argparse.ArgumentParser(description='Ask for user specific information')

parser.add_argument('-f', '--file-location',
  type=str,
  action="store",
  dest="file_location",
  help="Defines the location of the tfstate file. If empty then use the current_folder/terraform.tfstate.json",
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
  help="Defines if remote (s3) or local tfstate file. If empty local is used",
  default="")

args = parser.parse_args()

ARGS_REMOTE = args.remote
ARGS_FILE_LOCATION = args.file_location
ARGS_OUTPUT = args.output

if not ARGS_FILE_LOCATION:
  ARGS_FILE_LOCATION = "{}/terraform.tfstate.json".format(Path().absolute())

def main():
  remote_router = {
    's3': RemoteS3TfStateController,
    '': LocalTfStateController
  }

  tfstate_controller = remote_router[ARGS_REMOTE](ARGS_FILE_LOCATION)

  output_router = {
    'markdown': tfstate_controller.create_markdown_file,
    'html': tfstate_controller.create_html_file,
    '': tfstate_controller.show_resources,
  }

  output_router[ARGS_OUTPUT]()

if __name__ == "__main__":
  main()
