# How to generate the Backup.exe file

pyinstaller --onefile BackupX.py

# How to generate the BackupSettings.exe file

pyinstaller --onefile BackupSettings.py

# What to do next

* When removing files to skip, we should just be able to enter a number
* Improve to see better where the files are going in the logs
* Make it so that when picking a filename, we can pick a .lnk link instead of manually inputting it in the config
* Make each config easier to understand to users in the settings
* It should be that each destination folders have a set of conditions for a fileto go there. Most importantly we should have a contains + noncasesensitive feature.
