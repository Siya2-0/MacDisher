from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed

class ApiPermission(permissions.BasePermission):
    message = "You do not have permission to perform action"
    permission_map = {
        "GET": "{app_label}.view_{model_name}",
        "POST": "{app_label}.add_{model_name}",
        "PUT": "{app_label}.change_{model_name}",
        "PATCH": "{app_label}.change_{model_name}",
        "DELETE": "{app_label}.delete_{model_name}",
    }

    def _get_permission(self, method, permission_slug):
        app, model = permission_slug.split(".")
        if method not in self.permission_map:
            raise MethodNotAllowed(method)
        perm = self.permission_map.get(method).format(app_label=app, model_name=model)
        return perm

    def has_permission(self, request, view):
        perm = self._get_permission(
            method=request.method, permission_slug=view.permission_slug
        )
        if request.user.has_perm(perm):
            return True
        return False
