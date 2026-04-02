from django.http.response import Http404
from rest_framework.response import Response



def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        model_name = exc.__class__.__qualname__
        return Response({
            'detail':'Something goes wrong!!!'
        })
    return None