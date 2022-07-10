from ftg.controller.ftg_context import FtgContext
from ftg.utils.filename_generator import FilenameGenerator


class FtgUtils:

    def __init__(self,
                 context: FtgContext,
                 filename_generator: FilenameGenerator):
        self.__context = context
        self.__filename_generator = filename_generator

    def enable_checkbutton_indicators(self,
                                      indicatoron: bool) -> None:
        checkbuttons = self.__context.view.categories_widget.get_all_checkbuttons()

        for checkbutton in checkbuttons:
            checkbutton.configure(indicatoron=indicatoron)
