import json
from json.decoder import JSONDecodeError
import pathlib
import boto3

from botocore.exceptions import ClientError

from tflens.exception.exception import (
  CannotLoadLocalFile,
  CannotReadLocalFile,
  CannotLoadRemoteFile
)

class RemoteS3TfStateService():

  def __init__(self, file_location: str):
    self.__s3_client = boto3.client('s3')
    self.__bucket_name = file_location.split('/')[0]
    self.__file_s3_key = "/".join(file_location.split('/')[1:])

  def read_content(self):
    try:
      response = self.__s3_client.get_object(
        Bucket=self.__bucket_name,
        Key=self.__file_s3_key
      )
      print(response)

      return json.loads(response['Body'].read())

    except ClientError:
      raise CannotLoadRemoteFile

class LocalTfStateService():

  def __init__(self, file_location: str):
    self.__file_location = None

    try:
      path = pathlib.Path(file_location)
      with path.open():
        self.__file_location = file_location

    except OSError:
      raise CannotLoadLocalFile

  def read_content(self):
    try:
      with open(self.__file_location, 'r') as tfstate_file:
        return json.loads(tfstate_file.read())

    except JSONDecodeError:
      raise CannotReadLocalFile
