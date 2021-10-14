from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)
    if response:
        data = response.data
        message_list = []
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str):
                    message_list.append(v)
                else:
                    message_list.append(" ".join([str(exc) for exc in v]))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    message_list.append(item)
                elif isinstance(item, ErrorDetail):
                    message_list.append(item.detail)
        custom_response = {
            "message": " ".join(message_list),
            "status_code": response.status_code,
            "result": None,
        }
        response.data = custom_response
    return response


# base exception
class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
