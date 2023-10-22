import datetime
from typing import Tuple

from io import BytesIO
from PIL import Image, ImageDraw, ImageOps, ImageFont

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage

from .settings import BASE_DIR


def create_mask(size: Tuple[int, int]):
    """
    create circle mask
    """
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice((0, 0, size[1], size[0]), 0, 360, fill=255)

    return mask


def create_avatar(initials: str, size: Tuple[int, int] = (256, 256)):
    """
    create avatar from initials
    """
    font = ImageFont.truetype(
        open(BASE_DIR / "beelearn/static/fonts/albert-regular.ttf", "rb"),
        size=128,
    )

    image = Image.new("RGB", size, (196, 181, 253))
    draw = ImageDraw.Draw(image)
    textbbox = draw.textbbox((0, 0), text=initials, font=font)

    image.putalpha(create_mask(size))

    draw.text(
        ((size[0] - textbbox[2]) / 2, (size[1] - textbbox[3] - 8) / 2),
        initials,
        font=font,
        fill=(255, 255, 255),
    )

    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        None,
        str(round(datetime.datetime.now().timestamp())) + ".png",
        "image/png",
        output.tell(),
        None,
    )


def circle_image(file):
    """
    Circle crop an image and resize it to fit the specified size while maintaining aspect ratio.
    """
    # Open and convert the uploaded image to RGB mode
    image = Image.open(file).convert("RGB")

    # Apply the circular mask to the image
    image.putalpha(create_mask(image.size))

    # Resize the image to fit the specified size while maintaining aspect ratio
    image = ImageOps.fit(
        image,
        image.size,
        method=0,
        bleed=0.0,
        centering=(0.5, 0.5),
    )

    # Save the resulting image to a BytesIO object
    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    # Create an InMemoryUploadedFile
    file = InMemoryUploadedFile(
        output,
        None,
        str(round(datetime.datetime.now().timestamp())) + ".png",
        "image/png",
        output.tell(),
        None,
    )

    return file


# with open("test.png", "wb") as file:
#     avatar = create_avatar(
#             "AB"
#         )
#     avatar.seek(0)
#     FileSystemStorage(location=BASE_DIR / "beelearn").save(avatar.name, avatar)
  