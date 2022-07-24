import os
from tkinter import messagebox, DISABLED, NORMAL
from typing import List, Dict

import ftg.utils.filename_utils
from ftg.__constants import READONLY, MULTIPLE_FILES_SELECTED, NO, PENDING_CHANGES_TITLE, PENDING_CHANGES_MESSAGE
from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.ftg_window_controller_workers import FtgWindowControllerWorkers
from ftg.controller.workers.drop_event_data_processor import extract_paths
from ftg.utils import tag_utils
from ftg.utils.filename_generator import NameGenerator


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

        for path in paths:
            if not os.path.isfile(path):
                messagebox.showerror(title="Error",
                                     message="Only files are supported")
                return

        if self.__context.changes_are_pending:
            result = messagebox.askquestion(title=PENDING_CHANGES_TITLE,
                                            message=PENDING_CHANGES_MESSAGE)

            if result == NO:
                return

        self.__workers.clearer.clear()

        self.__context.selected_files = paths

        self.__context.tags_for_selected_files = ftg.utils.filename_utils.extract_tags_for_selected_files(
            self.__filename_generator,
            paths)

        if len(paths) > 1:
            self.__context.view.basename_entry.configure(state=READONLY)
            self.__context.view.extension_entry.configure(state=READONLY)
            self.__context.view.selected_file_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__workers.utils.enable_checkbutton_indicators(True)

            self.__set_checkbutton_tristates(self.__context.tags_for_selected_files)
            self.__context.view.apply_button.configure(state=NORMAL)

        elif len(paths) == 1:
            self.__context.view.apply_button.configure(state=NORMAL)
            self.__context.view.selected_file_string_var.set(paths[0])

            _, filename = os.path.split(paths[0])

            self.__workers.reverter.revert(filename)
            self.__context.view.filename_result_string_var.set(filename)

        else:
            messagebox.showerror(title="Unexpected Error",
                                 message="An unexpected error occurred.")
            return

        self.__context.view.filename_entry.configure(state=READONLY)
        self.__context.view.revert_button.configure(state=DISABLED)
        self.__context.changes_are_pending = False  # have to do this after setting all the checkboxes and stuff

        self.__check_for_unknown_tags()

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

        for abs_path_to_file, tags in unrecognized_tags.items():

            _, filename = os.path.split(abs_path_to_file)

            joined_tags = ", ".join(tags)

            message_queue = F"{nb + 1}/{len(unrecognized_tags)}"

            message = "WARNING\n" \
                      "\n" \
                      F"{filename} contains unknown tags which will get lost when you apply:\n" \
                      "\n" \
                      F"{joined_tags}\n" \
                      "\n" \
                      F"({message_queue})"

            should_continue = messagebox.askokcancel(title="Unknown Tag",
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
