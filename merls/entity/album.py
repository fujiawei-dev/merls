import os
import re
from pathlib import Path
from typing import Set, Tuple, Union

NUMBER_PATTERN = re.compile(r"NO\.(\d+)|VOL\.(\d+)")

DATE_PATTERN = re.compile(r"(20\d{2})[_\-./年](\d{1,2})[_\-./月](\d{1,2})日?")


class AlbumEntity(object):
    @staticmethod
    def get_latest_number(path: Union[str, Path]) -> Tuple[Set[int], int]:
        if (
            os.path.exists(path)
            and (entries := os.listdir(path))
            and (number_pairs := NUMBER_PATTERN.findall(" ".join(entries)))
            and (number_pairs[0][0] or number_pairs[0][1])
        ):
            numbers = set()

            for n, m in number_pairs:
                if n:
                    numbers.add(int(n))
                if m:
                    numbers.add(int(m))

            return numbers, max(numbers)

        return set(), 0
