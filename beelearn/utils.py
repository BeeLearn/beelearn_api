import os
from typing import Callable, TypeVar

from django.core.files import File
from django.db.models import ImageField
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
            save=True,
        )

TModel = TypeVar("TModel")


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
            save=True,
        )