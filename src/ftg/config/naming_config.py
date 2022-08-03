from abc import ABC
from typing import Dict

from ftg.__constants import illegal_chars
from ftg.exceptions import FtgException
from ftg.utils.parse_utils import read_bool_value, read_str_value
from ftg.config.tags import Tags


class NamingConfig(ABC):

    def get_adjust_basename(self) -> bool:
        raise NotImplementedError()

    def get_capitalize_basename(self) -> bool:
        raise NotImplementedError()

    def get_replace_basename_spacer(self) -> bool:
        raise NotImplementedError()

    def get_basename_spacer(self) -> str:
        raise NotImplementedError()

    def get_basename_tags_separator(self) -> str:
        raise NotImplementedError()

    def get_tags_separator(self) -> str:
        raise NotImplementedError()

    def check_tags(self,
                   tags: Tags) -> None:
        raise NotImplementedError()


class NamingConfigImpl(NamingConfig):
    # defaults
    __default_adjust_basename = True
    __default_capitalize_basename = True
    __default_replace_basename_spacer = True
    __default_basename_spacer = "-"
    __default_basename_tags_separator = ";"
    __default_tag_separator = "_"

    # json keys
    ADJUST_BASENAME_KEY = "adjust-basename"
    CAPITALIZE_BASENAME_KEY = "capitalize-basename"
    REPLACE_BASENAME_SPACER_KEY = "replace-basename-spacer"
    BASENAME_SPACER_KEY = "basename-spacer"
    BASENAME_TAGS_SEPARATOR_KEY = "basename-tags-separator"
    TAG_SEPARATOR_KEY = "tag-separator"

    default_config_dict = {ADJUST_BASENAME_KEY: __default_adjust_basename,
                           CAPITALIZE_BASENAME_KEY: __default_capitalize_basename,
                           REPLACE_BASENAME_SPACER_KEY: __default_replace_basename_spacer,
                           BASENAME_SPACER_KEY: __default_basename_spacer,
                           BASENAME_TAGS_SEPARATOR_KEY: __default_basename_tags_separator,
                           TAG_SEPARATOR_KEY: __default_tag_separator}

    def __init__(self,
                 adjust_basename=__default_adjust_basename,
                 capitalize_basename=__default_capitalize_basename,
                 replace_basename_spacer=__default_replace_basename_spacer,
                 basename_spacer=__default_basename_spacer,
                 basename_tags_separator=__default_basename_tags_separator,
                 tag_separator=__default_tag_separator):
        self.__adjust_basename = adjust_basename
        self.__capitalize_basename = capitalize_basename
        self.__replace_basename_spacer = replace_basename_spacer
        self.__basename_spacer = basename_spacer
        self.__basename_tags_separator = basename_tags_separator
        self.__tag_separator = tag_separator

        self.check_self()

    def get_adjust_basename(self) -> bool:
        return self.__adjust_basename

    def get_capitalize_basename(self) -> bool:
        return self.__capitalize_basename

    def get_basename_spacer(self) -> str:
        return self.__basename_spacer

    def get_replace_basename_spacer(self) -> bool:
        return self.__replace_basename_spacer

    def get_basename_tags_separator(self) -> str:
        return self.__basename_tags_separator

    def get_tags_separator(self) -> str:
        return self.__tag_separator

    def check_self(self):

        for illegal_char in illegal_chars:
            if illegal_char in self.__basename_spacer \
                    or illegal_char in self.__tag_separator \
                    or illegal_char in self.__basename_tags_separator:
                raise FtgException(F'"{illegal_char}" is not allowed')

        if self.__tag_separator == "":
            raise FtgException(F'An empty value for "{self.TAG_SEPARATOR_KEY}" is not allowed')
        if self.__basename_tags_separator == "":
            raise FtgException(F'An empty value for "{self.BASENAME_TAGS_SEPARATOR_KEY}" is not allowed')

    def check_tags(self, tags: Tags) -> None:

        for tag in tags.tags:

            if self.get_basename_tags_separator() in tag.letter_code:
                raise FtgException(
                    F'Tag "{tag.letter_code}" contains text reserved for "{NamingConfigImpl.BASENAME_TAGS_SEPARATOR_KEY}": {self.get_basename_tags_separator()}')
            elif self.get_tags_separator() in tag.letter_code:
                raise FtgException(
                    F'Tag "{tag.letter_code}" contains text reserved for "{NamingConfigImpl.TAG_SEPARATOR_KEY}": {self.get_tags_separator()}')
            else:
                for illegal_char in illegal_chars:
                    if illegal_char in tag.letter_code:
                        raise FtgException(F'Tag "{tag.letter_code}" contains illegal text: {illegal_char}')

    @classmethod
    def parse_dict(cls,
                   json_dict: Dict[str, int]) -> NamingConfig:
        adjust_basename = read_bool_value(json_dict,
                                          cls.ADJUST_BASENAME_KEY,
                                          cls.__default_adjust_basename)

        capitalize_title = read_bool_value(json_dict,
                                           cls.CAPITALIZE_BASENAME_KEY,
                                           cls.__default_capitalize_basename)

        replace_basename_spacer = read_bool_value(json_dict,
                                                  cls.REPLACE_BASENAME_SPACER_KEY,
                                                  cls.__default_replace_basename_spacer)

        basename_spacer = read_str_value(json_dict,
                                         cls.BASENAME_SPACER_KEY,
                                         cls.__default_basename_spacer)

        basename_tags_separator = read_str_value(json_dict,
                                                 cls.BASENAME_TAGS_SEPARATOR_KEY,
                                                 cls.__default_basename_tags_separator)

        tag_separator = read_str_value(json_dict,
                                       cls.TAG_SEPARATOR_KEY,
                                       cls.__default_tag_separator)

        return NamingConfigImpl(adjust_basename=adjust_basename,
                                capitalize_basename=capitalize_title,
                                replace_basename_spacer=replace_basename_spacer,
                                basename_spacer=basename_spacer,
                                basename_tags_separator=basename_tags_separator,
                                tag_separator=tag_separator)
