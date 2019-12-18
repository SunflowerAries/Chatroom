from PyQt5 import QtWidgets, QtGui, QtCore

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