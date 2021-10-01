from typing import OrderedDict
from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    def get_offset_from_url(self, url: str):
        if not url:
            return None
        params = url.split("?")[-1]
        offset = params.split("&")[-1].split("=")[-1]
        return offset

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        raw_data = response.data
        previous_offset = self.get_offset_from_url(raw_data["previous"])
        next_offset = self.get_offset_from_url(raw_data["next"])
        raw_data.update(
            {
                "previous_offset": previous_offset,
                "next_offset": next_offset,
            }
        )
        response.data = OrderedDict(
            [("message", "success"), ("status_code", 200), ("response", raw_data)]
        )
        return response
