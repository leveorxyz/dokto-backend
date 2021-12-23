from django_filters import DateFilter, rest_framework as filters

from user.models import DoctorReview


class ReviewFilter(filters.FilterSet):
    created_at__gte = DateFilter(
        field_name="created_at", lookup_expr="gte", input_formats=["%Y-%m-%d"]
    )
    created_at__lte = DateFilter(
        field_name="created_at", lookup_expr="lte", input_formats=["%Y-%m-%d"]
    )

    class Meta:
        model = DoctorReview
        fields = ["created_at__gte", "created_at__lte"]
