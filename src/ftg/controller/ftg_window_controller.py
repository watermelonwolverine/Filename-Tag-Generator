from typing import Dict, List

from tkdnd import DND_FILES

from ftg.config import FtgConfig
from ftg.controller import tag_utils
from ftg.controller.ftg_context import FtgContext
from ftg.controller.workers import FtgWorkers
from ftg.view.ftg_window_view import FtgWindowView


class FtgWindowController:

    def __init__(self,
                 config: FtgConfig,
                 categories: Dict[str, List[str]]):
        tags = tag_utils.get_sorted_tags(categories)

        view = FtgWindowView(config.get_ui_config(),
                             categories,
                             tags)

        self.__context = FtgContext(tags,
                                    view)

        self.__workers = FtgWorkers(config,
                                    self.__context)

        self.__configure_view(view)

    def start(self):
        self.__context.view.as_tk().mainloop()

    def __configure_view(self,
                         view: FtgWindowView):
        view.as_tk().drop_target_register(DND_FILES)
        view.as_tk().dnd_bind('<<Drop>>', lambda event: self.__workers.dropper.drop_files(event))

        def do_revert():
            self.__workers.reverter.revert(self.__context.view.filename_result_string_var.get())

        view.revert_button.configure(command=do_revert)
        view.generate_button.configure(command=lambda: self.__generate())
        view.apply_button.configure(command=lambda: self.__workers.applier.apply())
        view.clear_button.configure(command=lambda: self.__workers.clearer.clear())

    def __generate(self) -> None:
        self.__context.view.filename_result_string_var.set(
            self.__workers.applier.generate_filename())
