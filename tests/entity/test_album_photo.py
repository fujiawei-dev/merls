from merls.entity.album_photo import AlbumPhotoEntity


def test_get_number():
    album_photo = AlbumPhotoEntity()

    for text, expected in [
        ("NO.1", 1),
        ("VOL.1", 2),
        ("NO.100", 100),
        ("NO.-", 3),
        ("VOL.-", 4),
        ("NO.1_", 5),
        ("VOL.1_", 6),
        ("VOL.100", 101),
    ]:
        assert album_photo.get_number(text) == expected
