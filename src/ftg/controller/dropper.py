import os
from tkinter import messagebox, DISABLED
from typing import List, Dict

from ftg.__constants import READONLY, MULTIPLE_FILES_SELECTED, SINGLE_FILE_SELECTED
from ftg.controller import tag_utils
from ftg.controller.ftg_context import FtgContext
from ftg.controller.workers import FtgWorkers


class FtgDropper:

    def __init__(self,
                 context: FtgContext,
                 workers: FtgWorkers):
        self.__context = context
        self.__workers = workers

    def drop_files(self,
                   event) -> None:

        self.__workers.clearer.clear()

        paths = self.extract_paths(event.data)

        if len(paths) > 1:
            self.__context.view.basename_entry.configure(state=READONLY)
            self.__context.view.extension_entry.configure(state=READONLY)
            self.__context.view.selected_file_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__context.view.filename_result_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__context.view.basename_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__context.view.extension_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__workers.utils.enable_checkbutton_indicators(True)

            self.__context.tags_for_selected_files = self.__workers.utils.extract_tags_for_selected_files(paths)
            self.__set_checkbutton_tristates(self.__context.tags_for_selected_files)
            self.__context.view.show_apply_button()

        elif len(paths) == 1:
            self.__context.view.show_selected_file_frame()
            self.__context.view.show_apply_button()
            self.__context.view.selected_file_string_var.set(paths[0])

            _, filename = os.path.split(paths[0])

            self.__workers.reverter.revert(filename)
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

    def __set_checkbutton_tristates(self,
                                    tags_for_selected_paths: Dict[str, List[str]]) -> None:

        states = tag_utils.get_check_button_tri_states(self.__context.tags,
                                                       tags_for_selected_paths)

        for tag in self.__context.tags:
            self.__context.view.checkbox_values[tag].set(states[tag])
