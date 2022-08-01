from tkinter import messagebox
from typing import List

from ftg.__constants import ON_STATE_VALUE
from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.workers.clearer import FtgClearer
from ftg.utils.name_generator import NameGenerator, ReversionResult


class FtgReverter:

    def __init__(self,
                 context: FtgWindowControllerContext,
                 clearer: FtgClearer,
                 filename_generator: NameGenerator):
        self.__context = context
        self.__clearer = clearer
        self.__filename_generator = filename_generator

    def revert(self,
               fullname: str):

        revert_result = self.__filename_generator.revert(fullname)

        unknown_tags = self.__find_unknown_tags(revert_result)

        if len(unknown_tags) > 0:
            if not self.__ask_user_if_continue(fullname,
                                               unknown_tags):
                return

        self.__clearer.clear_checkboxes()

        self.__context.view.extension_string_var.set(revert_result.extension)

        self.__context.view.basename_string_var.set(revert_result.basename)

        for tag in revert_result.tags:
            if tag in self.__context.view.checkbox_values.keys():
                self.__context.view.checkbox_values[tag].set(ON_STATE_VALUE)

    def __find_unknown_tags(self,
                            revert_result: ReversionResult) -> List[str]:

        known_tags = [tag.letter_code for tag in self.__context.tags.tags]

        result = list()

        for tag in revert_result.tags:
            if tag not in known_tags:
                result.append(tag)

        return result

    @classmethod
    def __ask_user_if_continue(cls,
                               fullname: str,
                               unknown_tags: List[str]):

        joined_tags = ", ".join(unknown_tags)

        message = str("WARNING\n"
                      "\n"
                      F'"{fullname}" contains unknown tags which will get lost:\n'
                      "\n"
                      F"{joined_tags}")

        answer = messagebox.askokcancel(title="Unknown Tags",
                                        message=message)
        return answer
