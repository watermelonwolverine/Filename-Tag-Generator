from tkinter import DISABLED

from ftg.__constants import NORMAL, OFF_STATE_VALUE
from ftg.view.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.view.controller.workers.utils import FtgUtils
from ftg.localization import NO_FILE_SELECTED
from ftg.name_generator import NameGenerator


class FtgClearer:

    def __init__(self,
                 context: FtgWindowControllerContext,
                 filename_generator: NameGenerator,
                 utils: FtgUtils):
        self.__context = context
        self.__filename_generator = filename_generator
        self.__utils = utils

    def clear(self):
        self.__context.changes_are_pending = False
        self.__context.selected_files = []
        self.__context.tags_for_selected_files = {}

        self.clear_checkboxes()

        self.__context.view.filename_entry.configure(state=NORMAL)
        self.__context.view.basename_entry.configure(state=NORMAL)
        self.__context.view.extension_entry.configure(state=NORMAL)
        self.__context.view.apply_button.configure(state=DISABLED)

        self.__context.view.filename_result_string_var.set("")
        self.__context.view.selected_file_string_var.set("")
        self.__context.view.basename_string_var.set("")
        self.__context.view.extension_string_var.set("")

        self.__context.view.selected_file_string_var.set(NO_FILE_SELECTED)

        self.__context.view.revert_button.configure(state=NORMAL)

        self.__utils.enable_checkbutton_indicators(False)

    def clear_checkboxes(self):
        for int_var in self.__context.view.checkbox_values.values():
            int_var.set(OFF_STATE_VALUE)
