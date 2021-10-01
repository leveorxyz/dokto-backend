from rest_framework.response import Response
from rest_framework.views import exception_handler

from .literals import INIT_CART


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)
    return response


# base exception
class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
