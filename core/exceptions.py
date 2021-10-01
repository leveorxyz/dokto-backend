from rest_framework.response import Response
from rest_framework.views import exception_handler

from .literals import INIT_CART


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)
    if response:
        data = response.data
        message_list = []
        for k, v in data.items():
            print(k)
            if isinstance(v, str):
                message_list.append(v)
            else:
                message_list.append(" ".join([str(exc) for exc in v]))
        custom_response = {
            "message": " ".join(message_list),
            "status_code": response.status_code,
        }
        response.data = custom_response
    return response


# base exception
class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
