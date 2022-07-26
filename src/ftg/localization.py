import sys

from ftg.__cli_wrapper.__args import tags_option
from ftg.__cli_wrapper.__constants import win32
from ftg.__constants import app_name

UNEXPECTED_ERROR_TITLE = "An Unexpected Error Occurred"
UNEXPECTED_ERROR_MSG = "\
IMPORTANT - DO NOT IGNORE\n\
\n\
An unexpected error occurred.\n\
\n\
A crash report was created at {0}.\n\
\n\
Please submit a bug report at {1}.\n\
\n\
Please include the crashreport and a detailed description of the steps that lead to the error."



WRONG_TAGS_FILE_STRUCTURE = "Structure of tags file is wrong."

PLEASE_CHECK_YOUR_FILES_TITLE = "Incorrect json files"

PLEASE_CHECK_YOUR_FILES_MSG = "\
While reading:\n\
\n\
{0}\n\
\n\
the following exception occurred:\n\
\n\
{1}\n\
\n\
Please check the correctness of this file."

FILE_NOT_FOUND = "File not found: {0}"
