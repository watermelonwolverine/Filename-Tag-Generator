from abc import ABC
from typing import Dict

from ftg.utils.misconfiguration_exception import MisconfigurationException
from ftg.utils.parse_utils import read_int_value


class UIConfig(ABC):
    def get_font_size(self) -> int:
        raise NotImplementedError()

    def get_padding_small(self) -> int:
        raise NotImplementedError()

    def get_padding_big(self) -> int:
        raise NotImplementedError()

    def get_button_width(self) -> int:
        raise NotImplementedError()


class UIConfigImpl(UIConfig):
    # defaults
    __default_font_size = 14
    __default_padding_small = 5
    __default_padding_big = 2 * __default_padding_small
    __default_button_width = 15

    # json keys
    FONT_SIZE_KEY = "font-size"
    PADDING_SMALL_KEY = "padding-small"
    PADDING_BIG_KEY = "padding-big"
    BUTTON_WIDTH_KEY = "button-width"

    def __init__(self,
                 font_size=__default_font_size,
                 padding_small=__default_padding_small,
                 padding_big=__default_padding_big,
                 button_width=__default_button_width):

        self.font_size = font_size
        self.padding_small = padding_small
        self.padding_big = padding_big
        self.button_width = button_width

    def get_font_size(self) -> int:
        return self.font_size

    def get_padding_small(self) -> int:
        return self.padding_small

    def get_padding_big(self) -> int:
        return self.padding_big

    def get_button_width(self) -> int:
        return self.button_width

    @classmethod
    def parse_dict(cls,
                   json_dict: Dict[str, int]) -> UIConfig:

        font_size = read_int_value(json_dict,
                                   cls.FONT_SIZE_KEY,
                                   cls.__default_font_size)

        padding_small = read_int_value(json_dict,
                                       cls.PADDING_SMALL_KEY,
                                       cls.__default_padding_small)

        padding_big = read_int_value(json_dict,
                                     cls.PADDING_BIG_KEY,
                                     cls.__default_padding_big)

        button_width = read_int_value(json_dict,
                                      cls.BUTTON_WIDTH_KEY,
                                      cls.__default_button_width)

        return UIConfigImpl(font_size=font_size,
                            padding_small=padding_small,
                            padding_big=padding_big,
                            button_width=button_width)

    @classmethod
    def read_int_value(cls,
                       dict_: Dict,
                       key: str,
                       default_value: int) -> int:

        if key in dict_.keys():
            value = dict_[key]

            if type(value) is not int:
                raise MisconfigurationException(F"{key} has to be an int")
        else:
            value = default_value

        return value
