import os
import threading
import subprocess
import yaml
import datetime

# Read config file as stream
config = dict()
with open('config.yaml') as stream:
    config = yaml.safe_load(stream)


# current screen (monitor) brightness level
brightnessFilePath = os.path.join(config['backlight']['path'], 'brightness')
# max screen (monitor) brightness level
maxBrightnessFilePath = os.path.join(
    config['backlight']['path'], 'max_brightness')
# Read and set max screen (monitor) brightness level
maxBrightness = int(open(maxBrightnessFilePath, 'r').read())
# current battery capacity lavel/percent
capacityFilePath = os.path.join(config['battery']['path'], 'capacity')
# current battery status (Charging, Discharging, Full, Unknow)
statusFilePath = os.path.join(config['battery']['path'], 'status')
# last stored status/last status at last executed function for ${time} second(s) !
global lastStatus
lastStatus = ''
global lastPercent  # last stored battery level
lastPercent = 50
global said  # It's just used for doINeedDischarge and doINeedCharge
said = False


def log(message):
    if config['log']['enable'] == True:
        try:
            mode = 'a' if os.path.exists(config['log']['path']) else 'w'
            with open(config['log']['path'], mode) as file:
                file.write('['+str(datetime.datetime.now())+'] ' + message+'\n')
        except:
            print("Error while log")
            pass

# set screen (monitor) brightness


def setBrightness(level):
    try:
        # convert percent of brightness in config to system
        level = int((level * maxBrightness) / 100)
        brightnessFile = open(brightnessFilePath, 'w')
        brightnessFile.write(str(level))
        brightnessFile.close()
    except:
        log("Permission to write " + brightnessFilePath + "file")

# battery percent charge


def getPercent():
    return int(open(capacityFilePath, 'r').read())

# battery status
# returns: (Charging, Discharging, Full, Unknow)


def getStatus():
    return str(open(statusFilePath, 'r').read())


def notification(message):
    clearNotifications()
    subprocess.Popen(['notify-send', '--hint', 'int:transient:1', message])


def clearNotifications():
    subprocess.Popen(['pkill', 'notify-osd'])


def amINowCharging(status):
    #  was n't charing = True     and    now is charging
    if lastStatus.startswith('D') and status.startswith('C'):
        print("Chargning ...")
        notification("Oh, yees :)")
        setBrightness(config['backlight']['charging'])
        pass  # TODO: Play mp3 file or use notification function and more ...


def amINowDischarging(status):
    #    was charging = True      and   now is discharging
    if lastStatus.startswith('C') and status.startswith('D'):
        print("Discharging ...")
        notification("Oh noo :(")
        setBrightness(config['backlight']['discharging'])
        pass  # TODO: Play mp3 file or use notification function and more ...


def doINeedCharge(percent, status):
    global said
    #    10    <=    15       and   is discharched
    if percent <= config['battery']['minLevel'] and status.startswith("D"):
        said = True
        notification("Need electricity to eat !!!")
        pass  # TODO: Play mp3 file or use notification function and more ...


def doINeedDischarge(status):
    global said
    #       Was full = True       and    Discharging now
    if status.startswith("F"):
        said = True
        notification("I ate all electricity I needed !!")
        pass  # TODO: Play mp3 file or use notification function and more ...


def doIDoNothing(percent, status):
    return config['battery']['minLevel'] < percent and percent <= 100


def changeSaid(percent, status):
    global said
    if said == True:
        #     was full charged        and   now is discharging
        if(lastStatus.startswith('F') and status.startswith('D')):
            said = False
        # last percent was less then min and now is more then min
        elif(lastPercent <= config['battery']['minLevel'] and config['battery']['minLevel'] < percent):
            said = False
        else:
            pass


def setInterval(func, sec):
    def wrapper():
        setInterval(func, sec)
        func()
    thread = threading.Timer(sec, wrapper)
    thread.start()
    return thread


def interval():
    percent = getPercent()
    status = getStatus()

    if doIDoNothing(percent, status) == False and said == False:
        doINeedCharge(percent, status)
        doINeedDischarge(status)
    else:
        amINowCharging(status)
        amINowDischarging(status)
        changeSaid(percent, status)

    if(status.startswith('U') == False):  # If new status wasn't Unknow
        global lastStatus
        lastStatus = status

    global lastPercent
    lastPercent = percent


# excute the function for each time
setInterval(interval, config['interval']['time'])
log("App running ...")
