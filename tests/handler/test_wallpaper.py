import os
import tempfile

from PIL import Image

from merls.handler.wallpaper import organize_wallpapers


def test_handle_wallpapers():
    with tempfile.TemporaryDirectory() as tmp_dir:
        size = (120, 240)

        for i in range(10):
            tmp_file = os.path.join(tmp_dir, f"{i}.jpg")
            Image.new("RGB", size).save(tmp_file)

        organize_wallpapers("A", "U", tmp_dir)

        for i in os.listdir(tmp_dir):
            assert i.startswith("[AUV]")
