from ftg.__help.utils import to_link, Section

header = 'Build'
link = to_link(header)

text = str(
    F'# {header}\n'
    F'\n'
    F'This section assumes you have extensive programming and Python experience as I will not explain every single detail.\n'
    F'If you want to build the program yourself, these are the steps:\n'
    F'\n'
    F'1. Clone repository\n'
    F'2. Install requirements (see requirements.txt)\n'
    F'3. On Windows ..\n'
    F'    1. .. EITHER download [UPX](https://upx.github.io/) and extract it into a folder called `upx` next to the project directory.\n'
    F'    2. .. OR remove the `--upx-dir ..\\upx` part from any build_for_windows_*_console.ps1 script\n'
    F'4. Build\n'
    F'    1. On Windows run one of the build_for_windows_*_console.ps1 files\n'
    F'    2. On Ubuntu run one of the build_for_ubuntu_*_console.sh files'
)

section = Section(link,
                  header,
                  text)
