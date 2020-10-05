class TfStateResource():

  def __init__(self, resource: dict):
    super().__init__()
    self.__resource = resource
    self.__module = None

    if 'module' in self.__resource:
      self.__module = self.__resource['module']

    self.__mode = self.__resource['mode']
    self.__type = self.__resource['type']
    self.__name = self.__resource['name']
    self.__provider = self.__resource['provider']
    self.__instances = self.__resource['instances']

  @classmethod
  def get_str_headers(cls):
    return ['provider', 'type', 'mode', 'name', 'module']

  def get_str_row(self):
    return [
      self.__provider,
      self.__type,
      self.__mode,
      self.__name,
      self.get_parent_module()
    ]

  def get_parent_module(self):
    return self.__module.split('.')[1] if self.__module else '(None)'

  def get_instances_count(self):
    return len(self.__instances)
