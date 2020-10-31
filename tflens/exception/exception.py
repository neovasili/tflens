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

class UnauthorizedAccess(CustomException):

  def __init__(self):
    super().__init__("Unauthorized access, check your auth credentials")

class Forbidden(CustomException):

  def __init__(self):
    super().__init__("Forbidden, your user does not have sufficient permissions")

class ServerUnavailable(CustomException):

  def __init__(self):
    super().__init__("The server is unavailable")
