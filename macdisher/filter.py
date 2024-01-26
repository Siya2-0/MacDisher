
from django.db.models.fields import Field

from abc import ABC, abstractmethod

class BaseFilter(ABC):
    def __init__(self, field, default=None) -> None:
        self.enabled = False
        self.field = field
        self.default = default

    def _evaluate(self, request, query_param):
        """
        Find the specified `query_param` in the `request` and extract the value

        The filter is enabled if a value or a default value is found
        """
        value = request.GET.get(query_param, None) or request.POST.get(query_param, None)
        if value or self.default:
            self.value = value or self.default
            self.enabled = True

    def _apply(self, manager):
        """
        Apply enabled filters to the manager queryset

        Each filter needs to implement `perform` as it has to be handled on a use case
        basis
        """
        if not self.enabled:
            return manager;
        return self.perform(manager)

    def update_with_filter(self, manager, request, query_param):
        self._evaluate(request, query_param)
        return self._apply(manager)

    @abstractmethod
    def perform(self, manager):
        return manager


class BaseTextFilter(BaseFilter):
    def __init__(self, field) -> None:
      super().__init__(field)

    @abstractmethod
    def string_filter_method(self, method):
      """
      Create filter to search for the column value only

      It uses equal value check
      """
      pass

    @abstractmethod
    def string_filter(self):
      """
        Generate method for the field

        Used for like and in
      """
      pass

    def perform(self, manager):
      kwargs = None
      value = self.value
      items = value.split(",")
      if len(items) > 1:
          items = list(map(lambda a: a.strip(), items))
          kwargs = {self.string_filter_method("in"): items}
      else:
          filter_value = items[0]
          # Filter wildcard contains - *11*
          if filter_value.startswith("*") and filter_value.endswith("*"):
              kwargs = {self.string_filter_method("contains"):filter_value.replace("*", "")}
          #  Filter wildcard start with value - 123*
          elif filter_value.endswith("*"):
              kwargs = {self.string_filter_method("startswith"):filter_value.replace("*", "")}
          #  Filter wildcard end with value - *123
          elif filter_value.startswith("*"):
              kwargs = {self.string_filter_method("endswith"):filter_value.replace("*", "")}
          else:
              kwargs = {self.string_filter():filter_value}
      if kwargs:
          manager = manager.filter(**kwargs)
      return manager

class TextFilter(BaseTextFilter):
    def __init__(self, field) -> None:
        super().__init__(field)

    def string_filter(self):
      """
      Create filter to search for the column value only

      It uses equal value check
      """
      return self.field

    def string_filter_method(self, method):
        """
        Generate method for the field

        Used for like and in
        """
        return f"{self.field}__{method}"

    def perform(self, manager):
        return super().perform(manager)

class JsonTextFilter(BaseTextFilter):
    def __init__(self, column, field) -> None:
        super().__init__(field)
        self.column = column

    def string_filter(self):
      return f"{self.column}__{self.field}"

    def string_filter_method(self, method):
        print('json ', f"{self.column}__{self.field}__{method}")
        return f"{self.column}__{self.field}__{method}"

    def perform(self, manager):
        return super().perform(manager)


class IntegerFilter(BaseFilter):
    def __init__(self, field) -> None:
        super().__init__(field)

    def perform(self, manager):
        value = int(self.value)
        kwargs = {f"{self.field}":value}
        manager = manager.filter(**kwargs)
        return manager

class Pagination:
    def __init__(self, offset=0, limit=100) -> None:
        self.field_limit = 'limit'
        self.field_offset = 'offset'
        self._offset = offset
        self._limit = limit

    @property
    def offset(self):
        return self._offset

    @property
    def limit(self):
        return self._limit

    def evaluate(self, request):
        offset = request.GET.get(self.field_offset, None) or request.POST.get(self.field_offset, None)
        if offset:
            self._offset = int(offset)
        limit = request.GET.get(self.field_limit, None) or request.POST.get(self.field_limit, None)
        if limit:
            self._limit = int(limit)

def query_parse_op_filter_value(query, column:Field, value):
    print("field ", column)
    tmp = "${}"
    items = value.split(",")
    if len(items) > 1:
        query = query.filter(column.in_(items))
    #### cannot use contains for multiple entries, only specific full serials
    else:
        filter_value = items[0]
        # Filter wildcard contains - *11*
        if filter_value.startswith("*") and filter_value.endswith("*"):
            kwargs = {f"{column}__contains":filter_value.replace("*", "")}
            query = query.filter(**kwargs)
        #  Filter wildcard start with value - 123*
        elif filter_value.endswith("*"):
            kwargs = {f"{column}__endswith":filter_value.replace("*", "")}
            query = query.filter(**kwargs)
        #  Filter wildcard end with value - *123
        elif filter_value.startswith("*"):
            kwargs = {f"{column}__startswith":filter_value.replace("*", "")}
            query = query.filter(**kwargs)
        else:
            query = query.filter(column == filter_value)
    return query
