import json
from typing import List, Dict, Any

import ftg
from ftg.__constants import UTF_8
from ftg.exceptions import JSONParseException, FtgException
from ftg.localization import WRONG_TAGS_FILE_STRUCTURE


class Tag:
    def __init__(self,
                 letter_code: str,
                 full_name: str):
        self.letter_code = letter_code
        self.full_name = full_name

    def __lt__(self, other):
        if type(other) != Tag:
            raise Exception("Cannot compare")

        return self.full_name < other.full_name


class Tags:
    FTG_VERSION_KEY = "ftg-version"
    CATEGORIES_KEY = "categories"

    def __init__(self,
                 tags: List[Tag],
                 categories: Dict[str, List[Tag]]):
        self.tags = tags
        self.categories = categories
        self.check_self()

    def check_self(self) -> None:

        for tag in self.tags:
            if tag.letter_code == "":
                raise FtgException("Empty tag keys are not allowed.")

    @classmethod
    def parse_file(cls,
                   path_to_tags_file):

        with open(path_to_tags_file, "rt", encoding=UTF_8) as tags_file:
            json_dict: Dict[str, Any()] = json.load(tags_file)

        if cls.CATEGORIES_KEY not in json_dict.keys():
            raise JSONParseException(F"Missing key \"{cls.CATEGORIES_KEY}\"")

        categories = json_dict[cls.CATEGORIES_KEY]

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


example_tags_dict = {Tags.FTG_VERSION_KEY: ftg.__version__,
                     Tags.CATEGORIES_KEY: {
                         "category1": {"tag1": "tag1-display-name",
                                       "tag2": "tag2-display-name"},
                         "category2": {"tag1": "tag1-display-name",
                                       "tag3": "tag3-display-name"}
                     }}
