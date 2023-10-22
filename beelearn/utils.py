import json
import os

from typing import Callable, TypeVar
from typing_extensions import deprecated

from django.core.files import File
from django.db.models import ImageField, QuerySet, Model
from django.utils.timezone import now, timedelta

from .settings import BASE_DIR


def get_week_start_and_end(today=None):
    """
    Get week start and end for filter based on week
    """

    if not today:
        today = now().date()

    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    return week_start, week_end


TModel = TypeVar("TModel")


def file_to_image_field(path: str):
    return File(open(path, "rb"), name=os.path.basename(path))


@deprecated
def save_file_to_image_field(
    path: str,
    model_instance: TModel,
    image_instance: Callable[[TModel], ImageField],
    base_dir=BASE_DIR,
):
    with open(base_dir / path, "rb") as file:
        # Create a Django File object from the file
        file_object = File(file)

        # Set the image_field with the file_object
        image_instance(model_instance).save(
            os.path.basename(path),
            file_object,
        )

        return file_object


def deep_merge(first: dict, second: dict):
    """
    recurvely merge two dict with second dict has higher precedence than first dict
    """
    for key, value in second.items():  # Use items() to iterate through key-value pairs
        if key in first:
            if isinstance(value, dict) and isinstance(first[key], dict):
                # Recursively merge if both values are dictionaries
                first[key] = deep_merge(first[key], value)
            else:
                # Otherwise, overwrite the value in the first dictionary
                first[key] = value
        else:
            # If the key doesn't exist in the first dictionary, add it
            first[key] = value

    return first


def serialize_deep(value: dict):
    """
    deep serializer a dict value turn array, dict into string
    """
    result = dict()

    for key, value in value.items():
        if isinstance(value, (dict, list, tuple)):
            result[key] = json.dumps(value)
        else:
            result[key] = value

    return result


def truncate_string(value: str, max_length: int = 48):
    """
    truncate a string, end a string with ellipsis when greater than `max_length`
    """
    if value is None:
        return "None"

    ellipsis = "..." if len(value) > max_length else ""

    return "%s%s" % (value[:max_length], ellipsis)


def get_update_fields(old: Model, new: Model):
    """
    get model updated fields when not available in signal
    """
    return set(
        map(
            lambda field: field.name,
            filter(
                lambda field: not field.is_relation
                and hasattr(new, field.name)
                and getattr(old, field.name) != getattr(new, field.name),
                old._meta.fields,
            ),
        ),
    )
