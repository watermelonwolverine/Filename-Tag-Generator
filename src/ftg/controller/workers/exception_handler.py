import logging
import os
import traceback
from tkinter import messagebox, Tk

import appdirs

from ftg.__constants import app_name, author, crash_report_file_name, UTF_8, issues_url
from ftg.localization import UNEXPECTED_ERROR_TITLE, UNEXPECTED_ERROR_MSG


class FtgExceptionHandler:

    def __init__(self,
                 tk: Tk):
        self.tk = tk
        self.__handling_exception = False

        self.__path_to_log_dir = appdirs.user_log_dir(appname=app_name,
                                                      appauthor=author)

        self.__path_to_log_file = os.path.join(self.__path_to_log_dir,
                                               crash_report_file_name)

    def __create_crash_file(self,
                            *args) -> None:

        crash_report_txt = traceback.format_exception(*args)

        if not os.path.exists(self.__path_to_log_dir):
            os.makedirs(self.__path_to_log_dir)

        with open(self.__path_to_log_file, "wt", encoding=UTF_8) as fh:
            fh.write("".join(crash_report_txt))

    def handle_exception(self,
                         *args) -> None:
        if self.__handling_exception:
            return

        # noinspection PyBroadException
        try:
            self.__handling_exception = True

            self.__create_crash_file(*args)

            msg = UNEXPECTED_ERROR_MSG.format(self.__path_to_log_file,
                                              issues_url)

            messagebox.showerror(title=UNEXPECTED_ERROR_TITLE,
                                 message=msg)

        except BaseException as exception:
            logging.critical(exception)
            pass

        self.tk.destroy()
