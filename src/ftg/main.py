import json
from typing import List, Dict

from ftg.controller.ftg_window_controller import FtgWindowController
from ftg.utils.program_config import ProgramConfigImpl


def read_categories_file(path_to_tags_file):
    with open(path_to_tags_file, "rt", encoding="UTF-8") as tags_file:
        json_dict: Dict[str, List[str]] = json.load(tags_file)

    result: Dict[str, List[str]] = {}

    for category_name, tags in json_dict.items():
        result[category_name.lower()] = [tag.lower() for tag in tags]

    return result


def main(path_to_tags_file):
    config = ProgramConfigImpl()
    categories = read_categories_file(path_to_tags_file)
    ftg_window_controller = FtgWindowController(config,
                                                categories)
    ftg_window_controller.start()
