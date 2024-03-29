import logging
import os.path
import sys
import traceback
from json import JSONDecodeError
from tkinter import Tk, messagebox
from typing import List, Union

import click

from ftg import __version__
from ftg.__cli_wrapper import __setup, __args
from ftg.__cli_wrapper.__constants import win32, linux, bug_report_message, unsupported_os_error_msg
from ftg.__cli_wrapper.__paths import path_to_tags_options, path_to_config_options
from ftg.__constants import app_name, window_title
from ftg.__help import command_line_usage
from ftg.config.program_config import ProgramConfigImpl
from ftg.config.tags import Tags
from ftg.view.ftg_window import FtgWindow
from ftg.exceptions import FtgException, FtgInternalException, JSONParseException
from ftg.localization import PLEASE_CHECK_YOUR_FILES_TITLE, PLEASE_CHECK_YOUR_FILES_MSG, FILE_NOT_FOUND

supported_platforms = [win32, linux]


# noinspection PyShadowingBuiltins
@click.command()
@click.option(__args.config_option, type=click.Path(exists=True))
@click.option(__args.tags_option, type=click.Path(exists=True))
@click.option(__args.verbosity_option, type=click.Choice(__args.verbosity_choices, case_sensitive=False))
@click.option(__args.version_option, is_flag=True)
@click.option(__args.setup_option, is_flag=True)
@click.option(__args.help_option, is_flag=True)
def cli_main(config: str = None,
             tags: str = None,
             verbosity: str = None,
             version: bool = False,
             setup: bool = False,
             help: bool = False) -> None:
    main(config,
         tags,
         verbosity,
         version,
         setup,
         help)


# noinspection PyShadowingBuiltins
def main(config: str = None,
         tags: str = None,
         verbosity: str = None,
         version: bool = False,
         setup: bool = False,
         help: bool = False) -> None:
    # noinspection PyBroadException
    try:
        __check_platform()

        if version:
            print(F"{app_name} version: {__version__}")
            return

        if help:
            print(command_line_usage.syntax)
            return

        __configure_logging(verbosity)

        if setup:
            tk = Tk()
            tk.title(window_title)
            __setup.setup()
            tk.destroy()
            sys.exit()

        __try_to_run_with(config,
                          tags)

    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    except FtgInternalException:
        formatted = traceback.format_exc()
        logging.error(formatted)
        print("An internal error occurred: " + str(formatted))
        print(bug_report_message)
    except FtgException as exception:
        # these are expected to happen sometimes - don't print the whole stack
        logging.error(exception)
        print(str(exception))
    except BaseException:
        formatted = traceback.format_exc()
        print(F"An unexpected error occured:\n{formatted}")
        print(bug_report_message)


def __check_platform():
    if sys.platform not in supported_platforms:
        raise FtgException(unsupported_os_error_msg.format(sys.platform))


def __configure_logging(verbosity: str) -> None:
    if verbosity == __args.verbosity_debug:
        __add_logging_stream_handler(logging.DEBUG)
    elif verbosity == __args.verbosity_info:
        __add_logging_stream_handler(logging.INFO)
    elif verbosity == __args.verbosity_error:
        __add_logging_stream_handler(logging.ERROR)
    elif verbosity == __args.verbosity_critical:
        __add_logging_stream_handler(logging.CRITICAL)
    elif verbosity == __args.verbosity_off:
        logging.disable(logging.CRITICAL)
        logging.disable(logging.ERROR)
        logging.disable(logging.WARNING)
        logging.disable(logging.INFO)
        logging.disable(logging.DEBUG)
    # warning is default
    else:
        __add_logging_stream_handler(logging.WARNING)


def __add_logging_stream_handler(level: int):
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    root.addHandler(handler)


def __try_to_run_with(given_path_to_config_file: str,
                      given_path_to_tags_file: str):
    path_to_tags_file = __take_or_look(given_path_to_tags_file,
                                       path_to_tags_options())

    path_to_config_file = __take_or_look(given_path_to_config_file,
                                         path_to_config_options())

    if path_to_tags_file is None:
        tk = Tk()
        tk.title(app_name)
        __setup.maybe_setup()
        tk.destroy()
        sys.exit()

    run_with(path_to_config_file,
             path_to_tags_file)


def __take_or_look(path: str,
                   options: List[str]) -> Union[str, None]:
    if path is None:
        return __look_for(options)
    else:
        if os.path.exists(path):
            return path
        else:
            raise FtgException(F'Error: File does not exists {path}')


def __look_for(options: List[str]) -> Union[str, None]:
    for option in options:
        if os.path.exists(option):
            return option

    return None


def run_with(path_to_config_file,
             path_to_tags_file):
    tags = __try_to_parse_file(path_to_tags_file,
                               lambda: __read_tags_file(path_to_tags_file))

    config = __try_to_parse_file(path_to_config_file,
                                 lambda: __read_config_file(path_to_config_file))

    ftg_window_controller = FtgWindow(config,
                                      tags)

    ftg_window_controller.start()
    sys.exit()


def __try_to_parse_file(path_to_file,
                        parse_function):
    try:
        return parse_function()

    except FileNotFoundError as ex:

        __show_error_for_file(FILE_NOT_FOUND,
                              str(ex))
    except (JSONDecodeError, JSONParseException, FtgException) as ex:

        message = PLEASE_CHECK_YOUR_FILES_MSG.format(path_to_file,
                                                     ex)

        __show_error_for_file(PLEASE_CHECK_YOUR_FILES_TITLE,
                              message)


def __read_tags_file(path_to_tags_file: str) -> Tags:
    if path_to_tags_file is not None and not os.path.exists(path_to_tags_file):
        raise FileNotFoundError(FILE_NOT_FOUND.format(path_to_tags_file))

    if path_to_tags_file is not None:
        return Tags.parse_file(path_to_tags_file)
    else:
        raise FtgException("Missing tags file")


def __read_config_file(path_to_config_file: str):
    if path_to_config_file is not None and not os.path.exists(path_to_config_file):
        raise FileNotFoundError(F"File not found: {path_to_config_file}")

    if path_to_config_file is not None:
        return ProgramConfigImpl.parse_file(path_to_config_file)
    else:
        return ProgramConfigImpl()


def __show_error_for_file(title,
                          message):
    tk = Tk()
    tk.title(window_title)
    messagebox.showerror(title=title,
                         message=message)

    tk.destroy()
    sys.exit()


if __name__ == "__main__":
    cli_main()
