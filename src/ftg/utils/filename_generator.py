from abc import ABC
from typing import List

from ftg.utils.program_config import FilenameConfig


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

        concatenated_tags = self.__config.get_tags_separator().join(sorted(tags))

        joins = []

        if basename != "":
            joins.append(self.__get_adjusted_base_name(basename))
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

    def __get_adjusted_base_name(self,
                                 basename: str) -> str:
        result = basename.upper()

        result = result.strip(" ")

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

        if len(full_filename_splits) > 1:
            filename = ".".join(full_filename_splits[0:-1])
            extension = full_filename_splits[-1]
        else:
            filename = full_filename_splits[0]
            extension = ""

        filename_splits = filename.split(self.__config.get_basename_tags_separator())

        if len(filename_splits) > 1:

            basename = self.__config.get_basename_tags_separator().join(filename_splits[0:-1])
            tags = filename_splits[-1].split(self.__config.get_tags_separator())
        else:
            basename = filename_splits[0]
            tags = []

        return ReversionResult(basename,
                               tags,
                               extension)
