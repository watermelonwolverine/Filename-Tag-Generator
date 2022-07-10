import os
from typing import Dict, List

from ftg.__constants import OFF_STATE_VALUE
from ftg.controller.filename_generator import FilenameGenerator
from ftg.controller.ftg_context import FtgContext


class FtgUtils:

    def __init__(self,
                 context: FtgContext,
                 filename_generator: FilenameGenerator):

        self.__context = context
        self.__filename_generator = filename_generator

    def extract_tags_for_selected_files(self,
                                        paths: List[str]) -> Dict[str, List[str]]:
        result: Dict[str, List[str]] = {}

        for path in paths:
            _, filename = os.path.split(path)
            reversion_result = self.__filename_generator.revert(filename)
            result[path] = reversion_result.tags

        return result

    def extract_extensions_for_selected_files(self,
                                              paths: List[str]) -> Dict[str, str]:
        result: Dict[str, str] = {}

        for path in paths:
            _, filename = os.path.split(path)
            reversion_result = self.__filename_generator.revert(filename)
            result[path] = reversion_result.extension

        return result

    def extract_basenames_for_selected_files(self,
                                             paths: List[str]) -> Dict[str, str]:
        result: Dict[str, str] = {}

        for path in paths:
            _, filename = os.path.split(path)
            reversion_result = self.__filename_generator.revert(filename)
            result[path] = reversion_result.basename

        return result

    def clear_checkboxes(self):
        for int_var in self.__context.view.checkbox_values.values():
            int_var.set(OFF_STATE_VALUE)

    def enable_checkbutton_indicators(self,
                                      indicatoron: bool) -> None:

        checkbuttons = self.__context.view.categories_widget.get_all_checkbuttons()

        for checkbutton in checkbuttons:
            checkbutton.configure(indicatoron=indicatoron)
