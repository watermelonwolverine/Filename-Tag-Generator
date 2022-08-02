import os
from tkinter import messagebox, DISABLED, NORMAL
from typing import List, Dict

import ftg.utils.filename_utils
from ftg.__constants import READONLY
from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.ftg_window_controller_workers import FtgWindowControllerWorkers
from ftg.controller.workers.drop_event_data_processor import extract_paths
from ftg.localization import PENDING_CHANGES_TITLE, PENDING_CHANGES_MESSAGE, MULTIPLE_FILES_SELECTED
from ftg.utils import tag_utils
from ftg.utils.name_generator import NameGenerator


class FtgDropper:

    def __init__(self,
                 context: FtgWindowControllerContext,
                 workers: FtgWindowControllerWorkers,
                 filename_generator: NameGenerator):
        self.__context = context
        self.__workers = workers
        self.__filename_generator = filename_generator

    def drop_files(self,
                   event) -> None:

        paths = extract_paths(event.data)

        if not self.__should_continue(paths):
            return

        self.__workers.clearer.clear()

        self.__context.selected_files = paths

        self.__context.tags_for_selected_files = ftg.utils.filename_utils.extract_tags_for_selected_files(
            self.__filename_generator,
            paths)

        if len(paths) > 1:
            self.__drop_multiple_files()

        elif len(paths) == 1:
            self.__drop_single_file(paths[0])

        else:
            raise Exception()

        self.__context.view.filename_entry.configure(state=READONLY)
        self.__context.view.revert_button.configure(state=DISABLED)
        self.__context.changes_are_pending = False  # have to do this after setting all the checkboxes and stuff

    def __drop_single_file(self,
                           path_to_file) -> None:
        self.__context.view.apply_button.configure(state=NORMAL)
        self.__context.view.selected_file_string_var.set(path_to_file)

        _, filename = os.path.split(path_to_file)

        self.__workers.reverter.revert(filename)

    def __drop_multiple_files(self) -> None:
        self.__context.view.basename_entry.configure(state=READONLY)
        self.__context.view.extension_entry.configure(state=READONLY)
        self.__context.view.selected_file_string_var.set(MULTIPLE_FILES_SELECTED)
        self.__workers.utils.enable_checkbutton_indicators(True)

        self.__set_checkbutton_tristates(self.__context.tags_for_selected_files)
        self.__context.view.apply_button.configure(state=NORMAL)

        self.__check_for_unknown_tags()

    def __should_continue(self,
                          paths) -> bool:
        for path in paths:
            if not os.path.isfile(path):
                messagebox.showerror(title="Error",
                                     message="Only files are supported")
                return False

        if self.__context.changes_are_pending:
            result = messagebox.askyesno(title=PENDING_CHANGES_TITLE,
                                         message=PENDING_CHANGES_MESSAGE)

            if not result:
                return False

        return True

    def __check_for_unknown_tags(self):
        tag_lettercodes = [tag.letter_code for tag in self.__context.tags.tags]

        unrecognized_tags: Dict[str, List[str]] = {}

        for abs_path_to_selected_file in self.__context.selected_files:
            tags = self.__context.tags_for_selected_files[abs_path_to_selected_file]

            unrecognized_tags_for_file = []

            for tag in tags:
                if tag not in tag_lettercodes:
                    unrecognized_tags_for_file.append(tag)

            if len(unrecognized_tags_for_file) > 0:
                unrecognized_tags[abs_path_to_selected_file] = unrecognized_tags_for_file

        nb = 0

        for abs_path_to_file, unknown_tags_for_file in unrecognized_tags.items():

            _, filename = os.path.split(abs_path_to_file)

            joined_tags = ", ".join(unknown_tags_for_file)

            message_queue = F"{nb + 1}/{len(unrecognized_tags)}"

            message = str("WARNING\n"
                          "\n"
                          F"{filename} contains unknown tags which will get lost when you apply:\n"
                          "\n"
                          F"{joined_tags}\n"
                          "\n"
                          F"({message_queue})\n"
                          F"\n"
                          F"OK: Next Warning, Cancel: Skip Warnings")

            should_continue = messagebox.askokcancel(title="Unknown Tags",
                                                     message=message)

            if not should_continue:
                break

            nb += 1

    def __set_checkbutton_tristates(self,
                                    tags_for_selected_paths: Dict[str, List[str]]) -> None:
        tag_letter_codes = [tag.letter_code for tag in self.__context.tags.tags]

        states = tag_utils.get_check_button_tri_states(tag_letter_codes,
                                                       tags_for_selected_paths)

        for tag in tag_letter_codes:
            self.__context.view.checkbox_values[tag].set(states[tag])
