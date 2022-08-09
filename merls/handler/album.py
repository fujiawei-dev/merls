import re
from pathlib import Path
from typing import Union

from merls.config.album_photo import AlbumPhotoOptions
from merls.entity.album import DATE_PATTERN, AlbumEntity
from merls.handler.rollback import ROLLBACK_SEP, get_rollback_logger
from merls.logger import logging

log = logging.getLogger(__name__)


def move_albums_to_owner(
    path: Union[str, Path],
    owners_path: Union[str, Path],
):
    rollback, _ = get_rollback_logger(Path(path).stem)

    path, owners_path = Path(path), Path(owners_path)

    owners: dict[str, Path] = {
        owner.name.lower().partition("[")[0]: owner for owner in owners_path.iterdir()
    }

    for original_path in path.iterdir():
        if original_path.is_dir():
            if any(item.is_dir() for item in original_path.iterdir()):
                continue

            for owner in owners:
                if owner in original_path.name.lower():
                    target_path = owners[owner] / original_path.name
                    rollback.info(f"{original_path}{ROLLBACK_SEP}{target_path}")
                    original_path.rename(target_path)
                    break


def organize_album_folders(
    src: Union[str, Path],
    dst: Union[str, Path],
    options: AlbumPhotoOptions,
):
    src, dst = Path(src), Path(dst)
    owner_path = dst / (options.owner or src.name)

    rollback, _ = get_rollback_logger(src.stem)

    if not owner_path.exists():
        log.warning(f"{owner_path} not found")
        owner_path.mkdir(parents=True)

    prefix_with_brackets = f"[{options.album_prefix}]" if options.album_prefix else ""
    numbers, latest_number = AlbumEntity.get_latest_number(owner_path)

    for album in src.iterdir():
        if not album.is_dir() or (
            prefix_with_brackets and album.name.startswith(prefix_with_brackets)
        ):
            continue

        album_name = album.name

        if prefix_with_brackets == "" and album_name.startswith("["):
            album_name = album_name[album_name.find("]") + 1 :]

        for k, v in {
            options.album_prefix: "",
            "-": "",
            "）": ") ",
            "（": "(",
            "vol.": "VOL.",
            "Vol.": "VOL.",
            "no.": "NO.",
            "No.": "NO.",
        }.items():
            album_name = album_name.replace(k, v)

        for alias in options.album_prefix_aliases:
            album_name = album_name.replace(alias, "").replace("[" + alias + "]", "")

        current_number = latest_number + 1

        match_no = re.search(r"NO\.(\d+)", album_name)
        match_vol = re.search(r"VOL\.(\d+)", album_name)
        match_number = match_no or match_vol

        if match_number:
            m, n = match_number.group(0), int(match_number.group(1))
            album_name = album_name.replace(m, "")
            if n not in numbers:
                current_number = n

        while current_number in numbers:
            current_number += 1
            latest_number = current_number

        numbers.add(current_number)

        date = ""
        if match_date := DATE_PATTERN.search(album_name):
            date = "%s.%s.%s " % match_date.groups()
            album_name = album_name.replace(match_date.group(0), "")

        album_name = (
            f"{prefix_with_brackets} {date}{'NO' if not match_vol else 'VOL'}"
            f".{current_number:03d} {album_name}"
        )

        album_name = re.sub(r"\s{2,}", " ", album_name).strip()
        new_album = album.with_name(album_name)
        rollback.info(f"{album}{ROLLBACK_SEP}{new_album}")
        album.rename(new_album)
