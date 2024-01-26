from rest_framework.response import Response
from rest_framework import status
from production.dto import failed

def fields_required(serializer):
  return Response(failed(serializer.errors, "FIELDS_REQUIRED"), status=status.HTTP_406_NOT_ACCEPTABLE)
