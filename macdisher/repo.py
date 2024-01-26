from abc import ABC, abstractmethod
import json


# class BaseRepo(ABC):
#     def __init__(self, pagination=None) -> None:
#       self.filter_map = {}
#       if pagination:
#          self.pagination = Pagination()
#       else:
#          self.pagination = None

#     def register(self, filter, cls):
#       self.filter_map[filter] = cls

#     def clear_filter_map(self):
#        self.filter_map = []

#     @abstractmethod
#     def build_manager(self):
#        pass

#     @abstractmethod
#     def serialize(self, item):
#        pass

#     def list(self, request):
#       manager = self.build_manager()
#       for k,v in self.filter_map.items():
#          manager = v.update_with_filter(manager, request, k)

#       manager = manager.order_by('-created_at')

#       values = []
#       if self.pagination:
#          self.pagination.evaluate(request=request)
#          values = manager[self.pagination.offset:self.pagination.limit]
#       else:
#          values = manager[:]

#       return list(map(self.serialize, values))

#     def find_first_by_id(self, id):
#       manager = self.build_manager()
#       return self.serialize(manager.filter(id=id).first())

# class DeviceStateRepo(BaseRepo):
#     def __init__(self) -> None:
#         super().__init__(False)

#     def build_manager(self):
#       return DeviceState.objects

#     def serialize(self, item):
#       serializer = DeviceStateSerializer(item)
#       return serializer.data

#     def find_first_by_name(self, name, serialize=True):
#       item = self.build_manager().filter(name=name).first()
#       if item:
#         if serialize:
#           return self.serialize(item)
#         else:
#           return item
#       return None


# class DeviceTypeRepo(BaseRepo):
#     def __init__(self, family_code) -> None:
#         super().__init__(False)
#         self.family_code = family_code

#     def build_manager(self):
#       if self.family_code is None:
#         return DeviceType.objects
#       return DeviceType.objects.filter(family__code=self.family_code)

#     def serialize(self, item):
#       serializer = DeviceTypeSerializer(item)
#       return serializer.data

#     def find_first_by_code(self, code, serialize=True):
#       item = self.build_manager().filter(code=code).first()
#       if item:
#         if serialize:
#           return self.serialize(item)
#         else:
#           return item
#       return None

# class DeviceRepo(BaseRepo):
#     def __init__(self, family_code=None, serializer_class=DeviceSerializer) -> None:
#         super().__init__(True)
#         self.family_code = family_code
#         self.serializer_class = serializer_class
#         self.register('uuid', TextFilter('uuid'))
#         self.register('type', IntegerFilter('type'))
#         self.register('box', JsonTextFilter('meta_json', 'box'))

#     def build_manager(self):
#       if self.family_code is None:
#         return Device.objects
#       return Device.objects.filter(type__family__code=self.family_code)

#     def serialize(self, item):
#       serializer = self.serializer_class(item)
#       data = {**serializer.data}
#       return data

# # BLE4824
# class DeviceDetailsRepo(DeviceRepo):
#     def __init__(self, family_code=None, serializer_class=DeviceSerializer) -> None:
#         super().__init__(family_code, serializer_class)
#         self.family_code = family_code
#         self.clear_filter_map()

#     def device_details_manager(self, id):
#       return self.build_manager().filter(id=id)

#     def device_details(self, id):
#       """
#       Uses the device details manager to retrieve the device

#       The device is then serialized using JSON serializer
#       """
#       manager = self.device_details_manager(id)
#       device = manager.first()
#       if device:
#         d = self.serialize(device)
#         return d
#       return None

#     def serialize(self, item):
#       data = super().serialize(item)
#       data['maintenance_logs'] = list(map(self.serialize_maintenance_log,  item.maintenance_logs.all().order_by('-created_at')))
#       return data

#     def serialize_maintenance_log(self, log):
#         maintenance_serializer = MaintenanceLogSerializer(log)
#         data = {**maintenance_serializer.data}
#         return data
