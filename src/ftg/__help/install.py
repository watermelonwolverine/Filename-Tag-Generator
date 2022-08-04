from ftg.__constants import url, app_name, author
from ftg.__help import configuration
from ftg.__help.utils import to_link, Section

header = "Install"
link = to_link(header)

text = str(
    F'# {header}\n'
    F'\n'
    F'## Windows\n'
    F'\n'
    F'You can install the program in two ways. You can either download one of the prebuilt exe files from [releases]({url + "/releases"}) '
    F'or you can install it using Python.\n'
    F'\n'
    F'### Using Prebuilt Binary\n'
    F'\n'
    F'1. Download exe file from one of the [releases]({url + "/releases"})\n'
    F'2. Put the binary in a folder of your choice. For example `C:\\Users\\<your-username>\\Programs\\{author}\\{app_name}`\n'
    F'3. Either run the  program for a first time setup or go directly to [configuration]({configuration.link}) to read about configuration files.\n'
    F'\n'
    F'### Using Python\n'
    F'\n'
    F'This section assumes that you have Python version >= 3.8 installed on your system and that you have some basic Python and command line knowledge.\n'
    F'Also, you must have installed Tkinter when you were installing Python.\n'
    F'If you have multiple versions on your system make sure you are using the right one using `python.exe --version`\n'
    F'\n'
    F'1. Install via pip\n'
    F'    1. Either from Python a wheel file from [releases]({url + "/releases"}) with `python.exe -m pip install <link-to-whl-file-under-releases>`\n'
    F'    2. Or install directly from the repo with `python.exe -m pip install git+{url}`\n'
    F'2. Find out where Python installs scripts. It should be in the `Scripts` folder under Python\'s `USER_BASE` folder which you can find out using `python.exe -m site`.\n'
    F'3. Either run the program for a first time setup or go directly to [configuration]({configuration.link}) to read about configuration files.\n'
    F'\n'
    F'## Ubuntu\n'
    F'\n'
    F'You can install the program in two ways. You can either download one of the prebuilt binaries files from [releases]({url + "/releases"}) '
    F'or you can install it using Python.\n'
    F'\n'
    F'### Using Prebuilt Binary\n'
    F'\n'
    F'1. Download binary from one of the [releases]({url + "/releases"})\n'
    F'2. Put the binary in a folder of your choice.\n'
    F'3. Either run the  program for a first time setup or go directly to [configuration]({configuration.link}) to read about configuration files.\n'
    F'\n'
    F'### Using Python\n'
    F'\n'
    F'This section assumes that you have Python version >= 3.8 installed on your system and that you have some basic Python and command line knowledge.\n'
    F'You must also install tkinter for your Python version. Under Ubuntu that can usually be done with `apt install pythonX-tk` with `X` being the Python version you use.\n'
    F'\n'
    F'1. Install via pip\n'
    F'    1. Either from a Python wheel file from [releases]({url + "/releases"}) with `pythonX -m pip install <link-to-whl-file-under-releases>`\n'
    F'    2. Or install directly from the repo with `pythonX -m pip install git+{url}`\n'
    F'2. You should now be able to run the program from command line with `{app_name}`.\n'
    F'3. Either run the  program for a first time setup or go directly to [configuration]({configuration.link}) to read about configuration files.')

section = Section(link,
                  header,
                  text)
