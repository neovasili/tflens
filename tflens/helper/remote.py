from tflens.controller.tfstate import (
  RemoteS3TfStateController,
  RemoteHttpTfStateController,
  LocalTfStateController
)

class RemoteHelper():

  def __init__(self, file_location: str):
    self.__file_location = file_location
    self.__remote_router = {
      's3': RemoteS3TfStateController,
      'http': RemoteHttpTfStateController,
      'https': RemoteHttpTfStateController,
      'local': LocalTfStateController
    }
    self.__remote_type = "local"

    if ":" in self.__file_location:
      self.__remote_type = self.__file_location.split(":")[0]

  def get_remote_type(self):
    return self.__remote_type

  def invoke_remote_controller(self, **kwargs):
    return self.__remote_router[self.__remote_type](**kwargs)
