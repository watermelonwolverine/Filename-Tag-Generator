import os
import sys
from tkinter import Tk, messagebox

from ftg import __version__
from ftg.__cli_wrapper.__paths import user_path_to_tags
from ftg.__constants import UTF_8
from ftg.localization import SETUP_TITLE, SETUP_MSG

example_tags = F"\
{{\n\
    \"ftg-version\" : \"{__version__}\"\n\
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


def do_setup():
    path_to_tags = user_path_to_tags()

    directory, filename = os.path.split(path_to_tags)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path_to_tags, "wt", encoding=UTF_8) as fh:
        fh.write(example_tags)

    os.startfile(directory)


def setup():
    tk = Tk()

    answer = messagebox.askyesno(title=SETUP_TITLE,
                                 message=SETUP_MSG)

    if answer:
        do_setup()

    tk.destroy()
    sys.exit()
