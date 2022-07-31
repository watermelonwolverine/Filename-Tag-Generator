import json
import os
import sys
from tkinter import messagebox

from ftg.__cli_wrapper.__args import tags_option
from ftg.__cli_wrapper.__constants import win32
from ftg.__cli_wrapper.__paths import user_path_to_tags, system_path_to_tags, \
    local_path_to_tags, local_path_to_config, system_path_to_config, user_path_to_config
from ftg.__constants import UTF_8, app_name, url
from ftg.utils.program_config import ProgramConfigImpl
from ftg.utils.tags import example_tags_dict


def maybe_setup():
    exe = ".exe" if sys.platform == win32 else ""

    msg = str(F"No tags file was found.\n"
              "\n"
              "Do you want to perform first time setup?\n"
              "\n"
              F"TIP: You can also specify a tags file from command line using the {tags_option} option.\n"
              "\n"
              "Example:\n"
              F"{app_name}{exe} {tags_option} <path-to-tags-file>\n"
              F"\n"
              F"On the projects website you can find tags files to start with:\n"
              F"\n"
              F"{url}")

    answer = messagebox.askyesno(title="Setup",
                                 message=msg)

    if answer:
        setup()


def setup():
    answer = messagebox.askyesno(title="Setup",
                                 message="Do you want to create a example tags file?")

    if answer:
        create_tags_file()

    answer = messagebox.askyesno(title="Setup",
                                 message="Do you want to create a config file with the default settings?")

    if answer:
        create_config_file()


def create_tags_file():
    contents = json.dumps(example_tags_dict,
                          indent=4)

    create_file("tags",
                local_path_to_tags(),
                user_path_to_tags(),
                system_path_to_tags(),
                contents)


def create_config_file():
    contents = json.dumps(ProgramConfigImpl.default_config_dict,
                          indent=4)

    create_file("config",
                local_path_to_config(),
                user_path_to_config(),
                system_path_to_config(),
                contents)


def create_file(name,
                local_path,
                user_path,
                system_path,
                default_content):
    path_to_file = None

    answer = messagebox.askyesno("Setup",
                                 F"Do you want create a local {name} file?\n"
                                 "\n"
                                 "It will be in the same location as the executable.\n"
                                 "\n"
                                 F"{local_path}\n"
                                 "\n"
                                 "Option 1/3")

    if answer:
        path_to_file = local_path

    if path_to_file is None:
        answer = messagebox.askyesno("Setup",
                                     F"Do you want create a {name} file in the active user's config directory?\n"
                                     "\n"
                                     F"{user_path}\n"
                                     "\n"
                                     "Option 2/3")
        if answer:
            path_to_file = user_path

    if path_to_file is None:
        answer = messagebox.askyesno("Setup",
                                     F"Do you want create a {name} file in the system config directory?\n"
                                     "\n" +
                                     F"{system_path}\n"
                                     "\n"
                                     "Option 3/3")
        if answer:
            path_to_file = system_path

    if path_to_file is None:
        messagebox.showerror("Setup Aborted",
                             "No option selected. Setup aborted")

    directory, filename = os.path.split(path_to_file)

    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(path_to_file):
        messagebox.showerror(title="Error",
                             message="File already exists:\n"
                                     "\n"
                                     F"{path_to_file}")
        return

    with open(path_to_file, "wt", encoding=UTF_8) as fh:
        fh.write(default_content)

    answer = messagebox.askyesno(title="New File Created",
                                 message=F"A new {name} file was created in at\n"
                                         F"\n"
                                         F" {path_to_file}\n"
                                         F"\n"
                                         F"Do you want open the folder?")
    if answer:
        os.startfile(directory)
