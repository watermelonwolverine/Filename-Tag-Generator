from tkinter import ttk, StringVar, BooleanVar, BOTTOM, BOTH, Tk, Frame, X, LEFT, Entry, Button, RIGHT
from typing import Dict, List

from ftg.category_widget import CategoriesWidget
from ftg.config import FtgConfig
from ftg.filename_generator import FilenameGeneratorImpl
from ftg.styles import Styles, StylesImpl


class FtgWindow:

    def __init__(self,
                 config: FtgConfig,
                 categories: Dict[str, List[str]]):
        self.__filename_generator = FilenameGeneratorImpl(config.get_filename_config())
        self.__config = config.get_ui_config()
        self.__categories = categories
        self.__tags = self.__get_sorted_tags(self.__categories)

        # noinspection PyTypeChecker
        self.__styles: Styles = None
        # noinspection PyTypeChecker
        self.__base_name_string_var: StringVar = None
        # noinspection PyTypeChecker
        self.__extension_string_var: StringVar = None
        self.__checkbox_values: Dict[str, BooleanVar] = {}
        # noinspection PyTypeChecker
        self.__filename_result_string_var: StringVar = None
        # noinspection PyTypeChecker
        self.__search_result_string_var: StringVar = None

    def __get_sorted_tags(self,
                          categories_dict: Dict) -> List[str]:
        result = []

        for tag_list in categories_dict.values():
            for tag in tag_list:
                if tag not in result:
                    result.append(tag)
        return sorted(result)

    def start(self):
        tk = self.__init_ui()
        tk.mainloop()

    def __init_ui(self) -> Tk:
        tk = Tk()
        tk.title("Filename Tag Generator")

        tk.minsize(width=500,
                   height=500)

        self.__styles = StylesImpl(self.__config.get_font_size())

        for tag in self.__tags:
            self.__checkbox_values[tag.lower()] = BooleanVar()

        root_frame = ttk.Frame(tk,
                               padding=self.__config.get_padding_small())

        root_frame.pack(fill=BOTH,
                        expand=True)

        self.__add_base_name_input(root_frame)

        self.__add_extension_input(root_frame)

        self.__add_result_frame(root_frame, BOTTOM)

        self.__add_buttons(root_frame, BOTTOM)

        CategoriesWidget(root_frame,
                         self.__config,
                         self.__categories,
                         self.__checkbox_values,
                         self.__styles).as_frame().pack(side=BOTTOM,
                                                        fill=BOTH,
                                                        expand=True)
        return tk

    def __add_base_name_input(self,
                              parent_frame: Frame) -> None:
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=X,
                   pady=self.__config.get_padding_small())

        ttk.Label(frame,
                  text="Base Name",
                  font=self.__styles.get_normal_font(),
                  width=10).pack(side=LEFT)

        self.__base_name_string_var = StringVar()

        Entry(frame,
              textvariable=self.__base_name_string_var,
              font=self.__styles.get_normal_font()).pack(side=LEFT,
                                                         padx=self.__config.get_padding_small(),
                                                         fill=X,
                                                         expand=True)

    def __add_extension_input(self,
                              parent_frame: Frame) -> None:
        frame = Frame(parent_frame)
        frame.pack(fill=X,
                   pady=self.__config.get_padding_small())

        ttk.Label(frame,
                  text="Extension",
                  font=self.__styles.get_normal_font(),
                  width=10).pack(side=LEFT)

        self.__extension_string_var = StringVar()

        Entry(frame,
              textvariable=self.__extension_string_var,
              font=self.__styles.get_normal_font()).pack(side=LEFT,
                                                         padx=self.__config.get_padding_small(),
                                                         fill=X,
                                                         expand=True)

    def __add_result_frame(self,
                           parent_frame: Frame,
                           side) -> None:

        frame = ttk.Frame(parent_frame)
        frame.pack(side=side,
                   fill=X)

        self.__add_filename_frame(frame)

    def __add_filename_frame(self,
                             parent_frame: Frame) -> None:
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=X,
                   expand=False)

        ttk.Label(frame,
                  text="Filename",
                  font=self.__styles.get_normal_font(),
                  width=8).pack(side=LEFT)

        self.__filename_result_string_var = StringVar()
        entry = Entry(frame,
                      textvariable=self.__filename_result_string_var,
                      font=self.__styles.get_normal_font())

        entry.pack(pady=self.__config.get_padding_small(),
                   fill=X,
                   expand=True,
                   side=LEFT)

    def __add_buttons(self,
                      parent_frame: Frame,
                      side) -> None:

        frame = ttk.Frame(parent_frame)
        frame.pack(fill=X,
                   pady=self.__config.get_padding_big(),
                   side=side)

        clear_button = Button(frame,
                              text="Clear",
                              command=lambda: self.__clear())

        clear_button["font"] = self.__styles.get_normal_font()

        revert_button = Button(frame,
                               text="Revert",
                               command=lambda: self.__revert())
        revert_button['font'] = self.__styles.get_normal_font()

        generate_button = Button(frame,
                                 text="Generate",
                                 command=lambda: self.__generate())
        generate_button["font"] = self.__styles.get_normal_font()

        clear_button.pack(side=RIGHT,
                          padx=self.__config.get_padding_big(),
                          expand=True,
                          fill=X)
        revert_button.pack(side=RIGHT,
                           padx=self.__config.get_padding_big(),
                           fill=X,
                           expand=True)
        generate_button.pack(side=RIGHT,
                             padx=self.__config.get_padding_big(),
                             fill=X,
                             expand=True)

    def __clear_checkboxes(self):
        for boolean_var in self.__checkbox_values.values():
            boolean_var.set(False)

    def __clear(self):
        self.__clear_checkboxes()
        self.__filename_result_string_var.set("")
        self.__search_result_string_var.set("")

    def __generate(self):
        result = self.__filename_generator.generate_filename(
            self.__base_name_string_var.get(),
            self.__get_checked_tags(),
            self.__extension_string_var.get())
        self.__filename_result_string_var.set(result)

    def __get_checked_tags(self):
        result = []

        for tag in self.__checkbox_values.keys():
            if self.__checkbox_values[tag].get():
                result.append(tag)

        return result

    def __revert(self):

        filename = self.__filename_result_string_var.get()

        revert_result = self.__filename_generator.revert(filename)

        self.__clear_checkboxes()

        self.__extension_string_var.set(revert_result.extension)

        self.__base_name_string_var.set(revert_result.basename)

        for tag in revert_result.tags:
            if tag in self.__checkbox_values.keys():
                self.__checkbox_values[tag].set(True)
