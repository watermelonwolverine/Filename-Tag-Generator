import os
import sys
from typing import List

import appdirs

import ftg
from ftg.__constants import app_name, author, default_config_file_name, default_tags_file_name


def local_config_dir() -> str:
    parent_dir, _ = os.path.split(path_to_executable())

    return parent_dir


def path_to_executable() -> str:
    if getattr(sys, 'frozen', False):
        # pyinstaller exe
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(ftg.__file__)


def user_config_dir() -> str:
    return appdirs.user_config_dir(app_name,
                                   author)


def system_config_dir() -> str:
    return appdirs.site_config_dir(app_name,
                                   author)


def local_path_to_config() -> str:
    return os.path.join(
        local_config_dir(),
        default_config_file_name)


def user_path_to_config() -> str:
    return os.path.join(
        user_config_dir(),
        default_config_file_name)


def system_path_to_config() -> str:
    return os.path.join(
        system_config_dir(),
        default_config_file_name)


def path_to_config_options() -> List[str]:
    return [local_path_to_config(),
            user_path_to_config(),
            system_path_to_config()]


def local_path_to_tags() -> str:
    return os.path.join(
        local_config_dir(),
        default_tags_file_name)


def user_path_to_tags() -> str:
    return os.path.join(
        user_config_dir(),
        default_tags_file_name)


def system_path_to_tags() -> str:
    return os.path.join(
        system_config_dir(),
        default_tags_file_name)


def path_to_tags_options() -> List[str]:
    return [local_path_to_tags(),
            user_path_to_tags(),
            system_path_to_tags()]
