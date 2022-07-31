import os
import shutil
import sys
from tkinter import messagebox
from typing import List, Dict, Iterable, Union

from ftg.__cli_wrapper.__constants import win32, linux
from ftg.__constants import ON_STATE_VALUE
from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.workers.utils import FtgUtils
from ftg.exceptions import FtgException
from ftg.localization import ERROR_TITLE
from ftg.utils import tag_utils, filename_utils
from ftg.utils.name_generator import NameGenerator

FILENAME_LENGTH_LIMIT = 255

tmp_marker_len = 5
tmp_markers = ["~tmp" + str(i) for i in range(0, 9)]


class FtgApplier:

    def __init__(self,
                 context: FtgWindowControllerContext,
                 name_generator: NameGenerator,
                 utils: FtgUtils):
        self.__context = context
        self.__name_generator = name_generator
        self.__utils = utils

    def apply(self) -> None:

        if len(self.__context.selected_files) == 1:
            self.__apply_single()
        elif len(self.__context.selected_files) > 1:
            self.__apply_batch()
        else:
            raise Exception("Illegal Program State")

    def __apply_single(self) -> None:

        old_path = None
        new_path = None

        try:

            self.check()

            new_filename = self.generate_full_name()

            old_path = self.__context.selected_files[0]

            folder, _ = os.path.split(old_path)

            new_path = os.path.join(folder, new_filename)

            self.__rename_file(old_path,
                               new_path)

            self.__context.selected_files = [new_path]

            self.__context.changes_are_pending = False

        except (FtgException, OSError) as ex:
            msg = self.__error_msg_for_exception(old_path,
                                                 new_path,
                                                 ex)
            messagebox.showerror(title="Error",
                                 message=msg)

    def __apply_batch(self) -> None:

        if len(self.__context.selected_files) >= 10:
            answer = messagebox.askyesno(title="Confirm Action",
                                         message="You are about to rename a lot of files, are you sure you want to continue?")
            if not answer:
                return

        updated_paths: Dict[str, str] = {}

        for old_path in self.__context.selected_files:
            try:
                updated_paths[old_path] = self.__new_path_for(old_path)
            except FtgException as ex:
                messagebox.showerror(title=ERROR_TITLE,
                                     message=F"Error while generating filenames: {ex}")
                return

        if self.__contains_duplicate_paths(updated_paths.values()):
            answer = messagebox.askyesno(title="Filename Collision",
                                         message="Cannot rename all files as it would lead to colliding filenames. Do you want to continue?\n"
                                                 "If you click yes some file will not be renamed.")
            if not answer:
                return

        if self.__contains_too_long_filenames(updated_paths.values()):
            answer = messagebox.askyesno(title="Filenames Too Long",
                                         message="Cannot rename all files as some filenames would be too long. Do you want to continue?\n"
                                                 "If you click yes some file will not be renamed.")
            if not answer:
                return

        self.__do_batch_rename(updated_paths)
        self.__context.changes_are_pending = False

    def __do_batch_rename(self,
                          updated_paths: Dict[str, str]) -> None:

        new_selected_files = self.__context.selected_files.copy()

        skip_warnings = False

        for old_path, new_path in updated_paths.items():

            try:
                self.__rename_file(old_path,
                                   new_path)
                new_selected_files.remove(old_path)
                new_selected_files.append(new_path)

            except (FtgException, OSError) as ex:
                if skip_warnings:
                    continue

                answer = self.__handle_batch_renaming_exception(old_path,
                                                                new_path,
                                                                ex)
                if answer is None:
                    break
                if not answer:
                    skip_warnings = True

        self.__context.selected_files = new_selected_files
        self.__context.tags_for_selected_files = filename_utils.extract_tags_for_selected_files(
            self.__name_generator,
            new_selected_files)

    def __handle_batch_renaming_exception(self,
                                          old_path: str,
                                          new_path: str,
                                          ex) -> Union[bool, None]:

        question = str('\n'
                       '\n'
                       'Yes: Continue batch process\n'
                       'No: Continue and skip all warnings\n'
                       'Cancel: Stop batch process\n')

        msg = self.__error_msg_for_exception(old_path,
                                             new_path,
                                             ex) + question

        return messagebox.askyesnocancel(title="Error",
                                         message=msg)

    @classmethod
    def __error_msg_for_exception(cls,
                                  old_path,
                                  new_path,
                                  ex):
        if issubclass(type(ex), FtgException):

            return str(F'Cannot rename {old_path} to {new_path}.\n'
                       F'\n'
                       F'Reason: {ex}')

        elif issubclass(type(ex), OSError):

            return str(F'Cannot rename {old_path} to {new_path}.\n'
                       F'\n'
                       F'OSError: {ex}\n'
                       F'\n'
                       F'This usually means:\n'
                       F'- You are using illegal characters\n'
                       F'- You don\'t have the permission\n'
                       F'- The file was deleted\n'
                       F'- The file was moved')

        raise Exception("BIG OOF")

    @classmethod
    def __contains_duplicate_paths(cls,
                                   paths: Iterable[str]) -> bool:

        if sys.platform == win32:
            paths = [path.lower() for path in paths]
        elif sys.platform == linux:
            pass
        else:
            raise NotImplementedError()

        return len(paths) != len(set(paths))

    @classmethod
    def __contains_too_long_filenames(cls,
                                      paths: Iterable[str]) -> bool:

        for path in paths:
            _, filename = os.path.split(path)
            if len(filename) > FILENAME_LENGTH_LIMIT:
                return True

        return False

    def __new_path_for(self,
                       old_path: str):

        old_dir, old_filename = os.path.split(old_path)

        old_tags = self.__context.tags_for_selected_files[old_path]
        override_tag_states = {tag: int_var.get() for tag, int_var in
                               self.__context.view.checkbox_values.items()}
        override_tags = tag_utils.override_tags(
            old_tags,
            override_tag_states)

        reversion_result = self.__name_generator.revert(old_filename)

        self.__name_generator.check(reversion_result.basename,
                                    override_tags,
                                    reversion_result.extension)

        new_filename = self.__name_generator.generate_filename(reversion_result.basename,
                                                               override_tags,
                                                               reversion_result.extension)

        return os.path.join(old_dir, new_filename)

    def check(self):
        self.__name_generator.check(self.__context.view.basename_string_var.get(),
                                    self.__get_checked_tags(),
                                    self.__context.view.extension_string_var.get())

    def generate_full_name(self) -> str:

        return self.__name_generator.generate_filename(
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
                      new_path: str) -> None:

        # does not fail on ubuntu if file was moved but should
        if not os.path.exists(old_path):
            raise FileNotFoundError(F"File not found: {old_path}")

        _, old_filename = os.path.split(old_path)
        _, new_filename = os.path.split(new_path)

        if len(new_filename) > 255:
            raise FtgException("Filename is too long.")

        if old_path == new_path:
            return

        if os.path.exists(new_path):
            # Windows ignores capitalization
            if sys.platform == win32:
                if old_path.lower() == new_path.lower():
                    # capitalization changed but everything else stayed the same
                    # Windows won't let us rename file
                    tmp_path = self.__get_tmp_path(old_path)

                    if tmp_path is None:
                        raise FtgException("Cannot create temp file.")

                    shutil.move(old_path, tmp_path)
                    shutil.move(tmp_path, new_path)
                    return
                else:
                    raise FtgException("Path already exists")
            elif sys.platform == linux:
                raise FtgException("Path already exists")
            else:
                raise NotImplementedError()

        shutil.move(old_path,
                    new_path)

    @classmethod
    def __get_tmp_path(cls,
                       old_path: str) -> Union[str, None]:

        folder, filename = os.path.split(old_path)

        for tmp_marker in tmp_markers:
            if len(filename) + tmp_marker_len > FILENAME_LENGTH_LIMIT:
                tmp_path = old_path[:-tmp_marker_len] + tmp_marker
            else:
                tmp_path = old_path + tmp_marker

            if not os.path.exists(tmp_path):
                return tmp_path

        return None
