import json
from typing import List, Dict, Any

from ftg.__constants import UTF_8
from ftg.exceptions import JSONParseException
from ftg.localization import WRONG_TAGS_FILE_STRUCTURE
from ftg.utils.tag import Tag

CATEGORIES_KEY = "categories"


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
            json_dict: Dict[str, Any()] = json.load(tags_file)

        if CATEGORIES_KEY not in json_dict.keys():
            raise JSONParseException(F"Missing key \"{CATEGORIES_KEY}\"")

        categories = json_dict[CATEGORIES_KEY]

        if type(categories) is not dict:
            raise JSONParseException(WRONG_TAGS_FILE_STRUCTURE)

        return cls.__parse_categories(categories)

    @classmethod
    def __parse_categories(cls,
                           json_dict: Dict[str, Dict[str, str]]):

        tags_by_letter_code: Dict[str, Tag] = {}
        categories: Dict[str, List[Tag]] = {}

        for category_name, tags in json_dict.items():

            if type(tags) is not dict:
                raise JSONParseException(F"The tag list for category \"{category_name}\" has the wrong type. "
                                         F"It should be a dictionary but is a {type(tags)}")

            if category_name in categories:
                raise JSONParseException(F"Duplicate category \"{category_name}\"")

            cls.__parse_category(category_name,
                                 tags,
                                 categories,
                                 tags_by_letter_code)
        return Tags(list(tags_by_letter_code.values()),
                    categories)

    @classmethod
    def __parse_category(cls,
                         category_name: str,
                         tags: Dict[str, str],
                         categories_out: Dict[str, List[Tag]],
                         tags_by_letter_code_out: Dict[str, Tag]):
        categories_out[category_name.lower()] = []

        for letter_code, full_name in tags.items():

            if type(full_name) is not str:
                raise JSONParseException(F"Wrong type for full name of \"{letter_code}\"")

            if letter_code in tags_by_letter_code_out.keys():

                tag = tags_by_letter_code_out[letter_code]
                if tag.full_name != full_name:
                    raise JSONParseException(F"Tags may only exists multiple times with the same display name. "
                                             F"This is not the case for \"{letter_code}\".")
            else:
                tag = Tag(letter_code, full_name)
                tags_by_letter_code_out[letter_code] = tag

            categories_out[category_name.lower()].append(tag)
