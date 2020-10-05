import json
import pathlib

class LocalTfStateService():

  def __init__(self, file_location: str):
    self.__file_location = None

    try:
      path = pathlib.Path(file_location)
      with path.open():
        self.__file_location = file_location

    except OSError as error:
      print(error)

  def read_content(self):
    with open(self.__file_location, 'r') as tfstate_file:
      return json.loads(tfstate_file.read())
