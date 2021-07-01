# whatis oj
Daily note manager for Console Dwellers

## What does it do specifically
1. On run:
- creates new file (note) in given directory
- notes name is todays date in given format
- writes text of template file into note 
- opens note

2. On run if todays note exists:
- opens note (only)

# Usage
## Basic
Run script with defaults with --skip option
- source : `$ ./oj.py --skip`
- release: `$ oj --skip`

This will create an empty file in current directory by default.

## Advance
You can change default behaviour on fly with --option
- source : `$ ./oj.py --skip --option destination=~/stuff/notes template=~/stuff/new_note.txt date_format=%%d.%%m.%%Y`
- release: `$ oj --skip --option destination=~/stuff/notes template=~/stuff/new_note.txt date_format=%%d.%%m.%%Y`

This will create new file:
- In HOME/stuff/notes directory
- With copy of text of HOME/stuff/new_note.txt
- And with filename like this: 31.12.2000.txt

## With config file
Run script with --config option
- source : `$ ./oj.py --config`
- release: `$ oj --config`

This will create file on path HOME/.config/oj.ini with valid settings and useful comments.

You could re-run this command to quickly re-open already existing config file.


It is also possible to read existing config file on another path with this option:

`--option config_directory=/another/directory/with/oj.ini/file`

# Future of project
I created oj basically for myself. 

I will add new features if I feel like I need them. I am happy by this so far.

However I am open for requests and pull requests.
