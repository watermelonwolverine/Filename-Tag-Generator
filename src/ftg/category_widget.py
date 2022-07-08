from tkinter import ttk, BooleanVar, BOTH, LEFT, Label
from typing import Dict, List

from ftg.config import UIConfig
from ftg.styles import Styles
from ftg.tag_list_widget import TagListWidget


class CategoriesWidget:

    def __init__(self,
                 parent,
                 config: UIConfig,
                 categories: Dict[str, List[str]],
                 checkbox_values: Dict[str, BooleanVar],
                 styles: Styles):
        self.__config = config
        self.__categories = categories
        self.__checkbox_values = checkbox_values
        self.__styles = styles

        self.__root_frame = ttk.Frame(parent)
        self.__add_categories()

    def as_frame(self):
        return self.__root_frame

    def __add_categories(self) -> None:
        for category in self.__categories.keys():
            frame = ttk.Frame(self.__root_frame)
            frame.pack(fill=BOTH,
                       side=LEFT,
                       expand=True)

            Label(frame,
                  text=category,
                  font=self.__styles.get_bold_font()).pack(pady=self.__config.get_padding_small())

            TagListWidget(frame,
                          self.__config,
                          self.__categories[category],
                          self.__checkbox_values,
                          self.__styles)
