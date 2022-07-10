from ftg.__constants import ON_STATE_VALUE
from ftg.controller.filename_generator import FilenameGenerator
from ftg.controller.ftg_context import FtgContext
from ftg.controller.utils import FtgUtils


class FtgReverter:

    def __init__(self,
                 context: FtgContext,
                 filename_generator: FilenameGenerator,
                 utils: FtgUtils):
        self.__context = context
        self.__filename_generator = filename_generator
        self.__utils = utils

    def revert(self,
               filename: str):

        revert_result = self.__filename_generator.revert(filename)

        self.__utils.clear_checkboxes()

        self.__context.view.extension_string_var.set(revert_result.extension)

        self.__context.view.basename_string_var.set(revert_result.basename)

        for tag in revert_result.tags:
            if tag in self.__context.view.checkbox_values.keys():
                self.__context.view.checkbox_values[tag].set(ON_STATE_VALUE)
