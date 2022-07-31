import os
from typing import List

import appdirs

from ftg.__constants import app_name, author, default_config_file_name, default_tags_file_name


def user_config_dir() -> str:
    return appdirs.user_config_dir(app_name,
                                   author)


def system_config_dir() -> str:
    return appdirs.site_config_dir(app_name,
                                   author)


def user_path_to_config() -> str:
    return os.path.join(
        user_config_dir(),
        default_config_file_name)


def system_path_to_config() -> str:
    return os.path.join(
        system_config_dir(),
        default_config_file_name)


def path_to_config_options() -> List[str]:
    return [user_path_to_config(),
            system_path_to_config()]


def user_path_to_tags() -> str:
    return os.path.join(
        user_config_dir(),
        default_tags_file_name)


def system_path_to_tags() -> str:
    return os.path.join(
        system_config_dir(),
        default_tags_file_name)


def path_to_tags_options() -> List[str]:
    return [user_path_to_tags(),
            system_path_to_tags()]
