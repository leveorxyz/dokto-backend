from requests.api import delete
from rest_framework.serializers import SerializerMethodField, ModelSerializer

from .models import CoreModel


class ReadWriteSerializerMethodField(SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs["source"] = "*"
        super(SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class CustomCreateUpdateDeleteObjectOperationSerializer(ModelSerializer):
    def _operation_filter(self, data, operation):
        filtered_data = []
        if operation == "add":
            filtered_data = [
                instance for instance in data if operation == instance.get("operation")
            ]

        elif operation == "delete":
            filtered_data = [
                instance.get("id")
                for instance in data
                if operation == instance.get("operation")
            ]
        elif operation == "update":
            filtered_data = [
                instance for instance in data if operation == instance.get("operation")
            ]
        return filtered_data

    def _perform_create(
        self, data, operation_serializer: ModelSerializer, **extra_create_kwargs
    ) -> int:
        create_count = 0
        filtered_data = self._operation_filter(data, "add")
        for instance in filtered_data:
            serializer_instance = operation_serializer(
                data={**instance, **extra_create_kwargs}
            )
            serializer_instance.is_valid(raise_exception=True)
            serializer_instance.save()
            create_count += 1
        return create_count

    def _perform_delete(self, data, operation_model: CoreModel, **kwargs) -> int:
        delete_count = 0
        filtered_data = self._operation_filter(data, "delete")
        filtered_queryset = operation_model.objects.filter(
            id__in=filtered_data, **kwargs
        )
        for instance in filtered_queryset:
            instance.delete()
            delete_count += 1
        return delete_count

    def _perform_update(self, data, operation_model: CoreModel, **kwargs) -> int:
        update_count = 0
        filtered_data = self._operation_filter(data, "update")
        for instance in filtered_data:
            instance.pop("operation")
            update_count += operation_model.objects.filter(
                id=instance.pop("id"), **kwargs
            ).update(**instance)
        return update_count

    def perform_crud_operations(
        self,
        data,
        operation_serializer: ModelSerializer,
        operation_model: CoreModel,
        add_kwagrs={},
        delete_kwargs={},
        update_kwargs={},
    ) -> dict:
        return {
            "add": self._perform_create(data, operation_serializer, **add_kwagrs),
            "update": self._perform_update(data, operation_model, **update_kwargs),
            "delete": self._perform_delete(data, operation_model, **delete_kwargs),
        }

    class Meta:
        model = CoreModel
        fields = "__all__"


class FieldListUpdateSerializer(ModelSerializer):
    def perform_list_field_update(
        self,
        updated_value: list,
        related_model: CoreModel,
        field_name: str,
        query_params={},
    ) -> int:
        new_data = set(updated_value)
        old_data = set(
            related_model.objects.filter(**query_params).values_list(
                field_name, flat=True
            )
        )
        to_add = new_data - old_data
        to_delete = old_data - new_data
        related_model.objects.filter(
            **{f"{field_name}__in": to_delete}, **query_params
        ).delete()
        related_model.objects.bulk_create(
            [related_model(**{field_name: item, **query_params}) for item in to_add]
        )
        return len(to_add) + len(to_delete)

    class Meta:
        model = CoreModel
        fields = "__all__"
