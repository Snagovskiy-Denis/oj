# whatis oj
Simple configurable script for managing daily notes.

## What does it do specifically
1. On run:
- creates new file (note) in given directory
- notes name is todays date in given format
- writes text of template file into note 
- opens note

2. On run if todays note exists:
- opens note (only)

# Usage
1. Create config file — `$ touch $HOME/.config/oj.ini` 
2. Edit config file with your data, e.g.:
```ini
[PATH]
# directory where notes will be located
destination = /home/johndoe/notes
# this files text data is used as base to new note
template    = /home/johndoe/notes/daily_note_template.md

[FILENAME]
# ISO 8601 format
# double % escapes single %
date format = %%Y-%%m-%%d
extension   = .md
```
3. Run script 
- source : `$ ./oj.py`
- release: `$ oj`
