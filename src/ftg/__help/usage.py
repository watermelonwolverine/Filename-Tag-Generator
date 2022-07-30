from ftg.__help.utils import __to_link__, Section

header = "Usage"
link = __to_link__(header)

text = str(
    F'# {header}\n'
    F'\n'
    F'The \n'
)

section = Section(link,
                  header,
                  text)
