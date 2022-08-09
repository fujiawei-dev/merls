import os
import tempfile
from pathlib import Path

from merls.config.album_photo import AlbumPhotoOptions
from merls.handler.album import move_albums_to_owner, organize_album_folders


def test_move_albums_to_owner():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "path")
        os.mkdir(path)

        owners_path = os.path.join(tmp_dir, "owners")
        os.mkdir(owners_path)

        owner_path = os.path.join(owners_path, "owner")
        os.mkdir(owner_path)

        owner_dirs, non_owner_dirs = [], []

        for i in range(10):
            owner_dir = os.path.join(path, f"owner{i}")
            owner_dirs.append(owner_dir)
            os.mkdir(owner_dir)

            for j in range(10):
                owner_file = os.path.join(owner_dir, f"owner{i}_{j}.jpg")
                with open(owner_file, "w") as f:
                    f.write("test")

        for i in range(10):
            owner_with_dir_dir = os.path.join(path, f"owner_with_dir{i}")
            non_owner_dirs.append(owner_with_dir_dir)
            os.mkdir(owner_with_dir_dir)

            test_dir = os.path.join(path, f"test{i}")
            non_owner_dirs.append(test_dir)
            os.mkdir(test_dir)

            for j in range(10):
                os.mkdir(os.path.join(owner_with_dir_dir, f"owner{i}_{j}"))
                owner_with_dir_file = os.path.join(
                    owner_with_dir_dir, f"owner{i}_{j}.jpg"
                )
                with open(owner_with_dir_file, "w") as f:
                    f.write("test")

                test_file = os.path.join(test_dir, f"test{i}_{j}.jpg")
                with open(test_file, "w") as f:
                    f.write("test")

        move_albums_to_owner(path, owners_path)

        for owner_dir in owner_dirs:
            assert os.path.exists(os.path.join(owner_path, os.path.basename(owner_dir)))

        for non_owner_dir in non_owner_dirs:
            assert os.path.exists(non_owner_dir)


def test_has_albums():
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

        dst = os.path.join(tmp_dir, "dst")
        os.mkdir(dst)

        for i in range(1, 20):
            Path(os.path.join(src, f"NO.{i}.jpg")).touch()
            os.mkdir(os.path.join(src, f"NO.{i} album"))
            excepted.append(
                os.path.join(src, f"[{options.album_prefix}] NO.{i:03d} album")
            )

        organize_album_folders(src, dst, options)

        assert os.path.exists(dst)

        for excepted_dir in excepted:
            assert os.path.exists(excepted_dir)

        organize_album_folders(src, dst, options)
        for excepted_dir in excepted:
            assert os.path.exists(excepted_dir)
