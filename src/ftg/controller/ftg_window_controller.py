import sys
from tkinter import messagebox

from tkdnd import DND_FILES

from ftg.controller.ftg_window_controller_context import FtgWindowControllerContext
from ftg.controller.ftg_window_controller_workers import FtgWindowControllerWorkers
from ftg.exceptions import FtgException
from ftg.localization import PENDING_CHANGES_TITLE, PENDING_CHANGES_MESSAGE
from ftg.utils.program_config import ProgramConfig
from ftg.utils.tags import Tags
from ftg.view.ftg_window import FtgWindow
from ftg.view.help.help_dialog import FtgHelpDialog


class FtgWindowController:

    def __init__(self,
                 config: ProgramConfig,
                 tags: Tags):

        self.__config = config

        view = FtgWindow(config.get_ui_config(),
                         tags)

        self.__context = FtgWindowControllerContext(tags,
                                                    view)

        self.__workers = FtgWindowControllerWorkers(config.get_naming_config(),
                                                    self.__context)

        self.__configure_view(view)

    def start(self):
        self.__workers.clearer.clear()
        self.__context.view.as_tk().mainloop()

    def stop(self):
        self.__context.view.as_tk().destroy()
        sys.exit()

    def __configure_view(self,
                         view: FtgWindow):

        def handle_exception(*args):
            self.__workers.exception_handler.handle_exception(*args)

        view.as_tk().report_callback_exception = handle_exception

        view.as_tk().drop_target_register(DND_FILES)
        view.as_tk().dnd_bind('<<Drop>>', lambda event: self.__workers.dropper.drop_files(event))

        def do_revert():
            self.__workers.reverter.revert(self.__context.view.filename_result_string_var.get())

        view.revert_button.configure(command=do_revert)
        view.apply_button.configure(command=lambda: self.__workers.applier.apply())
        view.clear_button.configure(command=lambda: self.__workers.clearer.clear())
        view.help_button.configure(command=lambda: self.__show_help())

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

        try:
            name = self.__workers.applier.generate_full_name()
        except FtgException as ex:
            name = F'Error: {ex}'
        self.__context.view.filename_result_string_var.set(name)

    def __on_change_callback(self):
        if len(self.__context.selected_files) > 0:
            self.__context.changes_are_pending = True

        if len(self.__context.selected_files) < 2:
            self.__generate()

    def __on_close_callback(self):
        if self.__context.changes_are_pending:
            result = messagebox.askyesno(title=PENDING_CHANGES_TITLE,
                                         message=PENDING_CHANGES_MESSAGE)

            if not result:
                return

        self.stop()

    def __show_help(self):
        FtgHelpDialog(self.__context.view.as_tk(),
                      self.__config.get_ui_config(),
                      self.__context.view.styles)
