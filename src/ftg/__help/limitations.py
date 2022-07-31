from ftg.__help.utils import to_link, Section

header = "Limitations"
link = to_link(header)

text = str(
    F'# {header}\n'
    '\n'
    'Putting the tags into the filenames is limited by the maximum path length and the maximum filename length of the system(s) you\'re using.\n'
    'Windows, Linux, GoogleDrive, OneDrive, Dropbox, etc. all have different restraints\n'
    'on those.\n'
    '\n'
    '- Linux has a maximum filename length of 255 characters for most filesystems (including EXT4), and a maximum path of\n'
    '  4096\n'
    '  characters. [link](https://unix.stackexchange.com/questions/32795/what-is-the-maximum-allowed-filename-and-folder-size-with-ecryptfs)\n'
    '- Without Long Paths enabled Windows 10 has a maximum path length of\n'
    '  260 characters. [link](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry)\n'
    '- With Long Paths enabled Windows 10 has a maximum path length of\n'
    '  32,767 characters. [link](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry#:~:text=path%20length%20of-,32%2C767%20characters,-.%20This%20type%20of)\n'
    '\n'
    'If you intend to use this tool you should check what the systems you are planning to use\n'
    'are supporting. Maybe even run some tests. If you plan to use this program on Windows you will have to enable Long Paths, almost certainly.\n'
    '\n'
    'Make yourself clear about these limitations before using this program as they cannot be circumvented.\n'
    '\n'
    'That said in most cases it´s pretty easy to stay below the limits unless you use a very high number of long tags.'
)

section = Section(link,
                  header,
                  text)
