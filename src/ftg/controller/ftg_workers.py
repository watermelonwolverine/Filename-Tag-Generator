from ftg.config import FtgConfig
from ftg.controller.ftg_context import FtgContext
from ftg.controller.workers.applier import FtgApplier
from ftg.controller.workers.clearer import FtgClearer
from ftg.controller.workers.reverter import FtgReverter
from ftg.controller.workers.utils import FtgUtils
from ftg.utils.filename_generator import FilenameGeneratorImpl


class FtgWorkers:

    def __init__(self,
                 config: FtgConfig,
                 context: FtgContext):
        filename_generator = FilenameGeneratorImpl(config.get_filename_config())

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

        # avoid circular import
        from ftg.controller.workers.dropper import FtgDropper
        self.dropper: FtgDropper = FtgDropper(context,
                                              self,
                                              filename_generator)
