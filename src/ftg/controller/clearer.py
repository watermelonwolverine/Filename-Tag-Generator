from ftg.controller.filename_generator import FilenameGenerator
from ftg.controller.ftg_context import FtgContext
from ftg.__constants import NORMAL, MULTIPLE_FILES_SELECTED
from ftg.controller.utils import FtgUtils


class FtgClearer:

    def __init__(self,
                 context: FtgContext,
                 filename_generator: FilenameGenerator,
                 utils: FtgUtils):
        self.__context = context
        self.__filename_generator = filename_generator
        self.__utils = utils

    def clear(self):
        self.__utils.clear_checkboxes()

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
