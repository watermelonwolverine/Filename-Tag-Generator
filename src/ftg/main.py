import json

import click

from ftg.config import FtgConfigImpl
from ftg.ftg_window import FtgWindow


def read_categories_file(path_to_tags_file):
    with open(path_to_tags_file, "rt", encoding="UTF-8") as tags_file:
        return json.load(tags_file)


def main(path_to_tags_file):
    config = FtgConfigImpl()
    categories = read_categories_file(path_to_tags_file)
    ftg_window = FtgWindow(config,
                           categories)
    ftg_window.start()


@click.command()
@click.option('--tags', '-t', multiple=False, default='tags.json', help='Path to json file containing tags')
def cli(path_to_tags_file):
    main(path_to_tags_file)
