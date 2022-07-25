import os
import sys

import appdirs

from ftg.__constants import app_name, author, default_config_file_name, default_tags_file_name


def path_to_executable() -> str:
    if getattr(sys, 'frozen', False):
        # pyinstaller exe
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)


def local_path_to_config():
    return os.path.join(
        path_to_executable(),
        default_config_file_name)


def user_path_to_config():
    return os.path.join(
        appdirs.user_config_dir(app_name,
                                author),
        default_config_file_name)


def system_path_to_config():
    return os.path.join(
        appdirs.site_config_dir(app_name,
                                author),
        default_config_file_name)


def local_path_to_tags():
    return os.path.join(
        path_to_executable(),
        default_tags_file_name)


def user_path_to_tags():
    return os.path.join(
        appdirs.user_config_dir(app_name,
                                author),
        default_tags_file_name)


def system_path_to_tags():
    return os.path.join(
        appdirs.site_config_dir(app_name,
                                author),
        default_tags_file_name)
