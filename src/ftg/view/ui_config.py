from abc import ABC


class UIConfig(ABC):
    def get_font_size(self) -> int:
        raise NotImplementedError()

    def get_padding_small(self) -> int:
        raise NotImplementedError()

    def get_padding_big(self) -> int:
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
