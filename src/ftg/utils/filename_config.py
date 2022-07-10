from abc import ABC


class FilenameConfig(ABC):
    def get_basename_spacer(self) -> str:
        raise NotImplementedError()

    def get_basename_tags_separator(self) -> str:
        raise NotImplementedError()

    def get_tags_separator(self) -> str:
        raise NotImplementedError()


class FilenameConfigImpl(FilenameConfig):
    __basename_spacer = "-"
    __basename_tags_separator = ";"
    __tag_separator = "_"

    def get_basename_spacer(self) -> str:
        return self.__basename_spacer

    def get_basename_tags_separator(self) -> str:
        return self.__basename_tags_separator

    def get_tags_separator(self) -> str:
        return self.__tag_separator
