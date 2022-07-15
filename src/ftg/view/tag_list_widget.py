import tkinter
from tkinter import ttk, BOTH, LEFT, RIGHT, Y, VERTICAL, Canvas, Frame, NW, Checkbutton, IntVar
from typing import List, Dict

from ftg.__constants import ON_STATE_VALUE, OFF_STATE_VALUE, MIXED_STATE_VALUE
from ftg.utils.program_config import UIConfig
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

        # from here: https://gist.github.com/JackTheEngineer/81df334f3dcff09fd19e4169dd560c59
        self.__configure_canvas_and_interior(canvas, tag_list_grid_frame)
        self.__configure_mousewheel_scrolling(canvas, tag_list_grid_frame)
        self.__add_tags_to_frame(tag_list_grid_frame)

    def __configure_canvas_and_interior(self,
                                        canvas: Canvas,
                                        frame: Frame) -> None:
        tag_list_frame_id = canvas.create_window(0, 0, window=frame,
                                                 anchor=NW)

        def _configure_interior(_):
            # Update the scrollbars to match the size of the inner frame.
            size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
            # noinspection PyTypeChecker
            canvas.config(scrollregion="0 0 %s %s" % size)
            if frame.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=frame.winfo_reqwidth())

        frame.bind('<Configure>', _configure_interior)

        def _configure_canvas(_):
            if frame.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(tag_list_frame_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)

    def __configure_mousewheel_scrolling(self,
                                         canvas: Canvas,
                                         frame: Frame) -> None:

        def _on_mousewheel(event):
            # Don't scroll when everything is visible, avoid weird behavior
            if frame.winfo_height() > canvas.winfo_height():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_to_mousewheel(_):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(_):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)

    def __add_tags_to_frame(self,
                            tag_list_grid_frame: Frame) -> None:

        current_first_letter = ""

        row = 0

        for tag in sorted(self.__tags):
            int_var = self.__checkbox_values[tag.letter_code]

            check_button = Checkbutton(tag_list_grid_frame,
                                       text=tag.full_name,
                                       variable=int_var,
                                       onvalue=ON_STATE_VALUE,
                                       offvalue=OFF_STATE_VALUE,
                                       tristatevalue=MIXED_STATE_VALUE,
                                       indicatoron=False)

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
