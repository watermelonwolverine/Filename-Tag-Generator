from ftg import __constants
from ftg.__help import known_issues
from ftg.__help.utils import to_link, Section

header = 'Troubleshooting'
link = to_link(header)

text = str(
    F'# {header}\n'
    F'\n'
    F'1. Have a look at [{known_issues.header}]({known_issues.link}) and see if you can find your issue there.\n'
    F'2. Check [here]({__constants.url + "/releases"}) if you have the newest version.\n'
    F'3. Go to [issues]({__constants.issues_url}) page on [GitHub]({__constants.url}) and see if somebody else had the same problem.\n'
    F'4. If nothing helped, create a new issue on [GitHub]({__constants.issues_url}).'
)

section = Section(link,
                  header,
                  text)
