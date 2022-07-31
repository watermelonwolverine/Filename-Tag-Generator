from . import __version__

ON_STATE_VALUE = 1
OFF_STATE_VALUE = 0
MIXED_STATE_VALUE = -1

NORMAL = "normal"
READONLY = "readonly"

UTF_8 = "UTF-8"

app_name = "Filename-Tag-Generator"
author = "watermelonwolverine"
url = "https://github.com/%s/%s" % (author, app_name)
issues_url = "%s/issues" % url
window_title = F'{app_name} v.{__version__}'

crash_report_file_name = "crashreport.txt"
default_config_file_name = "config.json"
default_tags_file_name = "tags.json"

illegal_chars = ["/", "\\"]
