from abc import ABC
from typing import List

from ftg.__constants import illegal_chars
from ftg.exceptions import FtgException
from ftg.utils.program_config import NamingConfig


class ReversionResult:

    def __init__(self,
                 basename: str,
                 tags: List[str],
                 extension: str, ):
        self.basename = basename
        self.tags = tags
        self.extension = extension


class NameGenerator(ABC):

    def generate_filename(self,
                          basename: str,
                          tags: List[str],
                          extension: str) -> str:
        raise NotImplementedError()

    def check(self, basename: str,
              tags: List[str],
              extension: str) -> None:
        raise NotImplementedError()

    def revert(self,
               filename: str) -> ReversionResult:
        raise NotImplementedError()


class NameGeneratorImpl(NameGenerator):

    def __init__(self,
                 config: NamingConfig):
        self.__config = config

    def generate_filename(self,
                          basename: str,
                          tags: List[str],
                          extension: str) -> str:

        concatenated_tags = self.__config.get_tags_separator().join(sorted(tags))

        joins = [self.__get_adjusted_base_name(basename)]

        if concatenated_tags != "":
            joins.append(concatenated_tags)

        result = self.__config.get_basename_tags_separator().join(joins)

        joins = []

        if result != "":
            joins.append(result)
        if extension != "":
            joins.append(extension)

        result = ".".join(joins)

        return result

    def check(self,
              basename: str,
              tags: List[str],
              extension: str) -> None:

        for illegal_char in illegal_chars:
            if illegal_char in extension:
                raise FtgException(F'"{illegal_char}" is not allowed as part of the extension.')
            if illegal_char in basename:
                raise FtgException(F'"{illegal_char}" is not allowed as part of the basename.')

        illegal_chars_for_tags = illegal_chars.copy()
        illegal_chars_for_tags.append(self.__config.get_tags_separator())
        illegal_chars_for_tags.append(self.__config.get_basename_tags_separator())

        for illegal_char in illegal_chars_for_tags:
            for tag in tags:
                if illegal_char in tag:
                    raise FtgException(F'"{illegal_char}" is not allowed as part of any tag.')

    def __get_adjusted_base_name(self,
                                 basename: str) -> str:

        if not self.__config.get_adjust_basename():
            return basename

        result = basename

        if self.__config.get_capitalize_basename():
            result = result.upper()

        result = result.strip(" ")

        spacer = self.__config.get_basename_spacer()
        double_spacer = spacer + spacer

        if self.__config.get_replace_basename_spacer():

            result = result.replace(" ",
                                    spacer)

            result = result.replace(self.__config.get_tags_separator(),
                                    spacer)

            result = result.replace(self.__config.get_basename_tags_separator(),
                                    spacer)

            while double_spacer in result:
                result = result.replace(double_spacer, spacer)

        return result

    def revert(self,
               full_filename: str) -> ReversionResult:

        full_filename_splits = full_filename.split(".")

        # split at the last . if more than one exist
        if len(full_filename_splits) > 1:
            filename = ".".join(full_filename_splits[0:-1])
            extension = full_filename_splits[-1]
        else:
            filename = full_filename_splits[0]
            extension = ""

        filename_splits = filename.split(self.__config.get_basename_tags_separator())

        # split at the last separator if more than one exist
        if len(filename_splits) > 1:

            basename = self.__config.get_basename_tags_separator().join(filename_splits[0:-1])
            tags = filename_splits[-1].split(self.__config.get_tags_separator())
        else:
            basename = filename_splits[0]
            tags = []

        return ReversionResult(basename,
                               tags,
                               extension)
