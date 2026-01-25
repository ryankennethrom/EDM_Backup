# How to generate the exe files

./build.sh

But first, you need to run "chmod +x build.sh" one time on fresh clone.
The exe files are generate in root/dist

# What you can improve 

* When removing files to skip, we should just be able to enter a number
* Improve to see better where the files are going in the logs
* When picking a .lnk file, it will treat it as if it its name is the original file instead of the shortcut file's name. Fix this.
* Make it so that the folders directory, name, skip, and source configs are separate and modular from the exe file
