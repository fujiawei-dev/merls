import os
import tempfile
from pathlib import Path

from merls.config.album_photo import AlbumPhotoOptions
from merls.config.ignore import Ignore
from merls.handler.album import organize_album_folders
from merls.handler.album_photo import organize_album_photos


def test_handle_photos():
    options = AlbumPhotoOptions(
        owner="test",
        album_prefix="prefix",
        album_prefix_aliases=["alias1", "alias2"],
        photo_mode=2,
        photo_prefix="prefix",
        photo_prefix_aliases=["alias1", "alias2"],
    )

    excepted = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        src = os.path.join(tmp_dir, "src")
        os.mkdir(src)

        for i in range(1, 20):
            album = os.path.join(src, f"NO.{i} album")
            os.mkdir(album)

            excepted_album = os.path.join(
                src, f"[{options.album_prefix}] NO.{i:03d} album"
            )

            excepted.append(excepted_album)

            for j in range(1, 20):
                Path(album).joinpath(f"NO.{j}.jpg").touch()
                excepted.append(
                    os.path.join(
                        excepted_album,
                        f"[{options.photo_prefix}]NO{i:03d}[{j:04d}].jpg",
                    )
                )

        organize_album_folders(src, src, options)
        organize_album_photos(src, options, Ignore())

        for excepted_dir in excepted:
            assert os.path.exists(excepted_dir)
