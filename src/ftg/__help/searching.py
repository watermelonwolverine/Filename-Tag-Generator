from ftg.__help.utils import to_link, Section

header = "searching"
link = to_link(header)
text = str(
    F'# {header}\n'
    F'\n'
    F''
)

section = Section(link,
                  header,
                  text)
