import os.path
import tempfile

from toolkit.config.serialize import serialize_to_json_file

from merls.config.album_photo import AlbumPhotoOptions, get_album_photo_options


def test_get_album_photo_options():
    with tempfile.TemporaryDirectory() as tmp_dir:
        options, _ = get_album_photo_options(tmp_dir)
        assert options is None

        tmp_file = os.path.join(tmp_dir, "config.json")
        serialize_to_json_file(AlbumPhotoOptions(owner="pytest"), tmp_file)
        options, _ = get_album_photo_options(tmp_dir)
        assert isinstance(options, AlbumPhotoOptions)
        assert options.owner == "pytest"
