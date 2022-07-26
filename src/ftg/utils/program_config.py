import json
from abc import ABC
from typing import Dict

from ftg.__constants import UTF_8
from ftg.exceptions import JSONParseException
from ftg.utils.naming_config import NamingConfig, NamingConfigImpl
from ftg.view.ui_config import UIConfig, UIConfigImpl


class ProgramConfig(ABC):

    def get_ui_config(self) -> UIConfig:
        raise NotImplementedError()

    def get_naming_config(self) -> NamingConfig:
        raise NotImplementedError()


class ProgramConfigImpl(ProgramConfig):
    # defaults
    __default_ui_config = UIConfigImpl()
    __default_naming_config = NamingConfigImpl()

    # json keys
    UI_CONFIG_KEY = "ui-config"
    NAMING_CONFIG_KEY = "naming-config"

    default_config_dict = {UI_CONFIG_KEY: UIConfigImpl.default_config_dict,
                           NAMING_CONFIG_KEY: NamingConfigImpl.default_config_dict}

    def __init__(self,
                 ui_config=__default_ui_config,
                 naming_config=__default_naming_config):

        self.__ui_config = ui_config
        self.__naming_config = naming_config

    def get_ui_config(self) -> UIConfig:
        return self.__ui_config

    def get_naming_config(self) -> NamingConfig:
        return self.__naming_config

    @classmethod
    def parse_file(cls,
                   path_to_file: str) -> ProgramConfig:
        with open(path_to_file, "rt", encoding=UTF_8) as fh:
            json_str = fh.read()
            return cls.parse_json_str(json_str)

    @classmethod
    def parse_json_str(cls,
                       json_str: str) -> ProgramConfig:
        json_dict = json.loads(json_str)

        return cls.parse_dict(json_dict)

    @classmethod
    def parse_dict(cls,
                   json_dict: Dict[str, Dict]) -> ProgramConfig:

        if cls.UI_CONFIG_KEY in json_dict.keys():

            ui_config_dict = json_dict.get(cls.UI_CONFIG_KEY)

            if type(ui_config_dict) is not dict:
                raise JSONParseException(F"Wrong type for \"{cls.UI_CONFIG_KEY}\". "
                                         F"Expected a dictionary, got {type(ui_config_dict).__name__}")

            ui_config = UIConfigImpl.parse_dict(ui_config_dict)
        else:
            ui_config = cls.__default_ui_config

        if cls.NAMING_CONFIG_KEY in json_dict.keys():

            naming_config_dict = json_dict.get(cls.NAMING_CONFIG_KEY)

            if type(naming_config_dict) is not dict:
                raise JSONParseException(F"Wrong type for \"{cls.UI_CONFIG_KEY}\". "
                                         F"Expected a dictionary, got {type(naming_config_dict).__name__}")

            naming_config = NamingConfigImpl.parse_dict(naming_config_dict)
        else:
            naming_config = cls.__default_naming_config

        return ProgramConfigImpl(ui_config=ui_config,
                                 naming_config=naming_config)
