from ftg.__help.utils import to_link, Section

header = "Searching"
link = to_link(header)
text = str(
    F'# {header}\n'
    F'\n'
    F'This program does not have any search functionality. Instead, you use whatever file browser your system has which '
    F'usually has all the features you need. Windows, Ubuntu, GDrive, Dropbox, etc. all provide thumbnail views and indexed search.\n'
    F'\n'
    F'## Examples\n'
    F'\n'
    F'On Windows the [syntax](https://docs.microsoft.com/en-us/windows/win32/lwef/-search-2x-wds-aqsreference) is very easy. The query\n'
    F'\n'
    F'`"tag1" ("tag2" OR "tag3") NOT kind:folder`\n'
    F'\n'
    F'would give you all files with the tag `tag1` that also have `tag2` or `tag3`\n'
    F'\n'
    F'The Google Drive search syntax is different, and I couldn\'t find any good references. With a bit of trial and error I found that:\n'
    F'\n'
    F'`"tag1"("tag2"|"tag3")-type:folder`\n'
    F'\n'
    F'would be equal to the above. It\'s important to not use whitespaces. `|` operates as (logical) or. `-` excludes stuff.\n'
)

section = Section(link,
                  header,
                  text)
