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
      object_attribute_value=resource.get_parent_module()
    )

class NameFilterHelper(FilterHelper):

  def __init__(self, filter_expression: str, resource: TfStateResource):
    super().__init__(
      filter_expression=filter_expression,
      object_attribute_value=resource.get_name()
    )

class TypeFilterHelper(FilterHelper):

  def __init__(self, filter_expression: str, resource: TfStateResource):
    super().__init__(
      filter_expression=filter_expression,
      object_attribute_value=resource.get_type()
    )

class TfStateFilterHelper():

  def __init__(
    self,
    name_filter_expression: str=None,
    type_filter_expression: str=None,
    module_filter_expression: str=None,
    resources: list=None
  ):
    self.__name_filter_expression = name_filter_expression
    self.__type_filter_expression = type_filter_expression
    self.__module_filter_expression = module_filter_expression
    self.__resources = resources

  def apply_filter(self):
    filtered_list = list()

    for resource in self.__resources or []:
      pass_name_filter = True
      pass_module_filter = True
      pass_type_filter = True

      if self.__name_filter_expression:
        filter_helper = NameFilterHelper(filter_expression=self.__name_filter_expression, resource=resource)
        pass_name_filter = filter_helper.check_filter()

      if self.__type_filter_expression:
        filter_helper = TypeFilterHelper(filter_expression=self.__type_filter_expression, resource=resource)
        pass_type_filter = filter_helper.check_filter()

      if self.__module_filter_expression:
        filter_helper = ModuleFilterHelper(filter_expression=self.__module_filter_expression, resource=resource)
        pass_module_filter = filter_helper.check_filter()

      if pass_module_filter and pass_name_filter and pass_type_filter:
        filtered_list.append(resource)

    return filtered_list
