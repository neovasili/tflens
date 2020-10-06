class CustomException(Exception):

  def __init__(self, message):
    super().__init__(message)
    self.__message = message

  def __str__(self):
    return str(self.__message)

class CannotLoadLocalFile(CustomException):

  def __init__(self):
    super().__init__("Cannot load local tfstate")

class CannotReadLocalFile(CustomException):

  def __init__(self):
    super().__init__("Cannot read local tfstate")

class CannotLoadRemoteFile(CustomException):

  def __init__(self):
    super().__init__("Cannot load remote tfstate")
