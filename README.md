# OJ
Simple configurable script for managing daily notes.

Useful:

- test/functional_test/\* = use cases \ expected behaviour
- `python -c 'import configurator; help(configurator)` = settings

# Usage
1. Create config file — `touch $HOME/.config/oj.ini` 
2. Edit config file with your data, e.g.:
```ini
[PATH]
# directory where notes are located
destination = /home/John_Doe/notes
# this file text data is used as base to new note
template    = /home/John_Doe/notes/new_note_template.md

[FILENAME]
# ISO 8601 format
date format = %%Y-%%m-%%d
extension   = .md
```
3. Run script (source: `oj.py`; builded: `oj`)
