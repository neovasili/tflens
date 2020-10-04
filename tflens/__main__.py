import os
import argparse
from pathlib import Path

from tflens.controller.tfstate import LocalTfStateController

parser = argparse.ArgumentParser(description='Ask for user specific information')

parser.add_argument('-f', '--file-location',
  type=str,
  action="store",
  dest="file_location",
  help="Location of local tfstate file. If empty then use the current folder",
  default="")

parser.add_argument('-o', '--output',
  type=str,
  action="store",
  dest="output",
  help="Defines output type (markdown|html). If empty outputs in terminal",
  default="")

# parser.add_argument('-r', '--remote',
#   action="store_true",
#   dest="remote",
#   help="If tfstate must be retrieved from remote source")

args = parser.parse_args()

# ARGS_REMOTE = args.remote
ARGS_FILE_LOCATION = args.file_location
ARGS_OUTPUT = args.output

if not ARGS_FILE_LOCATION:
  ARGS_FILE_LOCATION = "{}/terraform.tfstate.json".format(Path().absolute())

def main():
  local_tfstate_controller = LocalTfStateController(ARGS_FILE_LOCATION)

  output_router = {
    'markdown': local_tfstate_controller.create_markdown_file,
    'html': local_tfstate_controller.create_html_file,
    '': local_tfstate_controller.show_resources,
  }

  output_router[ARGS_OUTPUT]()

if __name__ == "__main__":
  main()
