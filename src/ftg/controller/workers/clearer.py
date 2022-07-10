from ftg.__constants import NORMAL, MULTIPLE_FILES_SELECTED, OFF_STATE_VALUE
from ftg.controller.ftg_context import FtgContext
from ftg.utils.filename_generator import FilenameGenerator
from ftg.controller.workers.utils import FtgUtils


class FtgClearer:

    def __init__(self,
                 context: FtgContext,
                 filename_generator: FilenameGenerator,
                 utils: FtgUtils):
        self.__context = context
        self.__filename_generator = filename_generator
        self.__utils = utils

    def clear(self):
        self.clear_checkboxes()

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

        self.__utils.enable_checkbutton_indicators(False)

    def clear_checkboxes(self):
        for int_var in self.__context.view.checkbox_values.values():
            int_var.set(OFF_STATE_VALUE)
