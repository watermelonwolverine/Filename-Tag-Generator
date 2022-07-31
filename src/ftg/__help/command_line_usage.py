from ftg.__cli_wrapper import __args
from ftg.__constants import app_name
from ftg.__help.utils import to_link, Section, to_code_block

header = "Command Line Options"
link = to_link(header)

num_spaces = 20


def __with_spaces(text_: str) -> str:
    remaining_spaces = num_spaces - len(text_)
    return "  " + text_ + remaining_spaces * " "


def __make_markdown(text_: str) -> str:
    result = text_.replace("\n", "\n\n")
    return result


usage = str(
    F'{app_name} '
    F'[{__args.tags_option} path-to-tags-file] '
    F'[{__args.config_option} path-to-config-file] '
    F'[{__args.verbosity_option} {{{"|".join(__args.verbosity_choices)}}}] '
    F'[{__args.setup_option}] '
    F'[{__args.version_option}]\n'
    F'\n'
    F'{__with_spaces(__args.tags_option)} specify a tags file\n'
    F'{__with_spaces(__args.config_option)} specify a config file\n'
    F'{__with_spaces(__args.verbosity_option)} set the verbosity of the console logger\n'
    F'{__with_spaces(__args.setup_option)} run interactive setup\n'
    F'{__with_spaces(__args.version_option)} print version and exit\n'
)

text = str(
    F'# {header}\n'
    F'\n'
    F'For those who want a bit more control over the program I added some command line options.\n'
    F'\n'
    F'{to_code_block(usage)}'
)

section = Section(link,
                  header,
                  text)
