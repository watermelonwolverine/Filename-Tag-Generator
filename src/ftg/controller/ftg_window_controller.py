from tkinter import messagebox
from typing import Dict, List

from tkdnd import DND_FILES

from ftg.__constants import PENDING_CHANGES_TITLE, PENDING_CHANGES_MESSAGE, NO
from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.ftg_window_controller_workers import FtgWindowControllerWorkers
from ftg.utils.program_config import ProgramConfig
from ftg.utils.tag import Tag
from ftg.view.ftg_window import FtgWindow


class FtgWindowController:

    def __init__(self,
                 config: ProgramConfig,
                 tags: List[Tag],
                 categories: Dict[str, List[Tag]]):
        view = FtgWindow(config.get_ui_config(),
                         tags,
                         categories)

        self.__context = FtgWindowControllerContext(tags,
                                                    view)

        self.__workers = FtgWindowControllerWorkers(config,
                                                    self.__context)

        self.__configure_view(view)

    def start(self):
        self.__workers.clearer.clear()
        self.__context.view.as_tk().mainloop()

    def __configure_view(self,
                         view: FtgWindow):
        view.as_tk().drop_target_register(DND_FILES)
        view.as_tk().dnd_bind('<<Drop>>', lambda event: self.__workers.dropper.drop_files(event))

        def do_revert():
            self.__workers.reverter.revert(self.__context.view.filename_result_string_var.get())

        view.revert_button.configure(command=do_revert)
        view.apply_button.configure(command=lambda: self.__workers.applier.apply())
        view.clear_button.configure(command=lambda: self.__workers.clearer.clear())

        self.__add_listeners()

    def __add_listeners(self):

        # noinspection PyUnusedLocal
        def on_change_callback(*args, **kwargs):
            self.__on_change_callback()

        for tag_var in self.__context.view.checkbox_values.values():
            tag_var.trace_variable(mode="w",
                                   callback=on_change_callback)

        self.__context.view.extension_string_var.trace_variable(mode="w",
                                                                callback=on_change_callback)

        self.__context.view.basename_string_var.trace_variable(mode="w",
                                                               callback=on_change_callback)

        # noinspection PyUnusedLocal
        def on_close_callback(*args, **kwargs):
            self.__on_close_callback()

        self.__context.view.as_tk().protocol("WM_DELETE_WINDOW",
                                             on_close_callback)

    def __generate(self) -> None:
        self.__context.view.filename_result_string_var.set(
            self.__workers.applier.generate_filename())

    def __on_change_callback(self):
        if len(self.__context.selected_files) > 0:
            self.__context.changes_are_pending = True

        if len(self.__context.selected_files) < 2:
            self.__generate()

    def __on_close_callback(self):
        if self.__context.changes_are_pending:
            result = messagebox.askquestion(title=PENDING_CHANGES_TITLE,
                                            message=PENDING_CHANGES_MESSAGE)

            if result == NO:
                return

        self.__context.view.as_tk().destroy()
