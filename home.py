from PyQt5 import QtCore, QtGui, QtWidgets

def setupIcon(Icon, url, size):
    jpg = QtGui.QPixmap(url)
    Icon.resize(size[0], size[1])
    Icon.setPixmap(jpg.scaled(Icon.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.setFixedSize(1330, 980)
        self.setStyleSheet("QLineEdit{\n"
"border:none; color:#fff;}\n"
"QLabel#selfie{\n"
"border-radius:200px;}\n"
"QLabel{\n"
"border-right: 1px solid #24272c; color:#fff; border-radius: 20px}\n"
"\n"
"QPushButton{\n"
"    background-color:qradialgradient(spread:repeat, cx:0.5, cy:0.5, radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(0, 169, 255, 147), stop:0.497326 rgba(0, 0, 0, 147), stop:1 rgba(0, 169, 255, 147));\n"
"color:rgb(255, 255, 255)\n"
"}\n"
"")
        toppanel = QtWidgets.QWidget(self)
        self.setCentralWidget(toppanel)
        panel = QtWidgets.QHBoxLayout()
        panel.setContentsMargins(0, 0, 0, 0)
        panel.setSpacing(0)

        self.sidebarContainer = QtWidgets.QWidget()
        self.sidebar = QtWidgets.QVBoxLayout(self.sidebarContainer)
        self.sidebarContainer.setStyleSheet("background-color:rgb(38, 41, 46);")
        
        # self.infoContainer = QtWidgets.QWidget()
        self.info = QtWidgets.QHBoxLayout() # Self-info
        self.info.setSpacing(0)
        
        self.selfie = QtWidgets.QLabel()
        setupIcon(self.selfie, 'Pic/selfie.jpg', [50, 50])
        self.selfie.setObjectName('selfie')
        self.info.addWidget(self.selfie)
        self.info.setStretchFactor(self.selfie, 2)

        self.name = QtWidgets.QLabel()
        self.name.resize(200, 45)
        self.name.setText("二立")
        self.name.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        self.info.addWidget(self.name)
        self.info.setStretchFactor(self.name, 6)
        self.sidebar.addLayout(self.info)
        self.sidebar.setSpacing(0)

        self.searchContainer = QtWidgets.QWidget()
        self.search = QtWidgets.QHBoxLayout(self.searchContainer) # Search
        self.search.setSpacing(0)
        self.searchIcon = QtWidgets.QLabel()
        setupIcon(self.searchIcon, 'Pic/Search.png', [35, 35])
        self.search.addWidget(self.searchIcon)
        self.search.setStretchFactor(self.searchIcon, 1)

        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText("Search")
        # self.searchInput.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.searchInput.setFont(QtGui.QFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold)))
        self.search.addWidget(self.searchInput)
        self.search.setStretchFactor(self.searchInput, 25)

        self.searchContainer.setStyleSheet("background-color:#26292e; border-radius:2px;")
        self.sidebar.addWidget(self.searchContainer)
        self.sidebar.setStretchFactor(self.search, 2)

        # self.ctrlContainer = QtWidgets.QWidget()
        self.ctrl = QtWidgets.QHBoxLayout() # Control for main window
        self.ctrl.setSpacing(0)
        self.ctrl.addStretch(1)
        
        self.chatIcon = QtWidgets.QLabel()
        setupIcon(self.chatIcon, 'Pic/Chat-G.png', [45, 45])
        self.chatIcon.mousePressEvent = self.switchtoChat
        self.ctrl.addWidget(self.chatIcon)
        self.ctrl.setStretchFactor(self.chatIcon, 4)

        self.friendIcon = QtWidgets.QLabel()
        setupIcon(self.friendIcon, 'Pic/Friend.png', [45, 45])
        self.friendIcon.mousePressEvent = self.switchtoFriend
        self.ctrl.addWidget(self.friendIcon)
        self.ctrl.setStretchFactor(self.friendIcon, 4)

        self.discoveryIcon = QtWidgets.QLabel()
        setupIcon(self.discoveryIcon, 'Pic/Discovery.png', [45, 45])
        self.discoveryIcon.mousePressEvent = self.switchtoDiscovery
        self.ctrl.addWidget(self.discoveryIcon)
        self.ctrl.setStretchFactor(self.discoveryIcon, 4)

        self.sidebar.addLayout(self.ctrl)
        self.sidebar.setStretchFactor(self.ctrl, 2)

        self.list_for_chat = QtWidgets.QVBoxLayout() # Chat
        self.sidebar.addLayout(self.list_for_chat)

        self.list_for_friend = QtWidgets.QVBoxLayout() # Friend
        self.sidebar.addLayout(self.list_for_friend)
        
        panel.addWidget(self.sidebarContainer)
        panel.setStretchFactor(self.sidebar, 5)

        self.sidewindow = QtWidgets.QWidget()
        panel.addWidget(self.sidewindow)
        panel.setStretchFactor(self.sidewindow, 14)

        toppanel.setLayout(panel)

        self.retranslateUi()
        # QtCore.QMetaObject.connectSlotsByName()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def switchtoChat(self, event):
        print("In chat")
        setupIcon(self.chatIcon, 'Pic/Chat-G.png', [45, 45])
        setupIcon(self.friendIcon, 'Pic/Friend.png', [45, 45])
        setupIcon(self.discoveryIcon, 'Pic/Discovery.png', [45, 45])
        # self.chatIcon.setStyleSheet("background-color:rgb(115, 201, 40)")
    
    def switchtoFriend(self, event):
        print("In Friend")
        setupIcon(self.chatIcon, 'Pic/Chat.png', [45, 45])
        setupIcon(self.friendIcon, 'Pic/Friend-G.png', [45, 45])
        setupIcon(self.discoveryIcon, 'Pic/Discovery.png', [45, 45])

    def switchtoDiscovery(self, event):
        print("In Discovery")
        setupIcon(self.chatIcon, 'Pic/Chat.png', [45, 45])
        setupIcon(self.friendIcon, 'Pic/Friend.png', [45, 45])
        setupIcon(self.discoveryIcon, 'Pic/Discovery-G.png', [45, 45])

# class Mainwindow(Ui_MainWindow):
#     def __init__(self, parent=None):
#         super(Ui_MainWindow, self).__init__(parent)
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window = Ui_MainWindow()
    Window.show()
    sys.exit(app.exec_())

