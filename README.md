# About

The primary purpose of this program is to tag files by adding the tags to the name of the file.

The use case it is designed for is the organization of rpg map hoards and other media files a DM comes in contact with.

Anyone who every comes into contact with this task will quickly find that no folder structure will every be the right one.

## Example

To add the tags `tag1`, `tag2` and `tag3` to the file `some_map.png` it would be renamed to `SOME-MAP;tag1_tag2_tag3.png
`

# Where to Start

If you are a new user who is planning to use this program read about its [limitations](#Limitations) first.

Then go to [Install](#Install)

Then go to [Usage](#Usage)

If you want to understand the decisions that lead to this mess go to [Why Filenames?](#Why Filenames?)

If you think that putting the tags into the filenames is a bad solution go to [Alternatives](#Alternatives)

# Limitations

Putting the tags into the filenames is limited by the maximum path length and maximum file length.
Windows, Linux, GoogleDrive, OneDrive, Dropbox, etc. all have different restraints
on those.

- Linux has a maximum filename length of 255 characters for most filesystems (including EXT4), and a maximum path of
  4096
  characters. [link](https://unix.stackexchange.com/questions/32795/what-is-the-maximum-allowed-filename-and-folder-size-with-ecryptfs)
- Without Long Paths enabled Windows 10 has a maximum path length of
  260 [link](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry)
- With Long Paths enabled Windows 10 has a maximum path length of
  32,767 [link](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry#:~:text=path%20length%20of-,32%2C767%20characters,-.%20This%20type%20of)

If you intend to use this tool you should check what the systems you are planning to use
are supporting. Maybe even run some tests.

Make yourself clear about these limitations before using this tool as they cannot be circumvented.

That said in most cases it's pretty easy to stay below the limits unless you use very high number of long tags.

# Why Filenames?

This is the conclusion of a [reddit post](TODO)

# Summary

- Filenames are a good enough solution in the majority of cases.
- Every good enough solution is better than a perfect solution that is never finished.
- Every alternative to filenames I found so far either had other limitations or would require 100s of hours of work
  to produce a satisfying program.
- I don't get paid, and I won't spend 100s of hours implement a niche tool that only a handful of people will use.

## Why Filenames are Good

- Very verbose, can see tags with every file browser
- Re-using what already exists
    - File browser
    - Thumbnail cache
    - Search and indexing functionality
    - Image viewers
- Works in pretty much every cloud web interface
    - => Access your media files via tags everywhere without having to download them first
- Works with every type of file
- Tags don't get lost on conversion
- Tags don't get lost when file is moved outside the tool
- Tags always stay synced with file even when working on multiple machines 
  - => No need to sync databases, metafiles etc.

## Alternative Solutions

### Database

- What happens when files are moved outside the tool?
- Would require indexing
- Needs a thumbnail cache and a file browser with search functionality
- How to sync the database to different PC?
- Can't use tags in the cloud web interface
- Would basically just re-implement one of the countless tagging solutions that already exist

### Accompanying Metafiles

- Files always have to be moved together
- Would require indexing
- Needs a thumbnail cache and a file browser with search functionality
- Can't use tags in the cloud web interface

### Metadata of the Files

- Not supported for a lot of file types
- Would need to treat every file type special
- Would require indexing
- Needs a thumbnail cache and a file browser with search functionality
- Can't use tags in the cloud web interface

# Alternatives

Originally I was going to put a list of alternatives here, but then I found too many and none really satisfied me. That why I created this tool in the first place.

There is an abundance of tagging tools out there. If you find one that is 
- cross-platform
- works with cloud sync
- works in the cloud web interface
- can easily manage 100s of tags
- can easily manage dozens of tags per file  

let me know, so I can add it.