from ftg.__cli_wrapper import __paths
from ftg.__cli_wrapper.__args import setup_option
from ftg.__help import install, configuration
from ftg.__help.utils import to_link, Section

header = 'Where is my Stuff?'
link = to_link(header)

text = str(
    F'# {header}\n'
    F'\n'
    F'The program looks for tags files and config files in the order below. Configuration files in folders higher up in the '
    F'list override files in folders which are lower in the list. For more information see [configuration]({configuration.link}).\n'
    F'\n'
    F'Click on the a link below to the open folder if it exists. If the folder does not exist you have to create '
    F'it manually or run the application from command line with the `{setup_option}` flag. For more information see [install]({install.link}).\n'
    F'\n'
    F'1. Local config dir : [{__paths.local_config_dir()}](file://{__paths.local_config_dir()})\n'
    F'2. User config dir : [{__paths.user_config_dir()}](file://{__paths.user_config_dir()})\n'
    F'3. System config dir : [{__paths.system_config_dir()}](file://{__paths.system_config_dir()})\n'
)

section = Section(link,
                  header,
                  text)
