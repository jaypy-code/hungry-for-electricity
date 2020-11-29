import os
import threading
import subprocess

path = "/sys/class/power_supply/BAT1"  # Battery system folder
# current battery capacity lavel/percent
capacityFile = os.path.join(path, 'capacity')
# current battery status (Charging, Discharging, Full, Unknow)
statusFile = os.path.join(path, 'status')
minCapacity = 15  # min battery capacity level/percent could be
time = 1  # execute interval function for how many second(s) ?
# last stored status/last status at last executed function for ${time} second(s) !
global lastStatus
lastStatus = ''
global lastPercent  # last stored battery level
lastPercent = 50
global said  # It's just used for doINeedDischarge and doINeedCharge
said = False


def getPercent():
    file = open(capacityFile, 'r').read()
    return int(file)


def getStatus():
    file = open(statusFile, 'r').read()
    return str(file)


def notification(message):
    clearNotifications()
    subprocess.Popen(['notify-send', '--hint', 'int:transient:1', message])


def clearNotifications():
    subprocess.Popen(['pkill', 'notify-osd'])


def amINowCharging(status):
    #  was n't charing = True     and    now is charging
    if lastStatus.startswith('D') and status.startswith('C'):
        notification("Oh, yees :)")
        pass  # TODO: Play mp3 file or use notification function and more ...


def amINowDischarging(status):
    #    was charging = True      and   now is discharging
    if lastStatus.startswith('C') and status.startswith('D'):
        notification("Oh noo :(")
        pass  # TODO: Play mp3 file or use notification function and more ...


def doINeedCharge(percent, status):
    global said
    #    10    <=    15       and   is discharched
    if percent <= minCapacity and status.startswith("D"):
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
    return minCapacity < percent and percent <= 100


def changeSaid(percent, status):
    global said
    if said == True:
        #     was full charged        and   now is discharging
        if(lastStatus.startswith('F') and status.startswith('D')):
            said = False
        # last percent was less then min and now is more then min
        elif(lastPercent <= minCapacity and minCapacity < percent):
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
setInterval(interval, time)
