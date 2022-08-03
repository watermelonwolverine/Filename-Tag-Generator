from ftg.__help.utils import to_link, Section

header = 'Known Issues'
link = to_link(header)

text = str(
    F'# {header}\n'
    '\n'
    'Filesystems are quirky, and therefore so is this program.\n'
    '\n'
    '## Windows\n'
    '\n'
    '### Arbitrary "OSError [Errno 13] Permission Denied"\n'
    '\n'
    'This one is weird and I have spent many hours trying to fix it.\n'
    'It seems that Python sometimes can\'t handle `&` in paths.\n'
    'Even weirder, this problem only occurs sometimes and only with prebuilt binaries, not when installed with pip.\n'
    'Therefore, I assume that this is an issue with PyInstaller.\n'
    'This can usually be circumvented by moving the affected files into a different folder, temporarily. One without `&` in its path.'
)

section = Section(link,
                  header,
                  text)
