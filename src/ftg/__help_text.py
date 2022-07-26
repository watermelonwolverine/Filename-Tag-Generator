help_text = \
    str('# About\n'
        '\n'
        'The primary purpose of this program is to tag files by adding the tags to the name of the file.\n'
        '\n'
        'The use case it is designed for is the organization of rpg map hoards and other media files a DM comes in contact with.\n'
        '\n'
        'Anyone who every comes into contact with this task will quickly find that no folder structure will every be the right one.\n'
        '\n'
        '## Example\n'
        '\n'
        'To add the tags `tag1`, `tag2` and `tag3` to the file `some_map.png` it would be renamed to `SOME-MAP;tag1_tag2_tag3.png\n'
        '`\n'
        '\n'
        '# Where to Start\n'
        '\n'
        'If you are a new user who is planning to use this program read about its [limitations](#Limitations) first.\n'
        '\n'
        'Then go to [Install](#Install)\n'
        '\n'
        'Then go to [Usage](#Usage)\n'
        '\n'
        'If you want to understand the decisions that lead to this mess go to [Why Filenames?](#Why Filenames?)\n'
        '\n'
        'If you think that putting the tags into the filenames is a bad solution go to [Alternatives](#Alternatives)\n'
        '\n'
        '# Limitations\n'
        '\n'
        'Putting the tags into the filenames is limited by the maximum path length and maximum file length.\n'
        'Windows, Linux, GoogleDrive, OneDrive, Dropbox, etc. all have different restraints\n'
        'on those.\n'
        '\n'
        '- Linux has a maximum filename length of 255 characters for most filesystems (including EXT4), and a maximum path of\n'
        '  4096\n'
        '  characters. [link](https://unix.stackexchange.com/questions/32795/what-is-the-maximum-allowed-filename-and-folder-size-with-ecryptfs)\n'
        '- Without Long Paths enabled Windows 10 has a maximum path length of\n'
        '  260 [link](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry)\n'
        '- With Long Paths enabled Windows 10 has a maximum path length of\n'
        '  32,767 [link](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry#:~:text=path%20length%20of-,32%2C767%20characters,-.%20This%20type%20of)\n'
        '\n'
        'If you intend to use this tool you should check what the systems you are planning to use\n'
        'are supporting. Maybe even run some tests.\n'
        '\n'
        'Make yourself clear about these limitations before using this tool as they cannot be circumvented.\n'
        '\n'
        'That said in most cases it´s pretty easy to stay below the limits unless you use very high number of long tags.\n'
        '\n'
        '# Why Filenames?\n'
        '\n'
        'This is the conclusion of a [reddit post](TODO)\n'
        '\n'
        '# Summary\n'
        '\n'
        '- Filenames are a good enough solution in the majority of cases.\n'
        '- Every good enough solution is better than a perfect solution that is never finished.\n'
        '- Every alternative to filenames I found so far either had other limitations or would require 100s of hours of work\n'
        '  to produce a satisfying program.\n'
        '- I don`t get paid, and I won`t spend 100s of hours implement a niche tool that only a handful of people will use.\n'
        '\n'
        '## Why Filenames are Good\n'
        '\n'
        '- Very verbose, can see tags with every file browser\n'
        '- Re-using what already exists\n'
        '    - File browser\n'
        '    - Thumbnail cache\n'
        '    - Search and indexing functionality\n'
        '    - Image viewers\n'
        '- Works in pretty much every cloud web interface\n'
        '    - => Access your media files via tags everywhere without having to download them first\n'
        '- Works with every type of file\n'
        '- Tags don`t get lost on conversion\n'
        '- Tags don`t get lost when file is moved outside the tool\n'
        '- Tags always stay synced with file even when working on multiple machines \n'
        '  - => No need to sync databases, metafiles etc.\n'
        '\n'
        '## Alternative Solutions\n'
        '\n'
        '### Database\n'
        '\n'
        '- What happens when files are moved outside the tool?\n'
        '- Would require indexing\n'
        '- Needs a thumbnail cache and a file browser with search functionality\n'
        '- How to sync the database to different PC?\n'
        '- Can`t use tags in the cloud web interface\n'
        '- Would basically just re-implement one of the countless tagging solutions that already exist\n'
        '\n'
        '### Accompanying Metafiles\n'
        '\n'
        '- Files always have to be moved together\n'
        '- Would require indexing\n'
        '- Needs a thumbnail cache and a file browser with search functionality\n'
        '- Can`t use tags in the cloud web interface\n'
        '\n'
        '### Metadata of the Files\n'
        '\n'
        '- Not supported for a lot of file types\n'
        '- Would need to treat every file type special\n'
        '- Would require indexing\n'
        '- Needs a thumbnail cache and a file browser with search functionality\n'
        '- Can`t use tags in the cloud web interface\n'
        '\n'
        '# Alternatives\n'
        '\n'
        'Originally I was going to put a list of alternatives here, but then I found too many and none really satisfied me. That why I created this tool in the first place.\n'
        '\n'
        'There is an abundance of tagging tools out there. If you find one that is \n'
        '- cross-platform\n'
        '- works with cloud sync\n'
        '- works in the cloud web interface\n'
        '- can easily manage 100s of tags\n'
        '- can easily manage dozens of tags per file  \n'
        '\n'
        'let me know, so I can add it.')