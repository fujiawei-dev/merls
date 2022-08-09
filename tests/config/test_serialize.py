import os.path
import tempfile

from faker import Faker
from toolkit.config.serialize import (
    deserialize_from_json_file,
    deserialize_from_yaml_file,
    serialize_to_json_file,
    serialize_to_yaml_file,
)

from merls.config.album_photo import AlbumPhotoOptions


def test_serialize_to_json_file(faker: Faker):
    owner = faker.name()
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, "config.json")
        serialize_to_json_file(AlbumPhotoOptions(owner=owner), tmp_file)
        assert owner in open(tmp_file, encoding="utf-8").read()


def test_deserialize_from_json_file(faker: Faker):
    owner = faker.name()
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, "config.json")
        serialize_to_json_file(AlbumPhotoOptions(owner=owner), tmp_file)
        options = deserialize_from_json_file(AlbumPhotoOptions, tmp_file)
        assert options.owner == owner


def test_serialize_to_yaml_file(faker: Faker):
    owner = faker.name()
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, "config.yaml")
        serialize_to_yaml_file(AlbumPhotoOptions(owner=owner), tmp_file)
        assert owner in open(tmp_file, encoding="utf-8").read()


def test_deserialize_from_yaml_file(faker: Faker):
    owner = faker.name()
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, "config.yaml")
        serialize_to_yaml_file(AlbumPhotoOptions(owner=owner), tmp_file)
        options = deserialize_from_yaml_file(AlbumPhotoOptions, tmp_file)
        assert options.owner == owner
