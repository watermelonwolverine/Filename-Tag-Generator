import os
from typing import Dict, List

from ftg.__constants import OFF_STATE_VALUE, ON_STATE_VALUE, MIXED_STATE_VALUE
from ftg.controller.filename_generator import FilenameGenerator


class FtgUtils:

    def __init__(self,
                 filename_generator: FilenameGenerator):
        self.__filename_generator = filename_generator

    def get_check_button_tri_states(self,
                                    all_tags: List[str],
                                    tags_for_selected_paths: Dict[str, List[str]]) -> Dict[str, int]:
        num_files = len(tags_for_selected_paths)

        # count occurrences of each tag across all tags
        tag_counts: Dict[str, int] = {tag: 0 for tag in all_tags}

        for tag in all_tags:
            for tag_list in tags_for_selected_paths.values():
                if tag in tag_list:
                    tag_counts[tag] += 1

        # use counts to determine state
        states: Dict[str, int] = {}

        for tag in all_tags:
            if tag_counts[tag] == num_files:
                states[tag] = ON_STATE_VALUE
            elif tag_counts[tag] == 0:
                states[tag] = OFF_STATE_VALUE
            else:
                states[tag] = MIXED_STATE_VALUE

        return states

    def extract_tags_for_selected_files(self,
                                        paths: List[str]):
        result: Dict[str, List[str]] = {}

        for path in paths:
            _, filename = os.path.split(path)
            reversion_result = self.__filename_generator.revert(filename)
            result[path] = reversion_result.tags

        return result

    def extract_extensions_for_selected_files(self,
                                              paths: List[str]):
        result: Dict[str, str] = {}

        for path in paths:
            _, filename = os.path.split(path)
            reversion_result = self.__filename_generator.revert(filename)
            result[path] = reversion_result.extension

        return result

    def extract_basenames_for_selected_files(self,
                                             paths: List[str]):
        result: Dict[str, str] = {}

        for path in paths:
            _, filename = os.path.split(path)
            reversion_result = self.__filename_generator.revert(filename)
            result[path] = reversion_result.basename

        return result

    def override_tags(self,
                      all_tags: List[str],
                      old_tags: List[str],
                      override_tag_states: Dict[str, int]) -> List[str]:
        tag_states: Dict[str, bool] = {}

        for tag in all_tags:
            if override_tag_states[tag] == ON_STATE_VALUE \
                    or override_tag_states[tag] == OFF_STATE_VALUE:
                tag_states[tag] = override_tag_states[tag] == ON_STATE_VALUE
            else:
                tag_states[tag] = tag in old_tags

        result: List[str] = []

        for tag in all_tags:
            if tag_states[tag]:
                result.append(tag)

        return result
