from tkinter import messagebox

from ftg.__constants import ON_STATE_VALUE
from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.workers.clearer import FtgClearer
from ftg.utils.name_generator import NameGenerator


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

        known_tags = [tag.letter_code for tag in self.__context.tags.tags]

        unrecognized_tags = list()

        for tag in revert_result.tags:
            if tag not in known_tags:
                unrecognized_tags.append(tag)

        if len(unrecognized_tags) > 0:
            joined_tags = ", ".join(unrecognized_tags)

            message = str("WARNING\n"
                          "\n"
                          F'"{fullname}" contains unknown tags which will get lost:\n'
                          "\n"
                          F"{joined_tags}")

            answer = messagebox.askokcancel(title="Unknown Tags",
                                            message=message)

            if not answer:
                return

        self.__clearer.clear_checkboxes()

        self.__context.view.extension_string_var.set(revert_result.extension)

        self.__context.view.basename_string_var.set(revert_result.basename)

        for tag in revert_result.tags:
            if tag in self.__context.view.checkbox_values.keys():
                self.__context.view.checkbox_values[tag].set(ON_STATE_VALUE)
