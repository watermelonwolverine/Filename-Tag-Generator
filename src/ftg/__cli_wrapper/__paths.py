import os
import sys

import appdirs

from ftg.__constants import app_name, author, default_config_file_name, default_tags_file_name


def local_config_dir() -> str:
    return path_to_executable()


def path_to_executable() -> str:
    if getattr(sys, 'frozen', False):
        # pyinstaller exe
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)


def user_config_dir() -> str:
    return appdirs.user_config_dir(app_name,
                                   author)


def system_config_dir() -> str:
    return appdirs.site_config_dir(app_name,
                                   author)


def local_path_to_config():
    return os.path.join(
        local_config_dir(),
        default_config_file_name)


def user_path_to_config():
    return os.path.join(
        user_config_dir(),
        default_config_file_name)


def system_path_to_config():
    return os.path.join(
        system_config_dir(),
        default_config_file_name)


def local_path_to_tags():
    return os.path.join(
        local_config_dir(),
        default_tags_file_name)


def user_path_to_tags():
    return os.path.join(
        user_config_dir(),
        default_tags_file_name)


def system_path_to_tags():
    return os.path.join(
        system_config_dir(),
        default_tags_file_name)
