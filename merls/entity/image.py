import re
from enum import Enum
from pathlib import Path
from typing import Union

from pyexiv2 import Image

DOMAIN_PATTERN = re.compile(r"(http|https)?(://)?(www\.)?([^/]+?\.[^/]+)")


class ExifTags(str, Enum):
    description = "Exif.Image.ImageDescription"
    author = "Exif.Image.XPAuthor"
    comment = "Exif.Image.XPComment"
    keywords = "Exif.Image.XPKeywords"
    subject = "Exif.Image.XPSubject"
    title = "Exif.Image.XPTitle"


def clear_image_exif(path: Union[str, Path], title: str = "", author: str = ""):
    image = Image(str(path))
    exif = image.read_exif()

    for key, value in exif.items():
        if (
            "http" in value
            or "www" in value
            or ".com" in value
            or DOMAIN_PATTERN.match(value)
        ):
            exif[key] = ""

    if not exif.get(ExifTags.title.value):
        exif[ExifTags.title.value] = title

    if not exif.get(ExifTags.author.value):
        exif[ExifTags.author.value] = author

    image.modify_exif(exif)


def clear_images_exif_recursively(path: Union[str, Path]):
    for item in Path(path).iterdir():
        if item.iterdir():
            clear_images_exif_recursively(item)
        elif item.is_file() and item.suffix in {".jpg", ".jpeg", ".png"}:
            clear_image_exif(item, item.stem)
