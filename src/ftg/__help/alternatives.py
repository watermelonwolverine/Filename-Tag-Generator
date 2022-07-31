from ftg.__help.utils import to_link, Section

header = 'Alternatives'
link = to_link(header)

text = str(
    F'# {header}\n'
    '\n'
    'Originally I was going to put a list of alternatives here, but then I found many and none really satisfied me. '
    'That\'s why I created this tool in the first place.\n'
    '\n'
    'There is an abundance of tagging tools out there. If you find one that is \n'
    '\n'
    '- free\n'
    '- cross-platform\n'
    '- works with cloud sync\n'
    '- works in the  web interface of any cloud\n'
    '- can manage 100s of tags\n'
    '- can manage dozens of tags per file\n'
    '\n'
    'let me know, so I can link it here.'
)

section = Section(link,
                  header,
                  text)
