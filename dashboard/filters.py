from django_filters import DateFilter, rest_framework as filters
from datetime import timedelta

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
        value += timedelta(hours=0, seconds=0, minutes=0)
        return self.lookup_filter_method(queryset, name, value, "gte")

    def created_at_lte_method(self, queryset, name, value):
        value += timedelta(hours=23, seconds=59, minutes=59)
        return self.lookup_filter_method(queryset, name, value, "lte")

    class Meta:
        model = DoctorReview
        fields = ["created_at__gte", "created_at__lte"]
