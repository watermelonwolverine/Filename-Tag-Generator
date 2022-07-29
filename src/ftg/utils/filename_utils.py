import os
from typing import List, Dict

from ftg.utils.name_generator import NameGenerator


def extract_tags_for_selected_files(filename_generator: NameGenerator,
                                    paths: List[str]) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}

    for path in paths:
        _, filename = os.path.split(path)
        reversion_result = filename_generator.revert(filename)
        result[path] = reversion_result.tags

    return result


def extract_extensions_for_selected_files(filename_generator: NameGenerator,
                                          paths: List[str]) -> Dict[str, str]:
    result: Dict[str, str] = {}

    for path in paths:
        _, filename = os.path.split(path)
        reversion_result = filename_generator.revert(filename)
        result[path] = reversion_result.extension

    return result


def extract_basenames_for_selected_files(filename_generator: NameGenerator,
                                         paths: List[str]) -> Dict[str, str]:
    result: Dict[str, str] = {}

    for path in paths:
        _, filename = os.path.split(path)
        reversion_result = filename_generator.revert(filename)
        result[path] = reversion_result.basename

    return result
