from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from rest_framework.serializers import Field

class ContentTypeField(Field):
    def to_representation(self, instance):
        return instance.model

    def to_internal_value(self, value: str):
        return get_object_or_404(ContentType, model=value)


class GenericForeignKeyField(Field):
    def __init__(self, serializers):
        self.serializers = serializers

        super().__init__()

    def to_representation(self, instance):
        serializer = self.serializers.get(instance.__class__)

        if not serializer:
            self.fail(
                self.fk_field.ct_field,
                msg="A valid serializer not found for model %s"
                % instance._meta.model_name,
            )

        return serializer(instance).data

    @property
    def fk_field(self) -> GenericForeignKey:
        if hasattr(self, "_fk_field") is None:
            return self._fk_field

        self._fk_field = next(
            filter(
                lambda field: field.name == self.field_name,
                self.parent.Meta.model._meta.get_fields(True, True),
            ),
        )

        return self._fk_field

    def to_internal_value(self, value):
        initial_data = self.parent.initial_data
        if isinstance(initial_data, list):
            return

        content_type_field = initial_data.get(self.fk_field.ct_field)

        if not content_type_field:
            self.fail(
                self.field_name,
                msg="%s is required" % self.fk_field.ct_field,
            )

        content_type = ContentType.objects.get(model=content_type_field)
        model_class = content_type.model_class()

        serializer = self.serializers.get(model_class)(
            data=value,
            context=self.context,
        )

        if not serializer:
            self.fail(
                self.fk_field.ct_field,
                msg="This not a valid content_type",
            )

        serializer.is_valid()
        instance = serializer.save()
        self.parent.initial_data[self.fk_field.fk_field] = instance
        return instance
