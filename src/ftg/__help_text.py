from typing import Dict, List

from ftg.__cli_wrapper import __paths


def __to_link__(header: str):
    result = header.lower()
    result = result.strip(" ?!.")
    result.replace(" ", "-")
    return "#" + result


about_header = "About"
about_link = __to_link__(about_header)

where_to_start_header = "Where to Start"
where_to_start_link = __to_link__(where_to_start_header)

limitations_header = "Limitations"
limitations_link = __to_link__(limitations_header)

why_filenames_header = "Why Filenames?"
why_filenames_link = __to_link__(why_filenames_header)

alternatives_header = 'Alternatives'
alternatives_link = __to_link__(alternatives_header)

where_is_my_stuff_header = 'Where is my Stuff?'
where_is_my_stuff_link = __to_link__(where_is_my_stuff_header)

install_header = "Install"
install_link = __to_link__(install_header)

usage_header = "Usage"
usage_link = __to_link__(usage_header)

about_text = str(
    F'# {about_header}\n'
    '\n'
    'The primary purpose of this program is to tag files by appending the tags to the name of the file.\n'
    '\n'
    'The use case it is designed for is the organization of RPG maps and other media files a DM/GM comes in contact with.\n'
    '\n'
    '## Example\n'
    '\n'
    'To add the tags \n'
    '\n'
    '`tag1`, `tag2` and `tag3`\n'
    '\n'
    'to the file `some_map.png` it would be renamed to\n'
    '\n'
    '`some_map;tag1_tag2_tag3.png`')

configuration = str()

where_to_start_text = str(
    F'# {where_to_start_header}\n'
    '\n'
    F'If you are a new user who is planning to use this program read about its [limitations]({limitations_link}) first.\n'
    '\n'
    F'Then go to [{install_header}]({install_link})\n'
    '\n'
    F'Then go to [{usage_header}]({usage_link})\n'
    '\n'
    F'If you want to understand the decisions that lead to this mess go to [{why_filenames_header}]({why_filenames_link})\n'
    '\n'
    F'If you think that putting the tags into the filenames is a bad solution go to [{alternatives_header}]({alternatives_link})'
)

limitations_text = str(
    F'# {limitations_header}\n'
    '\n'
    'Putting the tags into the filenames is limited by the maximum path length and maximum file length.\n'
    'Windows, Linux, GoogleDrive, OneDrive, Dropbox, etc. all have different restraints\n'
    'on those.\n'
    '\n'
    '- Linux has a maximum filename length of 255 characters for most filesystems (including EXT4), and a maximum path of\n'
    '  4096\n'
    '  characters. [link](https://unix.stackexchange.com/questions/32795/what-is-the-maximum-allowed-filename-and-folder-size-with-ecryptfs)\n'
    '- Without Long Paths enabled Windows 10 has a maximum path length of\n'
    '  260 [link](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry)\n'
    '- With Long Paths enabled Windows 10 has a maximum path length of\n'
    '  32,767 [link](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry#:~:text=path%20length%20of-,32%2C767%20characters,-.%20This%20type%20of)\n'
    '\n'
    'If you intend to use this tool you should check what the systems you are planning to use\n'
    'are supporting. Maybe even run some tests.\n'
    '\n'
    'Make yourself clear about these limitations before using this tool as they cannot be circumvented.\n'
    '\n'
    'That said in most cases it´s pretty easy to stay below the limits unless you use very high number of long tags.'
)

