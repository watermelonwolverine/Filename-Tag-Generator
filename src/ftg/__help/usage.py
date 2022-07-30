from ftg.__help import configuration
from ftg.__help.utils import to_link, Section
from ftg.localization import SELECTED_FILE, BASENAME, EXTENSION, APPLY, FULL_NAME, REVERT

header = "Usage"
link = to_link(header)

text = str(
    F'# {header}\n'
    F'\n'
    F'The program can be used for two purposes:\n'
    F'\n'
    F'1. Directly rename files via drag and drop\n'
    F'2. Generate map names\n'
    F'\n'
    F'## Renaming Files\n'
    F'\n'
    F'### Single\n'
    F'\n'
    F'To rename a file drag and drop it from your file browser into the application window.\n'
    F'The program will then revert the filename back into basename, tags and extensions.\n'
    F'For this process to go smoothly make sure the filename doesn\'t contain special characters in its basename or tags.\n'
    F'See [{configuration.header}]({configuration.link}) for more information.\n'
    F'Any tags in the filename that are not in you tags file will get lost in this translation.\n'
    F'Once you dropped the file into the application you can change the basename and extension and select the tags you want to add.\n'
    F'\n'
    F'As soon as you click the `{APPLY}` button the file will be renamed in accordance to what you selected.\n'
    F'\n'
    F'### Multiple\n'
    F'\n'
    F'You can drag and drop multiple files into the application window.\n'
    F'In this case the program behaves very similar to single file drop with a few changes.\n'
    F'\n'
    F'- The tag buttons will be changed to checkboxes with one of three states `On` and `Off` and `Mixed`.\n'
    F'- The `{SELECTED_FILE}` field will be disabled. You will have to remember which files you dragged into the application.\n'
    F'- `{BASENAME}` and `{EXTENSION}` input fields will be disabled. You will have to adjust the basename and extension beforehand.\n'
    F'\n'
    F'Checkboxes states:\n'
    F'\n'
    F'- The `On` state indicates, that all files have this tag.\n'
    F'- The `Off` state indicates, that no file has this tags.\n'
    F'- The `Mixed` state indicates, that some, but not all, file have this tag.\n'
    F'\n'
    F'When you click on a checkbox with state `Mixed` it will change to `On`. After that you can only switch between `On` and `Off`.\n  '
    F'=> Don\'t touch a `Mixed` checkbox unless want to add or remove this tag to/from all files\n'
    F'\n'
    F'As soon as you click the `{APPLY}` button the files will be renamed in accordance to what you selected.\n'
    F'If you disabled a checkbox that was previously `Mixed` or `On` the tag will be removed from all files.\n'
    F'If you enabled a checkbox that was previously `Mixed` or `Off` the tag will be added to all files.\n'
    F'\n'
    F'## Generating Map Names\n'
    F'\n'
    F'This one is useful for organizing maps via names in your VTT.\n'
    F'\n'
    F'Simply enter a basename and click on the tags you want to select and copy the result from the `{FULL_NAME}` field.\n'
    F'\n'
    F'If you want to add or remove tags to a name paste it in `{FULL_NAME}` and click the `{REVERT}` button.'
)

section = Section(link,
                  header,
                  text)
