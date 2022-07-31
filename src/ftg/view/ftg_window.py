from tkinter import ttk, StringVar, BOTTOM, BOTH, Tk, Frame, X, LEFT, Entry, Button, RIGHT, TOP, IntVar
from typing import Dict, Literal

from tkinterdnd2 import TkinterDnD

from ftg.__constants import window_title
from ftg.localization import SELECTED_FILE, APPLY, CLEAR, FULL_NAME, EXTENSION, BASENAME, HELP, REVERT
from ftg.utils.program_config import UIConfig
from ftg.utils.tags import Tags
from ftg.view.categories_widget import CategoriesWidget
from ftg.view.styles import Styles, StylesImpl

SIDE = Literal["left", "right", "top", "bottom"]
input_label_width = 13


class FtgWindow:

    def __init__(self,
                 config: UIConfig,
                 tags: Tags):
        self.__config = config
        self.__tags = tags

        self.__tk = TkinterDnD.Tk()

        self.styles: Styles = StylesImpl(self.__config.get_font_size())

        self.__init_checkbutton_vars()

        self.__build_ui(self.__tk)

        self.__create_path_to_selected_file_frame(self.__path_to_selected_file_container)

    def as_tk(self):
        return self.__tk

    def __init_checkbutton_vars(self):
        self.checkbox_values: Dict[str, IntVar] = {}

        for tag in self.__tags.tags:
            self.checkbox_values[tag.letter_code] = IntVar()

    def __build_ui(self,
                   tk: Tk) -> None:
        tk.title(window_title)
        tk.minsize(width=500,
                   height=500)

        root_frame = ttk.Frame(tk,
                               padding=self.__config.get_padding_small())

        root_frame.pack(fill=BOTH,
                        expand=True)

        self.__path_to_selected_file_container = ttk.Frame(root_frame)

        self.__path_to_selected_file_container.pack(side=TOP,
                                                    fill=X,
                                                    expand=False)

        self.__add_basename_input(root_frame)

        self.__add_extension_input(root_frame)

        self.__add_result_frame(root_frame,
                                BOTTOM)

        self.__add_file_manipulation_buttons(root_frame,
                                             BOTTOM)

        self.categories_widget = CategoriesWidget(root_frame,
                                                  self.__config,
                                                  self.__tags.categories,
                                                  self.checkbox_values,
                                                  self.styles)

        self.categories_widget.as_frame().pack(side=BOTTOM,
                                               fill=BOTH,
                                               padx=self.__config.get_padding_big(),
                                               pady=self.__config.get_padding_small(),
                                               expand=True)

    def __create_path_to_selected_file_frame(self,
                                             parent_frame: Frame) -> None:
        frame = ttk.Frame(parent_frame)

        ttk.Label(frame,
                  text=SELECTED_FILE,
                  font=self.styles.get_normal_font(),
                  width=input_label_width).pack(side=LEFT)

        self.selected_file_string_var: StringVar = StringVar()

        entry = ttk.Entry(frame,
                          textvariable=self.selected_file_string_var,
                          font=self.styles.get_normal_font(),
                          state="readonly")

        # I just don't know where else to put this
        self.help_button = Button(frame,
                                  text=HELP)
        self.help_button['font'] = self.styles.get_normal_font()

        entry.pack(side=LEFT,
                   padx=self.__config.get_padding_small(),
                   fill=X,
                   expand=True)

        self.help_button.pack(side=RIGHT,
                              padx=self.__config.get_padding_big(),
                              fill=X)

        frame.pack(fill=X,
                   pady=self.__config.get_padding_small(),
                   side=TOP)

    def __add_basename_input(self,
                             parent_frame: Frame) -> None:
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=X,
                   pady=self.__config.get_padding_small(),
                   side=TOP)

        ttk.Label(frame,
                  text=BASENAME,
                  font=self.styles.get_normal_font(),
                  width=input_label_width).pack(side=LEFT)

        self.basename_string_var: StringVar = StringVar()

        self.basename_entry = Entry(frame,
                                    textvariable=self.basename_string_var,
                                    font=self.styles.get_normal_font())

        self.basename_entry.pack(side=LEFT,
                                 padx=self.__config.get_padding_small(),
                                 fill=X,
                                 expand=True)

    def __add_extension_input(self,
                              parent_frame: Frame) -> None:
        frame = Frame(parent_frame)

        frame.pack(fill=X,
                   pady=self.__config.get_padding_small(),
                   side=TOP)

        ttk.Label(frame,
                  text=EXTENSION,
                  font=self.styles.get_normal_font(),
                  width=input_label_width).pack(side=LEFT)

        self.extension_string_var: StringVar = StringVar()

        self.extension_entry = Entry(frame,
                                     textvariable=self.extension_string_var,
                                     font=self.styles.get_normal_font())

        self.extension_entry.pack(side=LEFT,
                                  padx=self.__config.get_padding_small(),
                                  fill=X,
                                  expand=True)

    def __add_result_frame(self,
                           parent_frame: Frame,
                           side: SIDE) -> None:
        frame = ttk.Frame(parent_frame)
        frame.pack(side=side,
                   fill=X)

        self.__add_full_name_frame(frame)

    def __add_full_name_frame(self,
                              parent_frame: Frame) -> None:
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=X,
                   expand=False)

        ttk.Label(frame,
                  text=FULL_NAME,
                  font=self.styles.get_normal_font(),
                  width=input_label_width).pack(side=LEFT)

        self.filename_result_string_var: StringVar = StringVar()

        self.filename_entry = Entry(frame,
                                    textvariable=self.filename_result_string_var,
                                    font=self.styles.get_normal_font())

        self.filename_entry.pack(fill=BOTH,
                                 expand=True,
                                 side=LEFT)

        self.revert_button = Button(frame,
                                    text=REVERT)
        self.revert_button['font'] = self.styles.get_normal_font()

        self.revert_button.pack(side=RIGHT,
                                padx=self.__config.get_padding_big(),
                                fill=X)

    def __add_file_manipulation_buttons(self,
                                        parent_frame: Frame,
                                        side: SIDE) -> None:
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=X,
                   pady=self.__config.get_padding_small(),
                   side=side)

        self.apply_button = Button(frame,
                                   text=APPLY)

        self.apply_button["font"] = self.styles.get_normal_font()

        self.apply_button.pack(side=LEFT,
                               padx=self.__config.get_padding_big(),
                               expand=True,
                               fill=BOTH)

        self.clear_button = Button(frame,
                                   text=CLEAR)

        self.clear_button["font"] = self.styles.get_normal_font()

        self.clear_button.pack(side=RIGHT,
                               padx=self.__config.get_padding_big(),
                               expand=True,
                               fill=BOTH)
