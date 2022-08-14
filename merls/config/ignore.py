from pydantic import BaseModel

NON_IMAGE_SUFFIXES = {".url", ".txt", ".html", ".gif", ".db", ".mov", ".mp4"}

SKIPPED_FILES = {"config.json"}


class Ignore(BaseModel):
    non_image_suffixes: set[str] = NON_IMAGE_SUFFIXES
    skipped_files: set[str] = SKIPPED_FILES
