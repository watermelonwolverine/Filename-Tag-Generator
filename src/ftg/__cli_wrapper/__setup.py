import os
import sys
from tkinter import messagebox

from ftg import __version__
from ftg.__cli_wrapper.__args import tags_option
from ftg.__cli_wrapper.__constants import win32
from ftg.__cli_wrapper.__paths import user_path_to_tags, user_config_dir, system_config_dir, system_path_to_tags, \
    local_path_to_tags
from ftg.__constants import UTF_8, app_name

example_tags = F"\
{{\n\
    \"ftg-version\" : \"{__version__}\",\n\
    \"categories\" : {{\n\
        \"category1\" : \n\
            {{\n\
                \"tag1\" : \"tag1-display-name\", \n\
                \"tag2\" : \"tag2-display-name\" \n\
            }},\n\
        \"category2\" : \n\
        {{\n\
            \"tag1\" : \"tag1-display-name\", \n\
            \"tag3\" : \"tag3-display-name\" \n\
        }}\n\
    }}\n\
}}"


def setup(tk):
    exe = ".exe" if sys.platform == win32 else ""

    msg = str(F"No tags file was found.\n"
              "\n"
              "Do you want to create a new tags file?\n"
              "\n"
              F"TIP: You can also specify a tags file from command line using the {tags_option} option.\n" + \
              "\n"
              "Example:\n"
              F"{app_name}{exe} {tags_option} <path-to-tags-file>")

    answer = messagebox.askyesno(title="Setup",
                                 message=msg)

    if answer:
        create_tags_file()


def create_tags_file():
    create_file("tags",
                local_path_to_tags(),
                user_path_to_tags(),
                system_path_to_tags(),
                example_tags)


def create_file(name,
                local_path,
                user_path,
                system_path,
                default_content):
    path_to_file = None

    answer = messagebox.askyesno("Setup",
                                 F"Do you want create a local {name} file?\n"
                                 "\n"
                                 "It will be in the same location as the executable.")

    if answer:
        path_to_file = local_path

    if path_to_file is None:
        answer = messagebox.askyesno("Setup",
                                     F"Do you want create a {name} file in the active user's config directory?\n"
                                     "\n" +
                                     user_config_dir())
        if answer:
            path_to_file = user_path

    if path_to_file is None:
        answer = messagebox.askyesno("Setup",
                                     F"Do you want create a {name} file in the system config directory?\n"
                                     "\n" +
                                     system_config_dir())
        if answer:
            path_to_file = system_path

    if path_to_file is None:
        messagebox.showerror("Setup Aborted",
                             "No option selected. Setup aborted")

    directory, filename = os.path.split(path_to_file)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path_to_file, "wt", encoding=UTF_8) as fh:
        fh.write(default_content)

    answer = messagebox.askyesno(title="New File Created",
                                 message=F"A new {name} file was created in at {path_to_file}\n"
                                         F"Do you want open the folder?")
    if answer:
        os.startfile(directory)
