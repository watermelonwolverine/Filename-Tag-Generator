import json
from typing import Dict, List

import ftg
from ftg.__cli_wrapper import __paths, __args
from ftg.__constants import default_tags_file_name, default_config_file_name, author, app_name, illegal_chars
from ftg.utils.name_generator import NameGeneratorImpl
from ftg.utils.naming_config import NamingConfigImpl
from ftg.utils.program_config import ProgramConfigImpl
from ftg.utils.tags import Tags


def __to_link__(header: str):
    result = header.lower()
    result = result.strip(" ?!.")
    result.replace(" ", "-")
    return "#" + result


def __to_code_block(code: str) -> str:
    indent = "    "

    result = ""

    for line in code.splitlines():
        result += indent + line + "\n"

    return result


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

config_header = "Config"
config_link = __to_link__(config_header)

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

__example_config = {
    ProgramConfigImpl.NAMING_CONFIG_KEY: {
        NamingConfigImpl.TAG_SEPARATOR_KEY: " ",
        NamingConfigImpl.BASENAME_TAGS_SEPARATOR_KEY: "-",
        NamingConfigImpl.ADJUST_BASENAME_KEY: False
    }
}

name_generator_default = NameGeneratorImpl(NamingConfigImpl())

name_generator_example = NameGeneratorImpl(
    NamingConfigImpl.parse_dict(__example_config[ProgramConfigImpl.NAMING_CONFIG_KEY]))

example_tags = ["tag1", "tag2", "tag3"]

example_basename = "This is some_base-name"

config_text = str(
    F'# {config_header}\n'
    F'\n'
    F'Two files are used to configure the program\n'
    F'\n'
    F'- Tag files, usually named `{default_tags_file_name}`\n'
    F'- Config files, usually named `{default_config_file_name}`\n'
    F'\n'
    F'Both are JSON files and need to be edited manually (as I cannot be bothered to spend countless hours on an editor)\n'
    F'\n'
    F'The program looks for configuration files in the following order:\n'
    F'\n'
    F'1. In the execution directory. I.e. where the executable is located.\n'
    F'2. In the user config directory.\n'
    F'    1. On Windows that\'s usually `C:\\users\\<user>\\AppData\\Local\\{author}\\{app_name}`\n'
    F'    2. On Linux that\'s usually "/home/<user>/TODO"\n'
    F'3. In the system config directory.\n'
    F'    1. On Windows that\'s usually `C:\\ProgramData\\{author}\\{app_name}`\n'
    F'    2. On Linux that\'s usually "/home/<user>/TODO"\n'
    F'\n'
    F'You can also specify the path to each file when starting from the command line using the `{__args.config_option}` and `{__args.tags_option}`\n'
    F'options. '
    F'This way you can have multiple tags and config files for different purposes.\n'
    F'\n'
    F'The program can run without a config file but it needs a tag file.\n'
    F'\n'
    F'## Tags\n'
    F'\n'
    F'The tags usually live in a `{default_tags_file_name}` file that follows the following structure:\n'
    F'\n'
    F'    {{\n'
    F'      "{Tags.FTG_VERSION_KEY}": "{ftg.__version__}",\n\n'
    F'      "{Tags.CATEGORIES_KEY}": {{\n'
    F'        "category-name1": {{\n'
    F'          "tag1": "tag1-display-name",\n'
    F'          "tag2": "tag2-display-name"\n'
    F'        }},\n'
    F'        "category-name2": {{\n'
    F'          "tag1": "tag1-display-name",\n'
    F'          "tag3": "tag3-display-name"\n'
    F'        }}\n'
    F'      }}\n'
    F'    }}\n'
    F'\n'
    F'You can have as many categories under `{Tags.CATEGORIES_KEY}` as you want. You can also have as many tags under each category as '
    F'you want.\n'
    F'\n'
    F'One tag can be in multiple categories as long as it has the the same display-name everywhere.\n'
    F'\n'
    F'For example: `"dungeon" : "Dungeon"` may fit into both categories `Nature` and `Civilization`.\n'
    F'\n'
    F'## UI and Behaviour\n'
    F'\n'
    F'You can configure the UI and the naming behaviour using a config file which is usually named `{default_config_file_name}`.\n'
    F'\n'
    F'The config file with the default values would look like this:\n'
    F'\n'
    F'{__to_code_block(json.dumps(ProgramConfigImpl.default_config_dict, indent=2))}\n'
    F'\n'
    F'I will not explain every single detail as most should be self-explanatory.\n'
    F'\n'
    F'The most important ones are:\n'
    F'\n'
    F'- `{NamingConfigImpl.BASENAME_TAGS_SEPARATOR_KEY}` : the string that will be used to separate the basename from the tags. Make sure this is unique and doesn\'t appear in any tag or in the basename.\n'
    F'- `{NamingConfigImpl.TAG_SEPARATOR_KEY}` : the string that will be used to separate the tags. Make sure this is unique and doesn\'t appear in any tag or in the basename.\n'
    F'- `{NamingConfigImpl.ADJUST_BASENAME_KEY}` : if this is set to `true` the program will adjust the basename\n'
    F'- `{NamingConfigImpl.CAPITALIZE_BASENAME_KEY}` : if this is set to `true` the basename will be capitalized when adjusted.\n'
    F'- `{NamingConfigImpl.REPLACE_BASENAME_SPACER_KEY}` : if this is set to `true` all spacers (whitespaces, {NamingConfigImpl.TAG_SEPARATOR_KEY} and {NamingConfigImpl.BASENAME_TAGS_SEPARATOR_KEY})  in the basename will be replaced by the given text\n'
    F'\n'
    F'## Example'
    F'\n'
    F'For the basename `{example_basename}` and the tags ´{", ".join(example_tags)}´ the default config would generate:\n'
    F'\n'
    F'`{name_generator_default.generate_filename(example_basename, example_tags, "png")}`\n'
    F'\n'
    F'With:\n'
    F'\n'
    F'{__to_code_block(json.dumps(__example_config, indent=2))}\n'
    F'\n'
    F'It would generate:\n'
    F'\n'
    F'`{name_generator_example.generate_filename(example_basename, example_tags, "png")}`\n'
    F'\n'
    F'As you can probably guess the last one is impossible to revert back into basename and tags. How is the program '
    F'supposed to know where the basename ends and the list of tags begins? Therefore you should be careful how separators and spacers you choose.\n'
    F'\n'
    F'Some filesystems forbid the usage of certain symbols. In other cases characters should be avoided for simplicity\'s sake. You must avoid:\n'
    F'\n'
    F'`{", ".join(illegal_chars)}`\n'
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
            Section(where_is_my_stuff_link,
                    where_is_my_stuff_header,
                    where_is_my_stuff_text),
            Section(install_link,
                    install_header,
                    install_text),
            Section(usage_link,
                    usage_header,
                    usage_text),
            Section(config_link,
                    config_header,
                    config_text),
            Section(why_filenames_link,
                    why_filenames_header,
                    why_filenames_text),
            Section(alternatives_link,
                    alternatives_header,
                    alternatives_text)]

sections_by_link: Dict[str, Section] = {section.link: section for section in sections}


def __get_readme_sections__() -> List[Section]:
    sections_copy = sections.copy()

    sections_copy.remove(sections_by_link[where_is_my_stuff_link])

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
