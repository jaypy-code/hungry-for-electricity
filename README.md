# Hungry for electricity
Hungry for electricity is a name for this simple python project ( It get's your custom status of Linux battery level )

# How to use ?
App configuration is in ``` config.yaml ``` file and change your's configuration if it need.

So just run ``` python app.py ``` is enough.

# Fix your issue
1- There is a file for change screen/monitor britness value that need permission to r&w for user ( not root ) and you need chmod that file to 707. Do this if you don't know how and what to do.
```
$ sudo chmod 707 /sys/class/backlight/intel_backlight/brightness
```
Warning: Correct folder path is in your yaml config file, this path is mine and probably be like your's path.

# Changelogs
[Nov 29 2020] First commit with just simple release and idea of the project

[Nov 30 2020] Second commit with changing screen/monitor brightness and wrote a yaml config file

[Now 30 2020] Third commit with enable/disable changing screen/monitor brightness