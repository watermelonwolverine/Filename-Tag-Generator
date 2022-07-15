import json
from typing import Dict, List

from ftg.controller.ftg_window_controller import FtgWindowController
from ftg.utils.program_config import ProgramConfigImpl
from ftg.utils.tag import Tag


def read_categories_file(path_to_tags_file) -> (List[Tag], Dict[str, List[Tag]]):
    with open(path_to_tags_file, "rt", encoding="UTF-8") as tags_file:
        json_dict: Dict[str, Dict[str, str]] = json.load(tags_file)

    tags_by_letter_code: Dict[str, Tag] = {}
    categories: Dict[str, List[Tag]] = {}

    for category_name, tags in json_dict.items():

        categories[category_name.lower()] = []

        for letter_code, full_name in tags.items():
            if letter_code in tags_by_letter_code.keys():

                tag = tags_by_letter_code[letter_code]
                if tag.full_name != full_name:
                    raise Exception("Invalid tag-list")
            else:
                tag = Tag(letter_code, full_name)
                tags_by_letter_code[letter_code] = tag

            categories[category_name.lower()].append(tag)

    return list(tags_by_letter_code.values()), categories


def main(path_to_tags_file):
    config = ProgramConfigImpl()
    tags, categories = read_categories_file(path_to_tags_file)
    ftg_window_controller = FtgWindowController(config,
                                                tags,
                                                categories)
    ftg_window_controller.start()
