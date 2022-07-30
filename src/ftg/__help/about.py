from ftg.__help.utils import to_link, Section

header = "About"
link = to_link(header)

text = str(
    F'# {header}\n'
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

section = Section(link,
                  header,
                  text)
