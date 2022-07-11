import os
from tkinter import messagebox, DISABLED
from typing import List, Dict

import ftg.utils.filename_utils
from ftg.__constants import READONLY, MULTIPLE_FILES_SELECTED, SINGLE_FILE_SELECTED
from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.ftg_window_controller_workers import FtgWindowControllerWorkers
from ftg.controller.workers.drop_event_data_processor import extract_paths
from ftg.utils import tag_utils
from ftg.utils.filename_generator import FilenameGenerator


class FtgDropper:

    def __init__(self,
                 context: FtgWindowControllerContext,
                 workers: FtgWindowControllerWorkers,
                 filename_generator: FilenameGenerator):
        self.__context = context
        self.__workers = workers
        self.__filename_generator = filename_generator

    def drop_files(self,
                   event) -> None:

        paths = extract_paths(event.data)

        for path in paths:
            if not os.path.isfile(path):
                messagebox.showerror(title="Error",
                                     message="Only files are supported")
                return

        self.__workers.clearer.clear()

        if len(paths) > 1:
            self.__context.view.basename_entry.configure(state=READONLY)
            self.__context.view.extension_entry.configure(state=READONLY)
            self.__context.view.selected_file_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__context.view.filename_result_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__context.view.basename_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__context.view.extension_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__workers.utils.enable_checkbutton_indicators(True)

            self.__context.tags_for_selected_files = ftg.utils.filename_utils.extract_tags_for_selected_files(
                self.__filename_generator,
                paths)
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

    def __set_checkbutton_tristates(self,
                                    tags_for_selected_paths: Dict[str, List[str]]) -> None:

        states = tag_utils.get_check_button_tri_states(self.__context.tags,
                                                       tags_for_selected_paths)

        for tag in self.__context.tags:
            self.__context.view.checkbox_values[tag].set(states[tag])
