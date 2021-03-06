from typing import List, Dict

from ftg.__constants import ON_STATE_VALUE, OFF_STATE_VALUE, MIXED_STATE_VALUE


def get_check_button_tri_states(all_tags: List[str],
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


def override_tags(old_tags: List[str],
                  override_tag_states: Dict[str, int]) -> List[str]:
    tag_states: Dict[str, bool] = {}

    for tag in override_tag_states.keys():
        if override_tag_states[tag] == ON_STATE_VALUE \
                or override_tag_states[tag] == OFF_STATE_VALUE:
            tag_states[tag] = override_tag_states[tag] == ON_STATE_VALUE
        else:
            tag_states[tag] = tag in old_tags

    result: List[str] = []

    for tag in override_tag_states.keys():
        if tag_states[tag]:
            result.append(tag)

    return result


def get_sorted_tags(categories_dict: Dict) -> List[str]:
    result = []

    for tag_list in categories_dict.values():
        for tag in tag_list:
            if tag not in result:
                result.append(tag)
    return sorted(result)
