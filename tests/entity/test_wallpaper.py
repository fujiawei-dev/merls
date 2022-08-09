import os
import tempfile

from PIL import Image

from merls.entity.wallpaper import WallpaperEntity


def test_format_ctime():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, "test.jpg")
        wallpaper = WallpaperEntity()
        with open(tmp_file, "w") as f:
            f.write("test")
        assert wallpaper.format_ctime(tmp_file).isnumeric()


def test_get_width_length():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, "test.jpg")
        size = (120, 240)
        Image.new("RGB", size).save(tmp_file)
        assert WallpaperEntity.get_width_length(tmp_file) == size
