from typing import Dict, List

from ftg.__help import install, why_filenames, configuration, about, where_to_start, limitations, alternatives, \
    where_is_my_stuff, usage
from ftg.__help.utils import __to_link__, Section

sections = [about.section,
            where_to_start.section,
            limitations.section,
            where_is_my_stuff.section,
            install.section,
            usage.section,
            configuration.section,
            why_filenames.section,
            alternatives.section]

sections_by_link: Dict[str, Section] = {section.link: section for section in sections}


def __get_readme_sections__() -> List[Section]:
    sections_copy = sections.copy()

    sections_copy.remove(sections_by_link[where_is_my_stuff.link])

    return sections_copy


def __build_readme_table_of_contents__() -> Section:
    return __build_table_of_contents__(__get_readme_sections__())


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

    return Section(__to_link__(header),
                   header,
                   text)


readme_sections_with_toc = [__build_readme_table_of_contents__()] + __get_readme_sections__()

readme_table_of_contents = __build_readme_table_of_contents__()

help_table_of_contents = __build_table_of_contents__(sections)

readme_text = '\n\n'.join([section.text for section in readme_sections_with_toc])
