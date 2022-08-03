import tkinter
from tkinter import ttk, BOTH, LEFT, RIGHT, Y, VERTICAL, Canvas, Frame, Checkbutton, IntVar
from typing import List, Dict

from ftg.__constants import ON_STATE_VALUE, OFF_STATE_VALUE, MIXED_STATE_VALUE
from ftg.config.program_config import UIConfig
from ftg.utils.scroll_config import configure_mousewheel_vertical_scrolling, \
    configure_canvas_and_interior_vertical_scroll
from ftg.utils.tag import Tag
from ftg.view.styles import Styles


class TagListWidget:

    def __init__(self,
                 parent,
                 config: UIConfig,
                 tags: List[Tag],
                 checkbox_values: Dict[str, IntVar],
                 styles: Styles):

        self.__config = config
        self.__tags = tags
        self.__checkbox_values = checkbox_values
        self.__styles = styles
        self.check_buttons: List[Checkbutton] = []

        self.__root_frame = ttk.Frame(parent)
        self.__add_tag_list()

    def as_frame(self):
        return self.__root_frame

    def __add_tag_list(self) -> None:

        self.__root_frame.pack(fill=BOTH,
                               expand=True)

        scrollbar = ttk.Scrollbar(self.__root_frame,
                                  orient=VERTICAL)
        scrollbar.pack(side=RIGHT,
                       fill=Y)

        canvas = Canvas(self.__root_frame,
                        yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT,
                    fill=BOTH,
                    expand=True)

        scrollbar.config(command=canvas.yview)

        tag_list_grid_frame = ttk.Frame(canvas)

        # seems that 0 makes it only as big as it needs to be
        tag_list_grid_frame.columnconfigure(0, weight=0)
        tag_list_grid_frame.columnconfigure(1, weight=1)

        configure_canvas_and_interior_vertical_scroll(canvas, tag_list_grid_frame)
        configure_mousewheel_vertical_scrolling(canvas, tag_list_grid_frame)
        self.__add_tags_to_frame(tag_list_grid_frame)

    def __add_tags_to_frame(self,
                            tag_list_grid_frame: Frame) -> None:

        current_first_letter = ""

        row = 0

        for tag in sorted(self.__tags):
            int_var = self.__checkbox_values[tag.letter_code]

            max_nb_of_chars = self.__config.get_button_width()

            full_name = tag.full_name

            if len(full_name) > max_nb_of_chars:
                full_name = full_name[:max_nb_of_chars - 3] + "..."

            check_button = Checkbutton(tag_list_grid_frame,
                                       text=full_name,
                                       variable=int_var,
                                       onvalue=ON_STATE_VALUE,
                                       offvalue=OFF_STATE_VALUE,
                                       tristatevalue=MIXED_STATE_VALUE,
                                       indicatoron=False,
                                       width=self.__config.get_button_width())

            check_button["font"] = self.__styles.get_normal_font()

            check_button.grid(column=1,
                              row=row,
                              sticky=tkinter.EW)

            self.check_buttons.append(check_button)

            first_letter = tag.letter_code[0]
            label_text = ""
            if first_letter != current_first_letter:
                label_text = first_letter

            ttk.Label(tag_list_grid_frame,
                      text=label_text.upper(),
                      font=self.__styles.get_bold_font()).grid(column=0,
                                                               row=row,
                                                               sticky=tkinter.EW)

            current_first_letter = first_letter
            row += 1
