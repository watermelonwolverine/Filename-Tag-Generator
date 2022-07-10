from ftg.config import FtgConfig
from ftg.controller.clearer import FtgClearer

from ftg.controller.filename_generator import FilenameGeneratorImpl
from ftg.controller.ftg_applier import FtgApplier
from ftg.controller.ftg_context import FtgContext
from ftg.controller.reverter import FtgReverter
from ftg.controller.utils import FtgUtils


class FtgWorkers:

    def __init__(self,
                 config: FtgConfig,
                 context: FtgContext):
        filename_generator = FilenameGeneratorImpl(config.get_filename_config())

        self.utils = FtgUtils(context,
                              filename_generator)

        self.applier = FtgApplier(context,
                                  filename_generator,
                                  self.utils)

        self.reverter = FtgReverter(context,
                                    filename_generator,
                                    self.utils)

        self.clearer = FtgClearer(context,
                                  filename_generator,
                                  self.utils)

        # avoid cirular import
        from ftg.controller.dropper import FtgDropper
        self.dropper = FtgDropper(context,
                                  self)
