from tflens.model.tfstate_resource import TfStateResource

class TfState():

  def __init__(self, content: dict):
    super().__init__()
    self.__content = content
    self.__version = self.__content['version']
    self.__tf_version = self.__content['terraform_version']
    self.__serial = self.__content['serial']
    self.__lineage = self.__content['lineage']
    self.__outputs = self.__content['outputs']

    self.__get_resources(self.__content['resources'])

  def __get_resources(self, source_resources: list):
    resources = list()

    for resource in source_resources or []:
      temp_resource = TfStateResource(resource)
      resources.append(temp_resource)

    self.__resources = resources

  def get_resources_count(self):
    return len(self.__resources)

  def get_resources(self):
    return self.__resources
