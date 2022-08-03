from tkinter import Tk

from ftg.config.naming_config import NamingConfig
from ftg.name_generator import NameGeneratorImpl
from ftg.view.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.view.controller.workers.applier import FtgApplier
from ftg.view.controller.workers.clearer import FtgClearer
from ftg.view.controller.workers.exception_handler import FtgExceptionHandler
from ftg.view.controller.workers.reverter import FtgReverter
from ftg.view.controller.workers.utils import FtgUtils


class FtgWindowControllerWorkers:

    def __init__(self,
                 tk: Tk,
                 naming_config: NamingConfig,
                 context: FtgWindowControllerContext):
        filename_generator = NameGeneratorImpl(naming_config)

        self.utils: FtgUtils = FtgUtils(context,
                                        filename_generator)

        self.applier: FtgApplier = FtgApplier(context,
                                              filename_generator,
                                              self.utils)

        self.clearer: FtgClearer = FtgClearer(context,
                                              filename_generator,
                                              self.utils)

        self.reverter: FtgReverter = FtgReverter(context,
                                                 self.clearer,
                                                 filename_generator)

        self.exception_handler: FtgExceptionHandler = FtgExceptionHandler(tk)

        # avoid circular import
        from ftg.view.controller.workers.dropper import FtgDropper
        self.dropper: FtgDropper = FtgDropper(context,
                                              self,
                                              filename_generator)