why_filenames_text = str(
    F'# {why_filenames_header}\n'
    '\n'
    'This is the conclusion of a [reddit post](TODO)\n'
    '\n'
    '# Summary\n'
    '\n'
    '- Filenames are a good enough solution in the majority of cases.\n'
    '- Every good enough solution is better than a perfect solution that is never finished. (It has already taken me too long to implement this)\n'
    '- Every alternative to filenames I found so far either had other limitations or would require 100s of hours of work\n'
    '  to produce a satisfying program.\n'
    '- I don\'t get paid so can\'t spend 100s of hours implementing niche tools that only a handful of people will use.\n'
    '\n'
    '## Why Filenames are Good\n'
    '\n'
    '- Very verbose, can see tags with every file browser\n'
    '- Re-using what already exists\n'
    '    - File browser\n'
    '    - Thumbnail cache\n'
    '    - Search and indexing functionality\n'
    '    - Image viewers\n'
    '- Works in pretty much every cloud web interface\n'
    '    - => Access your media files via tags everywhere without having to download them first\n'
    '- Works with every type of file\n'
    '- Tags don\'t get lost on conversion\n'
    '- Tags don\'t get lost when file is moved\n'
    '- Tags always stay synced with file even when working on multiple machines \n'
    '  - => No need to sync databases, metafiles etc.\n'
    '\n'
    '## Problems with Alternative Solutions\n'
    '\n'
    '### Database\n'
    '\n'
    '- What happens when files are moved outside the tool?\n'
    '- Would require indexing\n'
    '- Needs a thumbnail cache and a file browser with search functionality\n'
    '- How to sync the database to different PC?\n'
    '- Can\'t use tags in the cloud web interface\n'
    '- Would basically just re-implement one of the countless tagging solutions that already exist\n'
    '\n'
    '### Accompanying Metafiles\n'
    '\n'
    '- Files always have to be moved together\n'
    '- Would require indexing\n'
    '- Needs a thumbnail cache and a file browser with search functionality\n'
    '- Can\'t use tags in the cloud web interface\n'
    '\n'
    '### Metadata of the Files\n'
    '\n'
    '- Not supported for a lot of file types\n'
    '- Would need to treat every file type special\n'
    '- Would require indexing\n'
    '- Needs a thumbnail cache and a file browser with search functionality\n'
    '- Can\'t use tags in the cloud web interface'
)

alternatives_text = str(
    F'# {alternatives_header}\n'
    '\n'
    'Originally I was going to put a list of alternatives here, but then I found many and none really satisfied me. '
    'That\'s why I created this tool in the first place.\n'
    '\n'
    'There is an abundance of tagging tools out there. If you find one that is \n'
    '\n'
    '- free\n'
    '- cross-platform\n'
    '- works with cloud sync\n'
    '- works in the cloud web interface\n'
    '- can easily manage 100s of tags\n'
    '- can easily manage dozens of tags per file\n'
    '\n'
    'let me know, so I can link it here.'
)

where_is_my_stuff_text = str(
    F'# {where_is_my_stuff_header}\n'
    F'\n'
    F'1. Local config dir : [{__paths.local_config_dir()}](file://{__paths.local_config_dir()})\n'
    F'2. User config dir : [{__paths.user_config_dir()}](file://{__paths.user_config_dir()})\n'
    F'3. System config dir : [{__paths.system_config_dir()}](file://{__paths.system_config_dir()})\n'
)

install_text = str(
    F'# {install_header}\n'
    F'TODO'
)

usage_text = str(
    F'# {usage_header}\n'
    F'TODO'
)


class Section:
    def __init__(self,
                 link,
                 header,
                 text):
        self.link = link
        self.header = header
        self.text = text


sections = [Section(about_link,
                    about_header,
                    about_text),
            Section(where_to_start_link,
                    where_to_start_header,
                    where_to_start_text),
            Section(limitations_link,
                    limitations_header,
                    limitations_text),
            Section(why_filenames_link,
                    why_filenames_header,
                    why_filenames_text),
            Section(alternatives_link,
                    alternatives_header,
                    alternatives_text),
            Section(where_is_my_stuff_link,
                    where_is_my_stuff_header,
                    where_is_my_stuff_text),
            Section(install_link,
                    install_header,
                    install_text),
            Section(usage_link,
                    usage_header,
                    usage_text)]

sections_by_link: Dict[str, Section] = {section.link: section for section in sections}


def __build_readme_table_of_contents__() -> str:
    sections_copy = sections.copy()

    sections_copy.remove(sections_by_link[where_is_my_stuff_link])

    return __build_table_of_contents__(sections_copy)


def __build_table_of_contents__(sections_for_table: List[Section]) -> str:
    i = 1

    entries = []

    for section in sections_for_table:
        entries.append(F'{i}. [{section.header}]({section.link})')

    return "\n".join(entries)


readme_table_of_contents = __build_readme_table_of_contents__()

help_table_of_contents = __build_table_of_contents__(sections)

help_text = '\n\n'.join([about_text,
                         where_to_start_text,
                         limitations_text,
                         why_filenames_text,
                         alternatives_text])
