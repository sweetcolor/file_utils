# File Utilities 
some scripts and utils to work with files


## Smart copy

Can copy file or directory. It can copy source file to destination file
or destination directory. If destination file is already exist 
It continue copying if destination size is less than source 
or skip if equal. It does not check data in existing destination file,
so be careful, but this feature will be added in one of future release.
Also it can recursively copy directory and merge with existing 
destination directory.

##### Dependency

Work on python 3.6 or above

##### Using

``
python3 smart_copy.py <SOURCE_PATH> <DESTINATION_PATH>
``

##### Version

0.0.1

## Categorize files by extension

Move files with same extension to directory named by this extension

##### Dependency

Work on python 3.6 or above

##### Using

``
python3 smart_copy.py <DIRECTORY_PATH>
``

##### Version

0.0.1-alpha.1