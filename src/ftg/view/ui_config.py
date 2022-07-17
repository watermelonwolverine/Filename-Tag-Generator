from abc import ABC


class UIConfig(ABC):
    def get_font_size(self) -> int:
        raise NotImplementedError()

    def get_padding_small(self) -> int:
        raise NotImplementedError()

    def get_padding_big(self) -> int:
        raise NotImplementedError()

    def get_button_width(self) -> int:
        raise NotImplementedError()

    def get_horizontal_scrollbar_enabled(self) -> bool:
        raise NotImplementedError()

    def get_show_extension_entry(self) -> bool:
        raise NotImplementedError()

    def get_show_full_name_entry(self) -> bool:
        raise NotImplementedError()


class UIConfigImpl(UIConfig):
    __font_size = 14
    __padding_big = 10
    __padding_small = 5
    __button_width = 15
    __horizontal_scrollbar_enabled = True
    __show_extension_entry = False
    __show_full_name_entry = False

    def get_font_size(self) -> int:
        return self.__font_size

    def get_padding_small(self) -> int:
        return self.__padding_small

    def get_padding_big(self) -> int:
        return self.__padding_big

    def get_button_width(self) -> int:
        return self.__button_width

    def get_horizontal_scrollbar_enabled(self) -> bool:
        return self.__horizontal_scrollbar_enabled

    def get_show_extension_entry(self) -> bool:
        return self.__show_extension_entry

    def get_show_full_name_entry(self) -> bool:
        return self.__show_full_name_entry
