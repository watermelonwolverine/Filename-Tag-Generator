import logging
import os.path
import sys
import traceback
from json import JSONDecodeError
from tkinter import Tk, messagebox

import click

from ftg import __version__
from ftg.__cli_wrapper.__args import config_option, tags_option, verbosity_option, verbosity_choices, version_option, \
    verbosity_info, verbosity_debug
from ftg.__cli_wrapper.__constants import win32, linux, bug_report_message, unsupported_os_error_msg
from ftg.__cli_wrapper.__paths import local_path_to_config, user_path_to_config, system_path_to_config, \
    local_path_to_tags, user_path_to_tags, system_path_to_tags
from ftg.__cli_wrapper.__setup import setup
from ftg.__constants import app_name
from ftg.controller.ftg_window_controller import FtgWindowController
from ftg.exceptions import FtgException, FtgInternalException, JsonParseException
from ftg.localization import PLEASE_CHECK_YOUR_FILES_TITLE, PLEASE_CHECK_YOUR_FILES_MSG, FILE_NOT_FOUND
from ftg.utils.program_config import ProgramConfigImpl
from ftg.utils.tags import Tags

supported_platforms = [win32, linux]


@click.command()
@click.option(config_option, type=click.Path(exists=True))
@click.option(tags_option, type=click.Path(exists=True))
@click.option(verbosity_option, type=click.Choice(verbosity_choices, case_sensitive=False))
@click.option(version_option, is_flag=True)
def main(config: str = None,
         tags: str = None,
         verbosity: str = None,
         version: bool = False) -> None:
    # noinspection PyBroadException
    try:
        __check_platform()

        if version:
            print(F"{app_name} version: {__version__}")
            return

        __configure_logging(verbosity)

        path_to_config_file = __try_to_find_config_file(config)

        path_to_tags_file = __try_to_find_tags_file(tags)

        if path_to_tags_file is None:
            setup()
            return

        run_with(path_to_config_file,
                 path_to_tags_file)

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
    if verbosity == verbosity_info:
        __add_logging_stream_handler(logging.INFO)
    elif verbosity == verbosity_debug:
        __add_logging_stream_handler(logging.INFO)
    else:
        logging.disable(logging.CRITICAL)
        logging.disable(logging.ERROR)


def __add_logging_stream_handler(level: int):
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    root.addHandler(handler)


def __try_to_find_config_file(given_path_to_config: str):
    if given_path_to_config is not None:
        return given_path_to_config

    potential_path_to_config = local_path_to_config()

    if os.path.exists(potential_path_to_config):
        return potential_path_to_config

    potential_path_to_config = user_path_to_config()

    if os.path.exists(potential_path_to_config):
        return potential_path_to_config

    potential_path_to_config = system_path_to_config()

    if os.path.exists(potential_path_to_config):
        return potential_path_to_config

    return None


def __try_to_find_tags_file(given_path_to_tags: str):
    if given_path_to_tags is not None:
        raise FtgException(F"File not found: {given_path_to_tags}")

    potential_path_to_tags = local_path_to_tags()

    if os.path.exists(potential_path_to_tags):
        return potential_path_to_tags

    potential_path_to_tags = user_path_to_tags()

    if os.path.exists(potential_path_to_tags):
        return potential_path_to_tags

    potential_path_to_tags = system_path_to_tags()

    if os.path.exists(potential_path_to_tags):
        return potential_path_to_tags

    return None


def run_with(path_to_config_file,
             path_to_tags_file):
    try:
        if path_to_tags_file is not None and not os.path.exists(path_to_tags_file):
            raise FileNotFoundError(FILE_NOT_FOUND.format(path_to_tags_file))

        if path_to_tags_file is not None:
            tags: Tags = Tags.parse_file(path_to_tags_file)
        else:
            raise FtgException()

    except FileNotFoundError as ex:

        __show_error_for_file(FILE_NOT_FOUND,
                              str(ex))
        return
    except (JSONDecodeError, JsonParseException) as ex:

        message = PLEASE_CHECK_YOUR_FILES_MSG.format(path_to_tags_file,
                                                     ex)

        __show_error_for_file(PLEASE_CHECK_YOUR_FILES_TITLE,
                              message)
        return

    try:
        if path_to_config_file is not None and not os.path.exists(path_to_config_file):
            raise FileNotFoundError(F"File not found: {path_to_config_file}")

        if path_to_config_file is not None:
            config = ProgramConfigImpl.parse_file(path_to_config_file)
        else:
            config = ProgramConfigImpl()

    except FileNotFoundError as ex:

        __show_error_for_file(FILE_NOT_FOUND,
                              str(ex))
        return

    except (JSONDecodeError, JsonParseException) as ex:

        message = PLEASE_CHECK_YOUR_FILES_MSG.format(path_to_config_file,
                                                     ex)
        __show_error_for_file(PLEASE_CHECK_YOUR_FILES_TITLE,
                              message)
        return

    ftg_window_controller = FtgWindowController(config,
                                                tags)

    ftg_window_controller.start()
    sys.exit()


def __show_error_for_file(title,
                          message):
    tk = Tk()

    messagebox.showerror(title=title,
                         message=message)

    tk.destroy()
    sys.exit()


if __name__ == "__main__":
    main()
