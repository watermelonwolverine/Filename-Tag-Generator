import os
from tkinter import messagebox, DISABLED
from typing import Dict, List

from tkdnd import DND_FILES

from ftg.__constants import ON_STATE_VALUE, OFF_STATE_VALUE
from ftg.config import FtgConfig
from ftg.controller.ftg_applier import FtgApplier
from ftg.controller.filename_generator import FilenameGeneratorImpl
from ftg.controller.ftg_context import FtgContext
from ftg.controller.utils import FtgUtils
from ftg.view.ftg_window_view import FtgWindowView

NORMAL = "normal"
READONLY = "readonly"
MULTIPLE_FILES_SELECTED = ""
SINGLE_FILE_SELECTED = ""


class FtgWindowController:

    def __init__(self,
                 config: FtgConfig,
                 categories: Dict[str, List[str]]):

        tags = self.__get_sorted_tags(categories)

        view = FtgWindowView(config.get_ui_config(),
                             categories,
                             tags)

        self.__context = FtgContext(tags,
                                    view)

        self.__filename_generator = FilenameGeneratorImpl(config.get_filename_config())

        self.__utils = FtgUtils(self.__filename_generator)

        self.__applier = FtgApplier(self.__context,
                                    self.__filename_generator,
                                    self.__utils)

        self.__configure_view(view)

    def start(self):
        self.__context.view.as_tk().mainloop()

    def __get_sorted_tags(self,
                          categories_dict: Dict) -> List[str]:
        result = []

        for tag_list in categories_dict.values():
            for tag in tag_list:
                if tag not in result:
                    result.append(tag)
        return sorted(result)

    def __configure_view(self,
                         view: FtgWindowView):

        view.as_tk().drop_target_register(DND_FILES)
        view.as_tk().dnd_bind('<<Drop>>', lambda event: self.__drop_files(event))

        def do_revert():
            self.__revert(self.__context.view.filename_result_string_var.get())

        view.revert_button.configure(command=do_revert)
        view.generate_button.configure(command=lambda: self.__generate())
        view.apply_button.configure(command=lambda: self.__applier.apply())
        view.clear_button.configure(command=lambda: self.__clear())

    def __revert(self,
                 filename: str):

        revert_result = self.__filename_generator.revert(filename)

        self.__clear_checkboxes()

        self.__context.view.extension_string_var.set(revert_result.extension)

        self.__context.view.basename_string_var.set(revert_result.basename)

        for tag in revert_result.tags:
            if tag in self.__context.view.checkbox_values.keys():
                self.__context.view.checkbox_values[tag].set(ON_STATE_VALUE)

    def __clear_checkboxes(self):
        for int_var in self.__context.view.checkbox_values.values():
            int_var.set(OFF_STATE_VALUE)

    def __clear(self):
        self.__clear_checkboxes()

        self.__context.view.filename_entry.configure(state=NORMAL)
        self.__context.view.basename_entry.configure(state=NORMAL)
        self.__context.view.extension_entry.configure(state=NORMAL)

        self.__context.view.filename_result_string_var.set("")
        self.__context.view.selected_file_string_var.set("")
        if self.__context.view.basename_string_var.get() == MULTIPLE_FILES_SELECTED:
            self.__context.view.basename_string_var.set("")
        if self.__context.view.extension_string_var.get() == MULTIPLE_FILES_SELECTED:
            self.__context.view.extension_string_var.set("")

        self.__context.view.hide_selected_file_widgets()

        self.__context.clear()

        self.__context.view.generate_button.configure(state=NORMAL)
        self.__context.view.revert_button.configure(state=NORMAL)

        self.__enable_checkbutton_indicators(False)

    def __generate(self) -> None:

        self.__context.view.filename_result_string_var.set(
            self.__applier.generate_filename())

    def __drop_files(self,
                     event) -> None:

        self.__clear()

        paths = self.extract_paths(event.data)

        if len(paths) > 1:
            self.__context.view.basename_entry.configure(state=READONLY)
            self.__context.view.extension_entry.configure(state=READONLY)
            self.__context.view.selected_file_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__context.view.filename_result_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__context.view.basename_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__context.view.extension_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__enable_checkbutton_indicators(True)

            self.__context.tags_for_selected_files = self.__utils.extract_tags_for_selected_files(paths)
            self.__set_checkbutton_tristates(self.__context.tags_for_selected_files)
            self.__context.view.show_apply_button()

        elif len(paths) == 1:
            self.__context.view.show_selected_file_frame()
            self.__context.view.show_apply_button()
            self.__context.view.selected_file_string_var.set(paths[0])

            _, filename = os.path.split(paths[0])

            self.__revert(filename)
            self.__context.view.filename_result_string_var.set(filename)

            self.__context.view.filename_result_string_var.set(SINGLE_FILE_SELECTED)

        else:
            messagebox.showerror(title="Unexpected Error",
                                 message="An unexpected error occurred.")
            return

        self.__context.view.filename_entry.configure(state=READONLY)
        self.__context.view.generate_button.configure(state=DISABLED)
        self.__context.view.revert_button.configure(state=DISABLED)
        self.__context.selected_files = paths

    def extract_paths(self,
                      drop_event_data: str) -> List[str]:

        paths: List[str] = drop_event_data.split(" ")

        result = []

        for path in paths:
            trimmed_path = self.trim_path(path)
            normed_path = os.path.normpath(trimmed_path)
            result.append(normed_path)

        return result

    def trim_path(self,
                  path: str):
        result = path

        if result.startswith('{'):
            result = result.lstrip('{')
            result = result.rstrip('}')

        return result

    def __enable_checkbutton_indicators(self,
                                        indicatoron: bool) -> None:

        checkbuttons = self.__context.view.categories_widget.get_all_checkbuttons()

        for checkbutton in checkbuttons:
            checkbutton.configure(indicatoron=indicatoron)

    def __set_checkbutton_tristates(self,
                                    tags_for_selected_paths: Dict[str, List[str]]) -> None:

        states = self.__utils.get_check_button_tri_states(self.__context.tags,
                                                          tags_for_selected_paths)

        for tag in self.__context.tags:
            self.__context.view.checkbox_values[tag].set(states[tag])
