"""Console script for merls."""
import os
import sys

import click
from cookiecutter.prompt import read_user_choice
from toolkit.config.runtime import EDITOR
from toolkit.config.serialize import serialize_to_yaml_file
from toolkit.fs.dir import delete_empty_folder_including_itself

from merls import __version__, handler
from merls.config import DEFAULT_CONFIG_FILE, DEFAULT_ROLLBACK_DIR
from merls.config.album_photo import get_album_photo_options
from merls.config.settings import Settings
from merls.entity.image import clear_images_exif_recursively
from merls.handler import album, rollback

settings = Settings(config_file=DEFAULT_CONFIG_FILE)


@click.group(help="Merge your photos into albums.")
def main():
    pass


@main.command(help="Print the version of merls.")
def version():
    click.echo(__version__)


@main.command(help="Manage your configuration.")
@click.option("--edit", "-e", is_flag=True, help="Edit the config file.")
def config(edit: bool):
    if not DEFAULT_CONFIG_FILE.exists():
        serialize_to_yaml_file(settings, DEFAULT_CONFIG_FILE)

    if edit:
        click.edit(filename=DEFAULT_CONFIG_FILE, editor=EDITOR)
        return

    click.echo(DEFAULT_CONFIG_FILE)


@main.command(help="Remove all empty folders in the target path (including itself).")
@click.option(
    "--target-path",
    "-p",
    required=False,
    type=click.Path(exists=True, file_okay=False, writable=True),
    help="The target path.",
)
def rm(target_path):
    if not target_path:
        click.echo("Please specify the target path.")
        target_path = click.prompt(
            "Target path",
            default=settings.rm_target_path,
            type=click.Path(exists=True, file_okay=False, writable=True),
        )

    delete_empty_folder_including_itself(target_path)


@main.command(help="Move albums to the owners path.")
@click.option(
    "--source-path",
    required=False,
    type=click.Path(exists=True, file_okay=False, writable=True),
    help="The source path.",
)
@click.option(
    "--owners-path",
    required=False,
    type=click.Path(exists=True, file_okay=False, writable=True),
    help="The owners path.",
)
def mv(source_path, owners_path):
    if not source_path:
        click.echo("Please specify the source path.")
        source_path = click.prompt(
            "Source path",
            default=settings.mv_source_path,
            type=click.Path(exists=True, file_okay=False, writable=True),
        )

    if not owners_path:
        click.echo("Please specify the owners path.")
        owners_path = click.prompt(
            "Owners path",
            default=settings.mv_owners_path,
            type=click.Path(exists=True, file_okay=False, writable=True),
        )

    album.move_albums_to_owner(source_path, owners_path)


@main.command(help="Clear image's exif.")
@click.option(
    "--target-path",
    "-p",
    required=False,
    type=click.Path(exists=True, file_okay=False, writable=True),
    help="The target path.",
)
def cls(target_path):
    if not target_path:
        click.echo("Please specify the target path.")
        target_path = click.prompt(
            "Target path",
            default=settings.cls_target_path,
            type=click.Path(exists=True, file_okay=False, writable=True),
        )

    clear_images_exif_recursively(target_path)


@main.command(help="Recover from a rollback file.")
@click.option(
    "--rollback-file",
    "-f",
    required=False,
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="The rollback file.",
)
@click.option(
    "--open-explorer",
    "-e",
    is_flag=True,
    help="Open the rollback folder in explorer.",
)
@click.option(
    "--list-files",
    "-l",
    is_flag=True,
    help="List the rollback files.",
)
def rv(rollback_file: str, open_explorer: bool, list_files: bool):
    if open_explorer:
        click.launch(str(DEFAULT_ROLLBACK_DIR), locate=True)
        return

    if list_files:
        click.echo("\n".join(reversed(os.listdir(DEFAULT_ROLLBACK_DIR)[-20:])))
        return

    if not rollback_file:
        rollback_file = os.path.join(
            DEFAULT_ROLLBACK_DIR,
            read_user_choice(
                "Please select a rollback file",
                options=os.listdir(DEFAULT_ROLLBACK_DIR)[-20:],
            ),
        )

    rollback.rollback_from_file(rollback_file)


@main.command(help="Organize album folders or album photos or wallpapers.")
@click.option(
    "--source-path",
    "-s",
    required=False,
    type=click.Path(exists=True, file_okay=False, writable=True),
    help="The source path.",
)
@click.option(
    "--destination-path",
    "-d",
    required=False,
    default=settings.tidy_destination_path,
    type=click.Path(exists=True, file_okay=False, writable=True),
    help="The destination path.",
)
@click.option("--wallpapers", is_flag=True, help="Organize wallpapers.")
@click.option("--album-folders", is_flag=True, help="Organize album folders.")
@click.option("--album-photos", is_flag=True, help="Organize album photos.")
@click.option("--default", is_flag=True, default=True, help="Default actions.")
def tidy(
    source_path: str,
    destination_path: str,
    wallpapers: bool,
    album_folders: bool,
    album_photos: bool,
    default: bool,
):
    if not source_path:
        click.echo("Please specify the source path.")
        source_path = click.prompt(
            "Source path",
            default=settings.tidy_source_path,
            type=click.Path(exists=True, file_okay=False, writable=True),
        )

    if wallpapers:
        click.echo("Please specify the prefix of wallpapers.")
        wallpaper_type = click.prompt("Type", type=click.STRING, default="C")
        wallpaper_author = click.prompt("Author", type=click.STRING, default="U")
        handler.organize_wallpapers(wallpaper_type, wallpaper_author, source_path)
        return

    if not source_path:
        click.echo("Please specify the source path.")
        source_path = click.prompt(
            "Source path",
            default=settings.tidy_source_path,
            type=click.Path(exists=True, file_okay=False, writable=True),
        )

    options, config_file = get_album_photo_options(source_path)

    while not options:
        click.edit(filename=config_file, editor="code")
        click.echo("Please edit the config.json file.")
        click.pause(info="Press any key to continue...")
        options, config_file = get_album_photo_options(source_path)

    if default or album_folders:
        handler.organize_album_folders(source_path, destination_path, options)

    if default or album_photos:
        handler.organize_album_photos(source_path, options, settings.ignore)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
