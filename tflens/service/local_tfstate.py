import json
import pathlib

from json.decoder import JSONDecodeError
from tflens.exception.exception import (
  CannotLoadLocalFile,
  CannotReadLocalFile
)

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
