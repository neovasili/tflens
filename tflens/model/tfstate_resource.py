from tflens.exception.exception import NotExistingColumn


class TfStateResource():

  def __init__(self, resource: dict):
    super().__init__()
    self.__resource = resource
    self.__module = '-'

    if 'module' in self.__resource:
      self.__module = self.__resource['module'].split('.')[1]

  def get_str_row(self, show_columns: list = None):
    result = list()
    for column in show_columns:
      if column == 'module':
        value = self.__module
      else:
        if column not in self.__resource:
          raise NotExistingColumn(column_name=column)

        value = self.__resource[column]

      result.append(value)

    return result

  def get_name(self):
    return self.__resource['name']

  def get_type(self):
    return self.__resource['type']

  def get_provider(self):
    return self.__resource['provider']

  def get_mode(self):
    return self.__resource['mode']

  def get_parent_module(self):
    return self.__module

  def get_instances_count(self):
    return len(self.__resource['instances'])
