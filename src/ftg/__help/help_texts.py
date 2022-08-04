from typing import Dict, List

from ftg.__help import install, why_filenames, configuration, about, where_to_start, limitations, alternatives, \
    where_is_my_stuff, usage, searching, command_line_usage, known_issues, troubleshooting, build
from ftg.__help.utils import to_link, Section

usage_placeholder = Section("", "", "")

__sections = [about.section,
              where_to_start.section,
              limitations.section,
              usage_placeholder,
              command_line_usage.section,
              searching.section,
              install.section,
              configuration.section,
              where_is_my_stuff.section,
              known_issues.section,
              troubleshooting.section,
              build.section,
              why_filenames.section,
              alternatives.section]

__usage_index = __sections.index(usage_placeholder)


def __get_readme_sections__() -> List[Section]:
    result = __sections.copy()

    result.remove(usage_placeholder)

    result.insert(__usage_index,
                  usage.get_section(True))

    result.remove(where_is_my_stuff.section)

    toc = __build_table_of_contents__(result)

    result.insert(0, toc)

    return result


def __build_table_of_contents__(sections_for_table: List[Section]) -> Section:
    i = 1

    entries = []

    for section in sections_for_table:
        entries.append(F'{i}. [{section.header}]({section.link})')

    text = "\n".join(entries)

    header = 'Table of Contents'

    text = str(
        F"# {header}\n"
        F'\n'
        F'{text}')

    return Section(to_link(header),
                   header,
                   text)


def __build_help_sections():
    result = __sections.copy()

    result.remove(usage_placeholder)

    result.insert(__usage_index,
                  usage.get_section(False))

    return result


readme_sections = __get_readme_sections__()

readme_text = '\n\n'.join([section.text for section in readme_sections])

help_sections = __build_help_sections()

help_sections_by_link: Dict[str, Section] = {section.link: section for section in help_sections}

help_table_of_contents = __build_table_of_contents__(help_sections)
