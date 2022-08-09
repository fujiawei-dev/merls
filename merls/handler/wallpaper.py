from pathlib import Path
from typing import Union

from merls.entity.image import clear_image_exif
from merls.entity.wallpaper import WallpaperEntity
from merls.handler.rollback import ROLLBACK_SEP, get_rollback_logger
from merls.logger import logging

log = logging.getLogger(__name__)


def organize_wallpapers(category: str, author: str, folder: Union[str, Path]) -> None:
    rollback, _ = get_rollback_logger(Path(folder).stem)

    wallpaper_entity = WallpaperEntity()

    for wallpaper in Path(folder).iterdir():
        if wallpaper.is_file():
            size = wallpaper_entity.get_width_length(wallpaper)
            new = (
                "["
                + f"{category}{author}"
                + ("H" if size[0] > size[1] else "V")
                + "]"
                + wallpaper_entity.format_ctime(wallpaper)
                + wallpaper.suffix
            )
            rollback.info(f"{wallpaper.name}{ROLLBACK_SEP}{new}")
            wallpaper = wallpaper.rename(wallpaper.parent / new)
            clear_image_exif(wallpaper, wallpaper.stem)
