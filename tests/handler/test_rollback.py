import os.path
import tempfile

from merls.handler.rollback import (
    get_rollback_logger,
    pack_rollback_record,
    rollback_from_file,
)


def test_rollback_from_file():
    paris = [
        ("2_1.txt", "1_1.txt"),
        ("2_2.txt", "1_2.txt"),
        ("2_3.txt", "1_3.txt"),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        logger, filename = get_rollback_logger(os.path.basename(tmpdir))

        for i, j in paris:
            i, j = os.path.join(tmpdir, i), os.path.join(tmpdir, j)
            logger.info(pack_rollback_record(i, j))
            with open(j, "w") as f:
                f.write(i)

        for i, j in paris:
            assert not os.path.exists(os.path.join(tmpdir, i))
            assert os.path.exists(os.path.join(tmpdir, j))

        rollback_from_file(filename)

        for i, j in paris:
            assert os.path.exists(os.path.join(tmpdir, i))
            assert not os.path.exists(os.path.join(tmpdir, j))
