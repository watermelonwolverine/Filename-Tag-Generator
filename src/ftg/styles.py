from abc import ABC
from tkinter.font import Font


class Styles(ABC):

    def get_normal_font(self) -> Font:
        raise NotImplementedError()

    def get_bold_font(self) -> Font:
        raise NotImplementedError()


class StylesImpl(Styles):

    def __init__(self,
                 font_size):
        self.normal_font = Font(size=font_size)
        self.bold_font = Font(size=font_size)

    def get_normal_font(self) -> Font:
        return self.normal_font

    def get_bold_font(self) -> Font:
        return self.bold_font
