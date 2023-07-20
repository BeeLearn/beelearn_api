import os
from typing import Callable, TypeVar

from django.core.files import File
from django.db.models import ImageField

from .settings import BASE_DIR

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
