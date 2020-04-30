# coding: UTF-8

import sys
import os

# Switch using adb shell setprop, format is item -> [key, onValue, offValue]
setPropMap = {"overdraw": ["debug.hwui.overdraw", "show", "off", "过度绘制"],
              "layout": ["debug.layout", "true", "false", "显示布局边界"],
              "gpuprofile": ["debug.hwui.profile", "visual_bars", "false", "GPU呈现模式分析"]}

# Switch using settings put, format is item -> [type, key, onValue, offValue]
putSettingsMap = {"stayawake": ["global", "stay_on_while_plugged_in", "1", "0", "充电时不锁定屏幕"],
                "alwaysfinish": ["global", "always_finish_activities", "1", "0", "不保留活动"]}


def main():
    if len(sys.argv) < 2:
        print("Please specified an operation!")
        return

    operation = sys.argv[1]

    if operation == "toggle":
        handleToggle()
    elif operation == "help":
        printHelp()
    elif operation == "reboot":
        os.open("adb reboot")
    elif operation == "ss":
        runAdbShell("mkdir /sdcard/tmp")
        runAdbShell("screencap -p /sdcard/tmp/tmp.png")
        os.system("adb pull /sdcard/tmp/tmp.png ./adbscreenshot.png && start ./adbscreenshot.png")

def printHelp():
    print("=======================================")
    print("======== ADB小助手 by GlorinLi ========")
    print("=======================================")
    print("\n【功能一】切换开关，使用方法: toggle key, 其中 key 如下：")
    for key, value in setPropMap.items():
        print("    " + key + " -> " + value[3])
    for key, value in putSettingsMap.items():
        print("    " + key + " -> " + value[4])

    print("\n【功能二】重启，使用方法: reboot")

    print("\n【功能三】截图，使用方法: ss")

def handleToggle():
    if len(sys.argv) < 3:
        print("Please specified an item to toggle!")
        return

    item = sys.argv[2]
    
    for key, value in setPropMap.items():
        if key == item:
            toggleProp(value[0], value[1], value[2])
    
    for key, value in putSettingsMap.items():
        if key == item:
            toggleSettings(value[0], value[1], value[2], value[3])


def toggleProp(key, onValue, offValue):
    current = runAdbShell("getprop " + key)
    target = onValue if current == offValue else offValue

    print("Current is " + current + ", Set to: " + target)
    runAdbShell("setprop " + key + " " + target)

def toggleSettings(settingType, key, onValue, offValue):
    current = runAdbShell("settings get " + settingType + " " + key)
    target = onValue if current == offValue else offValue

    print("Current is " + current + ", Set to: " + target)
    runAdbShell("settings put " + settingType + " " + key + " " + target)


def runAdbShell(cmd):
    return os.popen("adb shell " + cmd).read().strip()


if __name__ == '__main__':
    main()
