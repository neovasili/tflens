import json
from json.decoder import JSONDecodeError
import pathlib
import boto3
import requests

from botocore.exceptions import ClientError

from tflens.helper.location import (
  S3LocationHelper,
  HttpLocationHelper
)
from tflens.exception.exception import (
  CannotLoadLocalFile,
  CannotReadLocalFile,
  CannotLoadRemoteFile,
  UnauthorizedAccess,
  Forbidden,
  ServerUnavailable,
  NotValidS3Location,
  NotValidHttpLocation
)

class RemoteS3TfStateService():

  def __init__(self, file_location: str):
    location_helper = S3LocationHelper(file_location=file_location)

    if location_helper.validate():
      location_without_schema = file_location.split(":")[1].replace("//", "")

      self.__s3_client = boto3.client('s3')
      self.__bucket_name = location_without_schema.split('/')[0]
      self.__file_s3_key = "/".join(location_without_schema.split('/')[1:])

    else:
      raise NotValidS3Location

  def read_content(self):
    try:
      response = self.__s3_client.get_object(
        Bucket=self.__bucket_name,
        Key=self.__file_s3_key
      )

      return json.loads(response['Body'].read())

    except ClientError:
      raise CannotLoadRemoteFile

class RemoteHttpTfStateService():

  def __init__(self, file_location: str, user: str=None, password: str=None):
    location_helper = HttpLocationHelper(file_location=file_location)

    if location_helper.validate():
      self.__file_location = file_location
      self.__user = user
      self.__password = password

    else:
      raise NotValidHttpLocation

  def read_content(self):
    try:
      response = requests.get(
        self.__file_location,
        auth=(self.__user, self.__password),
        timeout=(5, 30)
      )

      if response.status_code == 401:
        raise UnauthorizedAccess

      if response.status_code == 403:
        raise Forbidden

      if response.status_code == 404:
        raise CannotLoadRemoteFile

      if response.status_code >= 500:
        raise ServerUnavailable

      return json.loads(response.content)

    except ClientError:
      raise CannotLoadRemoteFile

    except requests.exceptions.ConnectionError:
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
