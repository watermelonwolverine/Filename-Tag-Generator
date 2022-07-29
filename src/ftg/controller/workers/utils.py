from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.utils.name_generator import NameGenerator


class FtgUtils:

    def __init__(self,
                 context: FtgWindowControllerContext,
                 filename_generator: NameGenerator):
        self.__context = context
        self.__filename_generator = filename_generator

    def enable_checkbutton_indicators(self,
                                      indicatoron: bool) -> None:
        checkbuttons = self.__context.view.categories_widget.get_all_checkbuttons()

        for checkbutton in checkbuttons:
            checkbutton.configure(indicatoron=indicatoron)
