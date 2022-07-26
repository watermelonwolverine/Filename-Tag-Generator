from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.workers.applier import FtgApplier
from ftg.controller.workers.clearer import FtgClearer
from ftg.controller.workers.exception_handler import FtgExceptionHandler
from ftg.controller.workers.reverter import FtgReverter
from ftg.controller.workers.utils import FtgUtils
from ftg.utils.naming_config import NamingConfig
from ftg.utils.filename_generator import NameGeneratorImpl


class FtgWindowControllerWorkers:

    def __init__(self,
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

        self.exception_handler: FtgExceptionHandler = FtgExceptionHandler(context.view.as_tk())

        # avoid circular import
        from ftg.controller.workers.dropper import FtgDropper
        self.dropper: FtgDropper = FtgDropper(context,
                                              self,
                                              filename_generator)
