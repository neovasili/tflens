import re

class LocationHelper():

  def __init__(self, file_location: str, validation_pattern: str):
    self.__file_location = file_location
    self.__validation_pattern = validation_pattern
    self.__compiled_pattern = re.compile(self.__validation_pattern)

  def validate(self):
    return self.__compiled_pattern.search(self.__file_location)

class S3LocationHelper(LocationHelper):

  def __init__(self, file_location: str):
    super().__init__(file_location=file_location, validation_pattern="s3\:\/\/.+\/.+")

class HttpLocationHelper(LocationHelper):

  def __init__(self, file_location: str):
    super().__init__(file_location=file_location, validation_pattern="http(s)?\:\/\/.+")
