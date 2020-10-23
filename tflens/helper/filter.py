import re

from tflens.model.tfstate_resource import TfStateResource

class FilterHelper():

  def __init__(self, filter_expression: str, object_attribute_value: str):
    self.__filter_expression = filter_expression
    self.__object_attribute_value = object_attribute_value

  def check_filter(self):
    return re.match(self.__filter_expression, self.__object_attribute_value)

class ModuleFilterHelper(FilterHelper):

  def __init__(self, filter_expression: str, resource: TfStateResource):
    super().__init__(
      filter_expression=filter_expression,
      object_attribute_value = resource.get_parent_module()
    )

class TfStateFilterHelper():

  def __init__(self, module_filter_expression: str=None, resources: list=None):
    self.__module_filter_expression = module_filter_expression
    self.__resources = resources

  def apply_filter(self):
    filtered_list = list()

    for resource in self.__resources or []:
      pass_module_filter = True

      if self.__module_filter_expression:
        filter_helper = ModuleFilterHelper(filter_expression=self.__module_filter_expression, resource=resource)
        pass_module_filter = filter_helper.check_filter()

      if pass_module_filter:
        filtered_list.append(resource)

    return filtered_list
