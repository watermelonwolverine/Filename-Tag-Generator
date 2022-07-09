from tkinter import ttk, BOTH, LEFT, Label, Checkbutton, IntVar
from typing import Dict, List

from ftg.config import UIConfig
from ftg.styles import Styles
from ftg.tag_list_widget import TagListWidget


class CategoriesWidget:

    def __init__(self,
                 parent,
                 config: UIConfig,
                 categories: Dict[str, List[str]],
                 checkbox_values: Dict[str, IntVar],
                 styles: Styles):
        self.__config = config
        self.__categories = categories
        self.__checkbox_values = checkbox_values
        self.__styles = styles

        self.__tag_list_widgets: List[TagListWidget] = []
        self.__root_frame = ttk.Frame(parent)
        self.__add_categories()

    def as_frame(self):
        return self.__root_frame

    def get_all_checkbuttons(self) -> List[Checkbutton]:
        result: List[Checkbutton] = []

        for tag_list_widget in self.__tag_list_widgets:
            result += tag_list_widget.check_buttons

        return result

    def __add_categories(self) -> None:
        for category_name, category_tags in self.__categories.items():
            frame = ttk.Frame(self.__root_frame)
            frame.pack(fill=BOTH,
                       side=LEFT,
                       expand=True)

            Label(frame,
                  text=category_name.capitalize(),
                  font=self.__styles.get_bold_font()).pack(pady=self.__config.get_padding_small())

            tag_list_widget = TagListWidget(frame,
                                            self.__config,
                                            category_tags,
                                            self.__checkbox_values,
                                            self.__styles)

            self.__tag_list_widgets.append(tag_list_widget)
