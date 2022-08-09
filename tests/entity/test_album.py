import os
import tempfile

from merls.entity.album import DATE_PATTERN, NUMBER_PATTERN, AlbumEntity


def test_patterns():
    assert NUMBER_PATTERN.match("NO.1")
    assert NUMBER_PATTERN.match("VOL.1")
    assert NUMBER_PATTERN.match("NO.100")
    assert not NUMBER_PATTERN.match("NO.-")
    assert not NUMBER_PATTERN.match("VOL.-")

    assert DATE_PATTERN.match("2019年1月1日")
    assert DATE_PATTERN.match("2019.1.1")
    assert not DATE_PATTERN.match("2019.1日")


def test_get_latest_number():
    with tempfile.TemporaryDirectory() as tmp_dir:

        numbers = set()
        max_number = 20

        for i in range(1, max_number + 1):
            numbers.add(i)
            os.makedirs(os.path.join(tmp_dir, f"{'NO'if i%2==0 else 'VOL'}.{i:03d}"))

        assert AlbumEntity.get_latest_number(tmp_dir) == (numbers, max_number)
