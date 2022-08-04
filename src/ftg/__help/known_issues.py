from ftg.__help import build, install
from ftg.__help.utils import to_link, Section

header = 'Known Issues'
link = to_link(header)

text = str(
    F'# {header}\n'
    F'\n'
    F'Filesystems are quirky, and therefore so is this program.\n'
    F'\n'
    F'## Windows\n'
    F'\n'
    F'### Arbitrary "OSError [Errno 13] Permission Denied"\n'
    F'\n'
    F'This one is weird and I have spent many hours trying to fix it.\n'
    F'It seems that Python sometimes can\'t handle `&` in paths.\n'
    F'Even weirder, this problem only occurs sometimes and only with prebuilt binaries, not when installed with pip.\n'
    F'I assume that this is either an issue with PyInstaller or with antivirus software thinking that the program is suspicious and denying it access to files.\n'
    F'This can usually be circumvented by moving the affected files into a different folder, temporarily. One without `&` in its path.\n'
    F'\n'
    F'### Anti-Virus Provider Flags Program As Virus"\n'
    F'\n'
    F'Binaries created with PyInstaller are known for being falsely flagged as malware by antivirus software. (Just google pyInstaller an VirusTotal)\n'
    F'This program is no exception and to this day I still haven\'t found a way to eliminate all positives on VirusTotal.\n'
    F'Still, you should not just simply disregard those warnings and use the tool anyway.\n'
    F'Don\'t believe a person on the internet who says their program is not a virus.\n'
    F'If you are suspicious you can install the program with Python Pip, see [{install.header}]({install.link}).\n'
    F'Or you can build the program yourself, see [{build.header}]({build.link})'
)

section = Section(link,
                  header,
                  text)
