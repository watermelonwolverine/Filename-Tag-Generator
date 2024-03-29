from ftg.__help import why_filenames, limitations, alternatives, usage
from ftg.__help.utils import Section

from ftg.__help.utils import to_link

header = "Where to Start"
link = to_link(header)

text = str(
    F'# {header}\n'
    '\n'
    F'If you just want to see how to the program works go to [{usage.header}]({usage.link})\n'
    '\n'
    F'If you are a new user who is planning to use this program you should read about its [limitations]({limitations.link}) first.\n'
    '\n'
    F'If you want to understand the decisions that lead to this mess go to [{why_filenames.header}]({why_filenames.link})\n'
    '\n'
    F'If you think that putting the tags into the filenames is a bad solution go to [{alternatives.header}]({alternatives.link})'
)

section = Section(link,
                  header,
                  text)
