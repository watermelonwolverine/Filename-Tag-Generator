from abc import ABC

from ftg.utils.filename_config import FilenameConfig, FilenameConfigImpl
from ftg.view.ui_config import UIConfig, UIConfigImpl


class ProgramConfig(ABC):

    def get_ui_config(self) -> UIConfig:
        raise NotImplementedError()

    def get_filename_config(self) -> FilenameConfig:
        raise NotImplementedError()


class ProgramConfigImpl(ProgramConfig):
    __ui_config = UIConfigImpl()
    __filename_config = FilenameConfigImpl()

    def get_ui_config(self) -> UIConfig:
        return self.__ui_config

    def get_filename_config(self) -> FilenameConfig:
        return self.__filename_config
