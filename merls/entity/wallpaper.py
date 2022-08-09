import os
from datetime import datetime
from pathlib import Path
from typing import Union

from PIL import Image


class WallpaperEntity(object):
    def __init__(self):
        self.used = set()

    def format_ctime(self, path: Union[str, Path]) -> str:
        ctime = int(os.path.getctime(path))
        while ctime in self.used:
            ctime += 1
        self.used.add(ctime)
        dtime = datetime.fromtimestamp(ctime)
        return dtime.strftime("%Y%m%d%H%M%S")

    @staticmethod
    def get_width_length(path: Union[str, Path]) -> tuple[int, int]:
        return Image.open(path).size
