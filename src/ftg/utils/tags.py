import json
from typing import List, Dict

from ftg.__constants import UTF_8
from ftg.utils.tag import Tag


class Tags:

    def __init__(self,
                 tags: List[Tag],
                 categories: Dict[str, List[Tag]]):
        self.tags = tags
        self.categories = categories

    @classmethod
    def parse_file(cls,
                   path_to_tags_file):

        with open(path_to_tags_file, "rt", encoding=UTF_8) as tags_file:
            json_dict: Dict[str, Dict[str, str]] = json.load(tags_file)

        tags_by_letter_code: Dict[str, Tag] = {}
        categories: Dict[str, List[Tag]] = {}

        for category_name, tags in json_dict.items():
            cls.__parse_category(category_name,
                                 tags,
                                 categories,
                                 tags_by_letter_code)

        result = Tags(list(tags_by_letter_code.values()),
                      categories)

        return result

    @classmethod
    def __parse_category(cls,
                         category_name: str,
                         tags: Dict[str, str],
                         categories_out: Dict[str, List[Tag]],
                         tags_by_letter_code_out: Dict[str, Tag]):

        categories_out[category_name.lower()] = []

        for letter_code, full_name in tags.items():
            if letter_code in tags_by_letter_code_out.keys():

                tag = tags_by_letter_code_out[letter_code]
                if tag.full_name != full_name:
                    raise Exception("Invalid tag-list")
            else:
                tag = Tag(letter_code, full_name)
                tags_by_letter_code_out[letter_code] = tag

            categories_out[category_name.lower()].append(tag)
