import re

NUMBER_PATTERNS = [
    re.compile(r"_?(\d+)_\w"),
    re.compile(r"[\[（(](\d+)[)）\]]"),
    re.compile(r"[_\-](\d+)"),
    re.compile(r"\[(\d+)]"),
    re.compile(r"(\d+)$"),
]


class AlbumPhotoEntity(object):
    def __init__(self):
        self.used = set()
        self.latest_number = 0

    def get_number(self, text: str) -> int:
        number = self.latest_number + 1

        for pattern in NUMBER_PATTERNS:
            if match := pattern.search(text):
                number = int(match.group(1))
                while number in self.used:
                    number += 1
                self.used.add(number)
                break

        if number == self.latest_number + 1:
            self.latest_number += 1

        return number
