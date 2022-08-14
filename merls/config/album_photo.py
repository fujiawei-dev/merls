from pathlib import Path
from typing import Optional, Tuple, Union

from pydantic import BaseModel
from toolkit.config.serialize import deserialize_from_json_file, serialize_to_json_file

from merls.logger import logging

log = logging.getLogger(__name__)


class AlbumPhotoOptions(BaseModel):
    owner: str = ""

    album_prefix: str = "prefix"
    album_prefix_aliases: list = ["alias1", "alias2"]

    photo_mode: int = 2
    photo_prefix: str = "prefix"
    photo_prefix_aliases: list = ["alias1", "alias2"]


def get_album_photo_options(
    src: Union[str, Path]
) -> Tuple[Optional[AlbumPhotoOptions], Union[str, Path]]:
    config_file = Path(src) / "config.json"

    if not config_file.is_file():
        log.error('Config file "%s" not found', config_file)
        serialize_to_json_file(AlbumPhotoOptions(), config_file)
        return None, config_file

    return deserialize_from_json_file(AlbumPhotoOptions, config_file), config_file
