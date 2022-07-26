import tkinter
from tkinter import Tk, Text, BOTH, Toplevel

from ftg.view.styles import Styles
from ftg.view.ui_config import UIConfig


class FtgHelpDialog:

    def __init__(self,
                 parent: Tk,
                 config: UIConfig,
                 styles: Styles):
        self.__root = Toplevel(parent)
        self.__root.title("Help")
        self.__root.minsize(400, 400)
        self.__config = config
        self.__styles = styles

        self.__build_ui()

    def __build_ui(self):
        text = Text(self.__root,
                    pady=self.__config.get_padding_small(),
                    padx=self.__config.get_padding_small(),
                    font=self.__styles.get_normal_font())

        text.insert(tkinter.END, "blablabla, mister freeman")

        text.pack(fill=BOTH,
                  expand=True)
