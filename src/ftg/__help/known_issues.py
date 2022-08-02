from ftg.__help.utils import to_link, Section

header = 'Known Issues'
link = to_link(header)

text = str(
    F'# {header}\n'
    '\n'
    'Filesystems are quirky, and therefore so is this program.'
    'On Windows Python can\'t handle `&` in paths for some reason. Even weirder this problem only occurs with the prebuilt binaries, not when installed with pip. I assume this to be an issue with PyInstaller.'
)

section = Section(link,
                  header,
                  text)
