from django_filters import DateFilter, rest_framework as filters
from datetime import datetime, timedelta

from user.models import DoctorReview


class ReviewFilter(filters.FilterSet):
    created_at__gte = DateFilter(
        field_name="created_at",
        input_formats=["%Y-%m-%d"],
        method="created_at_gte_method",
    )
    created_at__lte = DateFilter(
        field_name="created_at",
        input_formats=["%Y-%m-%d"],
        method="created_at_lte_method",
    )

    def lookup_filter_method(self, queryset, name, value, lookup_exp):
        return queryset.filter(**{f"{name}__{lookup_exp}": value})

    def created_at_gte_method(self, queryset, name, value):
        return self.lookup_filter_method(queryset, name, value, "gte")

    def created_at_lte_method(self, queryset, name, value):
        parsed_value = value.strftime("%Y-%m-%d")
        parsed_value += "T23:59:59Z"
        parsed_value = datetime.strptime(parsed_value, "%Y-%m-%dT%H:%M:%SZ")
        return self.lookup_filter_method(queryset, name, parsed_value, "lte")

    class Meta:
        model = DoctorReview
        fields = ["created_at__gte", "created_at__lte"]
