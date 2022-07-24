import os
import shutil
from tkinter import messagebox
from typing import List

import ftg.utils.filename_utils
from ftg.__constants import ON_STATE_VALUE
from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.workers.utils import FtgUtils
from ftg.utils import tag_utils
from ftg.utils.filename_generator import NameGenerator


class FtgApplier:

    def __init__(self,
                 context: FtgWindowControllerContext,
                 filename_generator: NameGenerator,
                 utils: FtgUtils):
        self.__context = context
        self.__filename_generator = filename_generator
        self.__utils = utils

    def apply(self) -> None:

        if len(self.__context.selected_files) == 1:

            new_filename = self.generate_filename()

            old_path = self.__context.selected_files[0]

            new_path = self.__rename_file(old_path,
                                          new_filename)

            self.__context.selected_files = [new_path]

        elif len(self.__context.selected_files) > 1:

            if len(self.__context.selected_files) >= 10:
                answer = messagebox.askyesno(title="Confirm Action",
                                             message="You are about to rename a lot of files, are you sure you want to continue?")

                if not answer:
                    return

            extensions = ftg.utils.filename_utils.extract_extensions_for_selected_files(
                self.__filename_generator,
                self.__context.selected_files)
            basenames = ftg.utils.filename_utils.extract_basenames_for_selected_files(
                self.__filename_generator,
                self.__context.selected_files)

            new_selected_files = [path for path in self.__context.selected_files]

            for old_path in self.__context.selected_files:
                old_tags = self.__context.tags_for_selected_files[old_path]
                override_tag_states = {tag: int_var.get() for tag, int_var in
                                       self.__context.view.checkbox_values.items()}
                override_tags = tag_utils.override_tags(
                    old_tags,
                    override_tag_states)

                new_filename = self.__filename_generator.generate_filename(basenames[old_path],
                                                                           override_tags,
                                                                           extensions[old_path])

                new_path = self.__rename_file(old_path,
                                              new_filename)

                new_selected_files.remove(old_path)
                new_selected_files.append(new_path)

            self.__context.selected_files = new_selected_files
            self.__context.tags_for_selected_files = ftg.utils.filename_utils.extract_tags_for_selected_files(
                self.__filename_generator,
                new_selected_files)

        else:
            messagebox.showerror(title="Unexpected Error",
                                 message="An unexpected error occurred.")
            return

        self.__context.changes_are_pending = False

    def generate_filename(self) -> str:
        return self.__filename_generator.generate_filename(
            self.__context.view.basename_string_var.get(),
            self.__get_checked_tags(),
            self.__context.view.extension_string_var.get())

    def __get_checked_tags(self) -> List[str]:
        result = []

        for tag in self.__context.view.checkbox_values.keys():
            if self.__context.view.checkbox_values[tag].get() == ON_STATE_VALUE:
                result.append(tag)

        return result

    def __rename_file(self,
                      old_path: str,
                      new_filename: str) -> str:
        folder, old_filename = os.path.split(old_path)

        if len(new_filename) > 255:
            messagebox.showerror(title="Filename too long",
                                 message=F"Unable to rename {old_filename} to {new_filename}. Filename is too long.")
            return old_path

        new_path = os.path.join(folder,
                                new_filename)

        old_path = os.path.normpath(old_path)
        new_path = os.path.normpath(new_path)

        if old_path == new_path:
            return old_path

        if os.path.exists(new_path):
            messagebox.showerror(title="Error Renaming File",
                                 message=F"Cannot rename {old_filename} to {new_filename}. Path already exists")
            return old_path

        shutil.move(old_path,
                    new_path)

        return new_path
