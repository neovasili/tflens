import os
import sys
import stat
import shutil
import argparse
import subprocess
import urllib.request
from pathlib import Path
from zipfile import ZipFile

parser = argparse.ArgumentParser(description='Ask for user specific information')

parser.add_argument('-o', '--current-os',
  type=str,
  action="store",
  dest="current_os",
  help="Defines the current operative system to use for binaries download",
  default="darwin")

args = parser.parse_args()

CURRENT_DIR = Path().absolute()
TEST_TF_FILE = "{}/resources/tests/tf_project/test.tf".format(CURRENT_DIR)
WORKING_DIR = "{}/.temp".format(CURRENT_DIR)
CURRENT_OS = args.current_os
TF_RELEASES_URL = 'https://releases.hashicorp.com/terraform/'
TF_SUPPORTED_VERSIONS = [
  '0.12.0',
  '0.12.29',
  '0.13.0',
  '0.13.7',
  '0.14.0',
  '0.14.1',
  '0.14.2',
  '0.14.3',
  '0.14.4',
  '0.14.5',
  '0.14.6',
  '0.14.7',
  '0.14.8',
  '0.14.9',
  '0.14.10',
  '0.14.11',
  '0.15.0',
  '0.15.1',
  '0.15.2',
  '0.15.3',
  '0.15.4',
  '0.15.5',
  '1.0.0',
]

def clean_dir(zip_files_dir: str):
  if os.path.isdir(zip_files_dir):
    shutil.rmtree(zip_files_dir)

  os.mkdir(zip_files_dir)

def get_tf_zip_files_urls(current_os: str, tf_releases_url: str, tf_supported_versions: list()):
  tf_zip_files_urls = list()

  for tf_version in tf_supported_versions:
    tf_zip_file_name = "terraform_{}_{}_amd64.zip".format(tf_version, current_os)
    tf_version_url = "{}{}/{}".format(
      tf_releases_url,
      tf_version,
      tf_zip_file_name
    )
    tf_zip_files_urls.append(tf_version_url)

  return tf_zip_files_urls

def download_tf_zip_files(zip_files_dir: str, tf_zip_files_urls: list):
  for tf_zip_files_url in tf_zip_files_urls:
    filedata = urllib.request.urlopen(tf_zip_files_url)
    datatowrite = filedata.read()
    local_file = "{}/{}".format(zip_files_dir, tf_zip_files_url.split('/')[-1])

    with open(local_file, 'wb') as zip_file:
      zip_file.write(datatowrite)

def get_zip_files(zip_files_dir: str):
  zip_files = list()

  for file in os.listdir(zip_files_dir):
    if os.path.isfile(os.path.join(zip_files_dir, file)) and file.startswith('terraform_'):
      zip_files.append(file)

  return zip_files

def unzip_tf_binary(zip_files_dir: str, zip_file: str):
  tf_binary_dir = "{}/{}".format(zip_files_dir, "_".join(zip_file.split('_')[:2]))
  tf_zip_file = "{}/{}".format(zip_files_dir, zip_file)
  tf_binary_path = "{}/{}".format(tf_binary_dir, 'terraform')

  os.mkdir(tf_binary_dir)

  with ZipFile(tf_zip_file, 'r') as zip_ref:
    zip_ref.extractall(tf_binary_dir)
    os.chmod(tf_binary_path, stat.S_IXUSR | stat.S_IRUSR)

  return tf_binary_dir

def execute_command(command: str):
  process = subprocess.Popen(command.split(), stdout=sys.stdout, stderr=sys.stderr)
  process.communicate()
  return_code = process.returncode
  process.kill()

  if return_code != 0:
    print("ERROR executing the command: {}".format(command))
    sys.exit(1)

  return return_code

def main():
  clean_dir(WORKING_DIR)
  tf_zip_files_urls = get_tf_zip_files_urls(CURRENT_OS, TF_RELEASES_URL, TF_SUPPORTED_VERSIONS)
  download_tf_zip_files(WORKING_DIR, tf_zip_files_urls)
  zip_files = get_zip_files(WORKING_DIR)

  for zip_file in zip_files:
    tf_binary_dir = unzip_tf_binary(WORKING_DIR, zip_file)

    shutil.copyfile(TEST_TF_FILE, "{}/test.tf".format(tf_binary_dir))
    os.chdir(tf_binary_dir)
    print("==============================================")
    execute_command("./terraform --version")
    execute_command("./terraform init")
    execute_command("./terraform apply --auto-approve")

    os.chdir(CURRENT_DIR)
    execute_command("python3 tflens/__main__.py --file-location {}/terraform.tfstate".format(tf_binary_dir))

    print("==============================================")

if __name__ == "__main__":
  main()
