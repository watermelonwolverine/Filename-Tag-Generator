import logging
import os.path
import sys
import traceback

import appdirs
import click

from ftg import __version__
from ftg.__cli_wrapper.__args import config_option, tags_option, verbosity_option, verbosity_choices, version_option, \
    verbosity_info, verbosity_debug
from ftg.__cli_wrapper.__constants import win32, linux, bug_report_message, unsupported_os_error_msg
from ftg.__constants import app_name, default_config_file_name, default_tags_file_name
from ftg.controller.ftg_window_controller import FtgWindowController
from ftg.exceptions import FtgException, FtgInternalException
from ftg.utils.program_config import ProgramConfigImpl
from ftg.utils.tags import Tags

supported_platforms = [win32, linux]


def run_with(path_to_config_file=None,
             path_to_tags_file=None):
    if path_to_config_file is not None:
        config = ProgramConfigImpl.parse_file(path_to_config_file)
    else:
        config = ProgramConfigImpl()

    if path_to_tags_file is not None:
        tags: Tags = Tags.parse_file(path_to_tags_file)
    else:
        tags = Tags([],
                    {})

    ftg_window_controller = FtgWindowController(config,
                                                tags)
    ftg_window_controller.start()
    sys.exit()


def __add_logging_stream_handler(level: int):
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    root.addHandler(handler)


def __configure_logging(verbosity: str) -> None:
    if verbosity == verbosity_info:
        __add_logging_stream_handler(logging.INFO)
    elif verbosity == verbosity_debug:
        __add_logging_stream_handler(logging.INFO)
    else:
        logging.disable(logging.CRITICAL)
        logging.disable(logging.ERROR)


def __check_platform():
    if sys.platform not in supported_platforms:
        raise FtgException(unsupported_os_error_msg.format(sys.platform))


def __get_path_to_executable() -> str:
    if getattr(sys, 'frozen', False):
        # pyinstaller exe
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)


def __try_to_find_config_file(given_path_to_config: str):
    if given_path_to_config is not None:
        if os.path.exists(given_path_to_config):
            return given_path_to_config
        else:
            raise FtgException(F"File not found: {given_path_to_config}")

    potential_path_to_config = os.path.join(
        __get_path_to_executable(),
        default_config_file_name)

    if os.path.exists(potential_path_to_config):
        return potential_path_to_config

    potential_path_to_config = os.path.join(
        appdirs.user_config_dir(),
        app_name,
        default_config_file_name)

    if os.path.exists(potential_path_to_config):
        return potential_path_to_config

    potential_path_to_config = os.path.join(
        appdirs.site_config_dir(),
        app_name,
        default_config_file_name)

    if os.path.exists(potential_path_to_config):
        return potential_path_to_config

    return None


def __try_to_find_tags_file(given_path_to_tags: str):
    if given_path_to_tags is not None:
        if os.path.exists(given_path_to_tags):
            return given_path_to_tags
        else:
            raise FtgException(F"File not found: {given_path_to_tags}")

    potential_path_to_tags = os.path.join(
        __get_path_to_executable(),
        default_tags_file_name)

    if os.path.exists(potential_path_to_tags):
        return potential_path_to_tags

    potential_path_to_tags = os.path.join(
        appdirs.user_config_dir(),
        app_name,
        default_tags_file_name)

    if os.path.exists(potential_path_to_tags):
        return potential_path_to_tags

    potential_path_to_tags = os.path.join(
        appdirs.site_config_dir(),
        app_name,
        default_tags_file_name)

    if os.path.exists(potential_path_to_tags):
        return potential_path_to_tags

    return None


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


if __name__ == "__main__":
    main()
