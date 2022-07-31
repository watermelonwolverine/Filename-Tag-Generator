from ftg.__help.utils import to_link, Section
from ftg.utils.name_generator import NameGeneratorImpl

header = "About"
link = to_link(header)

__nameGenerator = NameGeneratorImpl()

__example_filename = __nameGenerator.generate_filename("some_map",
                                                       ["tag1", "tag2", "tag3"],
                                                       "png")

text = str(
    F'# {header}\n'
    '\n'
    'The primary purpose of this program is to tag files by appending the tags to the name of the file.\n'
    '\n'
    'It\'s designed use case is the organization of RPG maps and other media files a DM/GM comes in contact with.\n'
    '\n'
    '## Example\n'
    '\n'
    'You have a file named `some_map.png`\n'
    '\n'
    'You want to add the tags `tag1`, `tag2` and `tag3` to this file.\n'
    '\n'
    'You drag and drop the file into the program, select the tags and the program automatically renames the file to\n'
    '\n'
    F'`{__example_filename}`')

section = Section(link,
                  header,
                  text)
