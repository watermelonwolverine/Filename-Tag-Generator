import json

import ftg
from ftg.__cli_wrapper import __args
from ftg.__constants import default_tags_file_name, default_config_file_name, author, app_name, illegal_chars
from ftg.__help import command_line_usage
from ftg.__help.utils import to_link, to_code_block, Section
from ftg.utils.name_generator import NameGeneratorImpl
from ftg.utils.naming_config import NamingConfigImpl
from ftg.utils.program_config import ProgramConfigImpl
from ftg.utils.tags import Tags

header = "Configuration"
link = to_link(header)

__example_config = {
    ProgramConfigImpl.NAMING_CONFIG_KEY: {
        NamingConfigImpl.TAG_SEPARATOR_KEY: " ",
        NamingConfigImpl.BASENAME_TAGS_SEPARATOR_KEY: " ",
        NamingConfigImpl.ADJUST_BASENAME_KEY: False
    }
}

__name_generator_default = NameGeneratorImpl()

__name_generator_example = NameGeneratorImpl(
    NamingConfigImpl.parse_dict(__example_config[ProgramConfigImpl.NAMING_CONFIG_KEY]))

__example_tags = ["tag1", "tag2", "tag3"]

__example_basename = "This is some_base-name"

__characters_to_avoid = ["*", "<", ">", "|", "?", ":", '"']

text = str(
    F'# {header}\n'
    F'\n'
    F'Two files are used to configure the program\n'
    F'\n'
    F'- Tags files, named `{default_tags_file_name}`\n'
    F'- Config files, named `{default_config_file_name}`\n'
    F'\n'
    F'Both are JSON files and need to be edited manually (as I cannot be bothered to spend countless hours on an editor)\n'
    F'\n'
    F'The program looks for configuration files in the following order:\n'
    F'\n'
    F'1. In the execution directory. I.e. where the executable is located.\n'
    F'2. In the user config directory.\n'
    F'    1. On Windows that\'s usually `C:\\users\\<user>\\AppData\\Local\\{author}\\{app_name}`\n'
    F'    2. On Linux that\'s usually `/home/<user>/TODO`\n'
    F'3. In the system config directory.\n'
    F'    1. On Windows that\'s usually `C:\\ProgramData\\{author}\\{app_name}`\n'
    F'    2. On Linux that\'s usually `/home/<user>/TODO`\n'
    F'\n'
    F'You can also specify the path to each file when starting from the command line using the `{__args.config_option}` and `{__args.tags_option}`\n'
    F'options. '
    F'This way you can have multiple tags and config files for different purposes. See [{command_line_usage.header}]({command_line_usage.link})\n'
    F'\n'
    F'The program can run without a config file, but it needs a tags file.\n'
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
    F'One tag can be in multiple categories as long as it has the same display-name everywhere.\n'
    F'\n'
    F'For example: `"dungeon" : "Dungeon"` may fit into both categories `Nature` and `Civilization`.\n'
    F'\n'
    F'## UI and Behaviour\n'
    F'\n'
    F'You can configure the UI and the naming behaviour using a config file which is usually named `{default_config_file_name}`.\n'
    F'\n'
    F'The config file with the default values would look like this:\n'
    F'\n'
    F'{to_code_block(json.dumps(ProgramConfigImpl.default_config_dict, indent=2))}\n'
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
    F'For the basename `{__example_basename}` and the tags `{", ".join(__example_tags)}` the default config would generate:\n'
    F'\n'
    F'`{__name_generator_default.generate_filename(__example_basename, __example_tags, "png")}`\n'
    F'\n'
    F'With:\n'
    F'\n'
    F'{to_code_block(json.dumps(__example_config, indent=2))}\n'
    F'\n'
    F'It would generate:\n'
    F'\n'
    F'`{__name_generator_example.generate_filename(__example_basename, __example_tags, "png")}`\n'
    F'\n'
    F'As you can probably guess the last one is impossible to revert into basename and tags. How is the program '
    F'supposed to know where the basename ends and the list of tags begins? Therefore, you should be careful which separators and spacers you choose.\n'
    F'\n'
    F'Some filesystems forbid the usage of certain symbols. In other cases characters should be avoided for simplicity\'s sake. You must avoid:\n'
    F'\n'
    F'`{", ".join(illegal_chars)}`\n'
    F'\n'
    F'and you should avoid:\n'
    F'\n'
    F'`{", ".join(__characters_to_avoid)}`\n'
    F'\n'
    F'You should also avoid having the same text as `{NamingConfigImpl.BASENAME_SPACER_KEY}` and `{NamingConfigImpl.TAG_SEPARATOR_KEY}`.'
)

section = Section(link,
                  header,
                  text)
