from PyQt5 import QtWidgets, QtGui, QtCore
import re, time
from datetime import timedelta, datetime

def setupIcon(Icon, url, size):
    jpg = QtGui.QPixmap(url)
    Icon.resize(size[0], size[1])
    Icon.setPixmap(jpg.scaled(Icon.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))

def Ray(object, num): # 0: blue 1: red
    layout = object.parentWidget()
    prompt = layout.findChild(QtWidgets.QLabel, "Prompt")
    error = layout.findChild(QtWidgets.QLabel, "Icon")
    if num == 0:
        object.setStyleSheet("border:1px solid #549df8; border-radius:4px;}")
        prompt.setVisible(False)
        error.setVisible(False)
    elif num == 1:
        prompt.setVisible(True)
        error.setVisible(True)
        object.setStyleSheet("border:1px solid #ff5b5b; border-radius:4px;\n")

def calculate(time1, time2):
    if time1 == None:
        return True
    tim1 = datetime.strptime(time1['Date'], "%a %b %d %H:%M:%S %Y")
    tim2 = datetime.strptime(time2['Date'], "%a %b %d %H:%M:%S %Y")
    print(tim1, tim1)
    print(timedelta(minutes=5), timedelta(minutes=5))
    return tim2 > tim1 + timedelta(minutes=5)
    # print(time1['Date'], time2['Date'])
    return True

def feed(String):
    index = [i.start() for i in re.finditer(' ', String)]
    # print(index)
    k = 1
    i = j = 0
    num = 0
    lenth = len(String)
    while i < lenth:
        if num % 50 == 0 and num != 0:
            for m in range(j, len(index)):
                if index[m] > i:
                    if index[m] - i < 5:
                        j = m + 1
                        String = String[:index[m]+k] + '\n' + String[index[m]+k:]
                        i = index[m]
                        # print(String, i, k, "First")
                    else:
                        i = index[m - 1]
                        j = m
                        String = String[:i+k] + '\n' + String[i+k:]
                        # print(String, i, k, "Second")
                    break
            num = 0
            k += 1
            continue
        i += 1
        num += 1
    # print(String)
    return String
