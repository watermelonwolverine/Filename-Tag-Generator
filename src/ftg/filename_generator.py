from abc import ABC
from typing import List

from ftg.config import FilenameConfig


class ReversionResult:

    def __init__(self,
                 basename: str,
                 tags: List[str],
                 extension: str, ):
        self.basename = basename
        self.tags = tags
        self.extension = extension


class FilenameGenerator(ABC):

    def generate_filename(self,
                          basename: str,
                          tags: List[str],
                          extension: str) -> str:
        raise NotImplementedError()

    def revert(self,
               filename: str) -> ReversionResult:
        raise NotImplementedError()


class FilenameGeneratorImpl(FilenameGenerator):

    def __init__(self,
                 config: FilenameConfig):
        self.__config = config

    def generate_filename(self,
                          basename: str,
                          tags: List[str],
                          extension: str) -> str:

        result = self.__get_adjusted_base_name(basename)

        concatenated_tags = self.__config.get_tags_separator().join(tags)

        if concatenated_tags != "":
            result = self.__config.get_basename_tags_separator().join(
                [result,
                 concatenated_tags])

        if extension != "":
            result = ".".join([result, extension])

        return result

    def __get_adjusted_base_name(self,
                                 basename: str) -> str:
        result = basename.upper()

        result = result.replace(" ",
                                self.__config.get_basename_spacer())

        result = result.replace(self.__config.get_tags_separator(),
                                self.__config.get_basename_spacer())

        result = result.replace(self.__config.get_basename_tags_separator(),
                                self.__config.get_basename_spacer())

        return result

    def revert(self,
               full_filename: str) -> ReversionResult:

        full_filename_splits = full_filename.split(".")

        filename = full_filename_splits[0]
        if len(full_filename_splits) > 1:
            extension = full_filename_splits[1]
        else:
            extension = ""

        filename_splits = filename.split(self.__config.get_basename_tags_separator())

        basename = filename_splits[0]

        if len(filename_splits) > 1:
            tags = filename_splits[1].split(self.__config.get_tags_separator())
        else:
            tags = []

        return ReversionResult(basename,
                               tags,
                               extension)
