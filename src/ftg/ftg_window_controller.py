import os
import shutil
from tkinter import messagebox, DISABLED
from typing import Dict, List

from tkdnd import DND_FILES

from ftg.__constants import on_state_value, off_state_value, mixed_state_value
from ftg.config import FtgConfig
from ftg.filename_generator import FilenameGeneratorImpl
from ftg.ftg_window_view import FtgWindowView

NORMAL = "normal"
READONLY = "readonly"
MULTIPLE_FILES_SELECTED = ""
SINGLE_FILE_SELECTED = ""


class FtgWindowController:

    def __init__(self,
                 config: FtgConfig,
                 categories: Dict[str, List[str]]):

        self.__config = config
        self.__tags = self.__get_sorted_tags(categories)

        self.__filename_generator = FilenameGeneratorImpl(config.get_filename_config())

        self.__view = self.__create_view(categories)
        self.__configure_view(self.__view)

        self.__selected_files = []
        # used for batch processing
        self.__tags_for_selected_files: Dict[str, List[str]] = {}

    def start(self):
        self.__view.as_tk().mainloop()

    def __get_sorted_tags(self,
                          categories_dict: Dict) -> List[str]:
        result = []

        for tag_list in categories_dict.values():
            for tag in tag_list:
                if tag not in result:
                    result.append(tag)
        return sorted(result)

    def __create_view(self,
                      categories: Dict[str, List[str]]) -> FtgWindowView:

        return FtgWindowView(self.__config.get_ui_config(),
                             categories,
                             self.__tags)

    def __configure_view(self,
                         view: FtgWindowView):

        view.as_tk().drop_target_register(DND_FILES)
        view.as_tk().dnd_bind('<<Drop>>', lambda event: self.__drop_files(event))

        def do_revert():
            self.__revert(self.__view.filename_result_string_var.get())

        view.revert_button.configure(command=do_revert)
        view.generate_button.configure(command=lambda: self.__generate())
        view.apply_button.configure(command=lambda: self.__apply())
        view.clear_button.configure(command=lambda: self.__clear())

    def __revert(self,
                 filename: str):

        revert_result = self.__filename_generator.revert(filename)

        self.__clear_checkboxes()

        self.__view.extension_string_var.set(revert_result.extension)

        self.__view.basename_string_var.set(revert_result.basename)

        for tag in revert_result.tags:
            if tag in self.__view.checkbox_values.keys():
                self.__view.checkbox_values[tag].set(on_state_value)

    def __clear_checkboxes(self):
        for int_var in self.__view.checkbox_values.values():
            int_var.set(off_state_value)

    def __clear(self):
        self.__clear_checkboxes()

        self.__view.filename_entry.configure(state=NORMAL)
        self.__view.basename_entry.configure(state=NORMAL)
        self.__view.extension_entry.configure(state=NORMAL)

        self.__view.filename_result_string_var.set("")
        self.__view.selected_file_string_var.set("")
        if self.__view.basename_string_var.get() == MULTIPLE_FILES_SELECTED:
            self.__view.basename_string_var.set("")
        if self.__view.extension_string_var.get() == MULTIPLE_FILES_SELECTED:
            self.__view.extension_string_var.set("")

        self.__view.hide_selected_file_widgets()

        self.__selected_files = []
        self.__tags_for_selected_files = {}
        self.__tag_overrides_of_selected_files = {}

        self.__view.generate_button.configure(state=NORMAL)
        self.__view.revert_button.configure(state=NORMAL)

        self.__enable_checkbutton_indicators(False)

    def __generate(self) -> None:

        self.__view.filename_result_string_var.set(
            self.__generate_filename())

    def __generate_filename(self) -> str:
        return self.__filename_generator.generate_filename(
            self.__view.basename_string_var.get(),
            self.__get_checked_tags(),
            self.__view.extension_string_var.get())

    def __get_checked_tags(self) -> List[str]:
        result = []

        for tag in self.__view.checkbox_values.keys():
            if self.__view.checkbox_values[tag].get() == on_state_value:
                result.append(tag)

        return result

    def __drop_files(self,
                     event) -> None:

        self.__clear()

        paths = self.extract_paths(event.data)

        if len(paths) > 1:
            self.__view.basename_entry.configure(state=READONLY)
            self.__view.extension_entry.configure(state=READONLY)
            self.__view.selected_file_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__view.filename_result_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__view.basename_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__view.extension_string_var.set(MULTIPLE_FILES_SELECTED)
            self.__enable_checkbutton_indicators(True)

            self.__tags_for_selected_files = self.__extract_tags_for_selected_files(paths)
            self.__set_checkbutton_tristates(self.__tags_for_selected_files)
            self.__view.show_apply_button()

        elif len(paths) == 1:
            self.__view.show_selected_file_frame()
            self.__view.show_apply_button()
            self.__view.selected_file_string_var.set(paths[0])

            _, filename = os.path.split(paths[0])

            self.__revert(filename)
            self.__view.filename_result_string_var.set(filename)

            self.__view.filename_result_string_var.set(SINGLE_FILE_SELECTED)

        else:
            messagebox.showerror(title="Unexpected Error",
                                 message="An unexpected error occurred.")
            return

        self.__view.filename_entry.configure(state=READONLY)
        self.__view.generate_button.configure(state=DISABLED)
        self.__view.revert_button.configure(state=DISABLED)
        self.__selected_files = paths

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

    def __apply(self) -> None:

        if len(self.__selected_files) == 1:

            new_filename = self.__generate_filename()

            old_path = self.__selected_files[0]

            new_path = self.__rename_file(old_path,
                                          new_filename)

            self.__selected_files = [new_path]

        elif len(self.__selected_files) > 1:

            extensions = self.__extract_extensions_for_selected_files(
                self.__selected_files)
            basenames = self.__extract_basenames_for_selected_files(
                self.__selected_files)

            new_selected_files = [path for path in self.__selected_files]

            for old_path in self.__selected_files:
                old_tags = self.__tags_for_selected_files[old_path]
                override_tag_states = {tag: int_var.get() for tag, int_var in self.__view.checkbox_values.items()}
                override_tags = self.__override_tags(old_tags,
                                                     override_tag_states)

                new_filename = self.__filename_generator.generate_filename(basenames[old_path],
                                                                           override_tags,
                                                                           extensions[old_path])

                new_path = self.__rename_file(old_path,
                                              new_filename)

                new_selected_files.remove(old_path)
                new_selected_files.append(new_path)

            self.__selected_files = new_selected_files
            self.__tags_for_selected_files = self.__extract_tags_for_selected_files(new_selected_files)

        else:
            messagebox.showerror(title="Unexpected Error",
                                 message="An unexpected error occurred.")

    def __rename_file(self,
                      old_path: str,
                      new_filename: str) -> str:
        folder, old_filename = os.path.split(old_path)

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

    def __enable_checkbutton_indicators(self,
                                        indicatoron: bool) -> None:

        checkbuttons = self.__view.categories_widget.get_all_checkbuttons()

        for checkbutton in checkbuttons:
            checkbutton.configure(indicatoron=indicatoron)

    def __set_checkbutton_tristates(self,
                                    tags_for_selected_paths: Dict[str, List[str]]) -> None:

        states = self.__get_check_button_tri_states(tags_for_selected_paths)

        for tag in self.__tags:
            self.__view.checkbox_values[tag].set(states[tag])

    def __get_check_button_tri_states(self,
                                      tags_for_selected_paths: Dict[str, List[str]]) -> Dict[str, int]:

        num_files = len(tags_for_selected_paths)

        # count occurences of each tag across all tags
        tag_counts: Dict[str, int] = {tag: 0 for tag in self.__tags}

        for tag in self.__tags:
            for tag_list in tags_for_selected_paths.values():
                if tag in tag_list:
                    tag_counts[tag] += 1

        # use counts to determine state
        states: Dict[str, int] = {}

        for tag in self.__tags:
            if tag_counts[tag] == num_files:
                states[tag] = on_state_value
            elif tag_counts[tag] == 0:
                states[tag] = off_state_value
            else:
                states[tag] = mixed_state_value

        return states

    def __extract_tags_for_selected_files(self,
                                          paths: List[str]):
        result: Dict[str, List[str]] = {}

        for path in paths:
            _, filename = os.path.split(path)
            reversion_result = self.__filename_generator.revert(filename)
            result[path] = reversion_result.tags

        return result

    def __extract_extensions_for_selected_files(self,
                                                paths: List[str]):
        result: Dict[str, str] = {}

        for path in paths:
            _, filename = os.path.split(path)
            reversion_result = self.__filename_generator.revert(filename)
            result[path] = reversion_result.extension

        return result

    def __extract_basenames_for_selected_files(self,
                                               paths: List[str]):
        result: Dict[str, str] = {}

        for path in paths:
            _, filename = os.path.split(path)
            reversion_result = self.__filename_generator.revert(filename)
            result[path] = reversion_result.basename

        return result

    def __override_tags(self,
                        old_tags: List[str],
                        override_tag_states: Dict[str, int]) -> List[str]:

        tag_states: Dict[str, bool] = {}

        for tag in self.__tags:
            if override_tag_states[tag] == on_state_value \
                    or override_tag_states[tag] == off_state_value:
                tag_states[tag] = override_tag_states[tag] == on_state_value
            else:
                tag_states[tag] = tag in old_tags

        result: List[str] = []

        for tag in self.__tags:
            if tag_states[tag]:
                result.append(tag)

        return result
