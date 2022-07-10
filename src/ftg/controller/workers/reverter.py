from ftg.__constants import ON_STATE_VALUE
from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.workers.clearer import FtgClearer
from ftg.utils.filename_generator import FilenameGenerator


class FtgReverter:

    def __init__(self,
                 context: FtgWindowControllerContext,
                 clearer: FtgClearer,
                 filename_generator: FilenameGenerator):
        self.__context = context
        self.__clearer = clearer
        self.__filename_generator = filename_generator

    def revert(self,
               filename: str):

        revert_result = self.__filename_generator.revert(filename)

        self.__clearer.clear_checkboxes()

        self.__context.view.extension_string_var.set(revert_result.extension)

        self.__context.view.basename_string_var.set(revert_result.basename)

        for tag in revert_result.tags:
            if tag in self.__context.view.checkbox_values.keys():
                self.__context.view.checkbox_values[tag].set(ON_STATE_VALUE)
