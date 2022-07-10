import json
from typing import List, Dict

import click

from ftg.config import FtgConfigImpl
from ftg.controller.ftg_window_controller import FtgWindowController


def read_categories_file(path_to_tags_file):
    with open(path_to_tags_file, "rt", encoding="UTF-8") as tags_file:
        json_dict: Dict[str, List[str]] = json.load(tags_file)

    result: Dict[str, List[str]] = {}

    for category_name, tags in json_dict.items():
        result[category_name.lower()] = [tag.lower() for tag in tags]

    return result


def main(path_to_tags_file):
    config = FtgConfigImpl()
    categories = read_categories_file(path_to_tags_file)
    ftg_window_controller = FtgWindowController(config,
                                                categories)
    ftg_window_controller.start()


@click.command()
@click.option('--tags', '-t', multiple=False, default='tags.json', help='Path to json file containing tags')
def cli(path_to_tags_file):
    main(path_to_tags_file)
