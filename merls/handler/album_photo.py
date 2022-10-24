import contextlib
import os
import re
import shutil
from pathlib import Path
from typing import Union

from merls.config.album_photo import AlbumPhotoOptions
from merls.config.ignore import Ignore
from merls.entity.album_photo import NUMBER_PATTERNS
from merls.handler.rollback import ROLLBACK_SEP, get_rollback_logger
from merls.logger import logging

log = logging.getLogger(__name__)


def organize_album_photos(
    src: Union[str, Path],
    options: AlbumPhotoOptions,
    ignore: Ignore,
):
    rollback, _ = get_rollback_logger(Path(src).stem)

    prefix_with_brackets = f"[{options.photo_prefix}]" if options.photo_prefix else ""

    for album in Path(src).iterdir():
        if album.name in ignore.skipped_files:
            continue

        if not album.is_dir():
            log.warning(f"{album.name} is not a directory")
            continue

        album_name = album.name

        if options.photo_mode == 1:
            stem = "".join(album_name.split()[0:2]).replace(".", "")
        elif options.photo_mode == 2:
            stem = "".join(album_name.split()[1:2]).replace(".", "")
        elif options.photo_mode == 3:
            stem = "".join(album_name.split()[1:3]).replace(".", "")
        else:
            raise ValueError(f"unknown photo mode: {options.photo_mode}")

        numbers = set(map(int, re.findall(r"\[(\d{4})]", "".join(os.listdir(album)))))
        latest_number = 0
        folders = []

        for photo in album.iterdir():
            if photo.stem.startswith(prefix_with_brackets + stem):
                continue

            if not photo.is_file():
                print(f"{photo.name} is not a file")
                folders.append(photo)
                continue

            if photo.stem in {"cover"}:
                photo.unlink(missing_ok=True)
                continue

            suffix = photo.suffix
            if not suffix or suffix in ignore.non_image_suffixes:
                with contextlib.suppress(PermissionError):
                    photo.unlink(missing_ok=True)
                continue

            number = latest_number + 1

            for pattern in NUMBER_PATTERNS:
                match = pattern.search(photo.stem)
                if match:
                    number = int(match.group(1))
                    while number in numbers:
                        number += 1
                    numbers.add(number)
                    break

            if number == latest_number + 1:
                latest_number += 1

            if suffix == ".jpeg":
                suffix = ".jpg"

            photo_name = f"{prefix_with_brackets}{stem}[{number:04d}]{suffix}"

            if photo_name != photo.name:
                new_photo = photo.with_name(photo_name)
                rollback.info(f"{photo}{ROLLBACK_SEP}{new_photo}")
                photo.rename(new_photo)

        for folder in folders:
            for photo in folder.iterdir():
                photo.rename(folder.parent / photo.name)

            with contextlib.suppress(PermissionError):
                folder.rmdir()

            organize_album_photos(src, options, ignore)
