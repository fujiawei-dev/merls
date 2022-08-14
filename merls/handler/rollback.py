import logging.handlers
import os
import time
from pathlib import Path
from typing import Tuple, Union

from merls.config import DEFAULT_ROLLBACK_DIR as rollback_folder
from merls.logger import logging

log = logging.getLogger(__name__)

ROLLBACK_SEP = " -> "

CURRENT_NUMBER = 1


def get_rollback_logger(
    stem: str, folder: Path = rollback_folder
) -> Tuple[logging.Logger, Path]:
    global CURRENT_NUMBER

    logger = log.getChild(stem)

    time_string = time.strftime("%Y%m%d%H%M%S")
    filename = folder / f"{time_string}_{stem}_{CURRENT_NUMBER}.log"
    CURRENT_NUMBER += 1

    file_handler = logging.FileHandler(
        filename=filename,
        mode="w",
        encoding="utf-8",
    )

    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    return logger, filename


def pack_rollback_record(src: Union[str, Path], dst: Union[str, Path]):
    return f"{src}{ROLLBACK_SEP}{dst}"


def unpack_rollback_record(record: str):
    src, dst = record.split(ROLLBACK_SEP)
    return src, dst


def rollback_from_file(rollback_file: Union[str, Path]):
    log.info(f"rollback from {rollback_file}")
    with open(rollback_file, encoding="utf-8") as fp:
        for record in fp.read().splitlines():
            if record:
                src, dst = unpack_rollback_record(record)
                if os.path.exists(dst):
                    log.info(pack_rollback_record(dst, src))
                    os.rename(dst, src)
                else:
                    log.warning(f"{dst} does not exist")
