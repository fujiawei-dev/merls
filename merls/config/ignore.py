from pydantic import BaseModel

NON_IMAGE_SUFFIXES = {".url", ".txt", ".html", ".gif", ".db", ".mov", ".mp4"}


class Ignore(BaseModel):
    non_image_suffixes: set[str] = NON_IMAGE_SUFFIXES
