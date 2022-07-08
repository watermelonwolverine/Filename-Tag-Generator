from abc import ABC


class UIConfig(ABC):
    def get_font_size(self) -> int:
        raise NotImplementedError()

    def get_padding_small(self) -> int:
        raise NotImplementedError()

    def get_padding_big(self) -> int:
        raise NotImplementedError()


class FilenameConfig(ABC):
    def get_basename_spacer(self) -> str:
        raise NotImplementedError()

    def get_basename_tags_separator(self) -> str:
        raise NotImplementedError()

    def get_tags_separator(self) -> str:
        raise NotImplementedError()


class FtgConfig(ABC):

    def get_ui_config(self) -> UIConfig:
        raise NotImplementedError()

    def get_filename_config(self) -> FilenameConfig:
        raise NotImplementedError()


class UIConfigImpl(UIConfig):
    __font_size = 14
    __padding_big = 10
    __padding_small = 5

    def get_font_size(self) -> int:
        return self.__font_size

    def get_padding_small(self) -> int:
        return self.__padding_small

    def get_padding_big(self) -> int:
        return self.__padding_big


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


class FtgConfigImpl(FtgConfig):
    __ui_config = UIConfigImpl()
    __filename_config = FilenameConfigImpl()

    def get_ui_config(self) -> UIConfig:
        return self.__ui_config

    def get_filename_config(self) -> FilenameConfig:
        return self.__filename_config
