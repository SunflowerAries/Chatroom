from PyQt5 import QtCore, QtGui, QtWidgets
from login import block
from event_handler import *

def setupIcon(Icon, url, size):
    jpg = QtGui.QPixmap(url)
    Icon.resize(size[0], size[1])
    Icon.setPixmap(jpg.scaled(Icon.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))

def Ray(object, num): # 0: blue 1: red
    layout = object.parentWidget()
    prompt = layout.findChild(QtWidgets.QLabel, "Prompt")
    error = layout.findChild(QtWidgets.QLabel, "Error")
    if num == 0:
        object.setStyleSheet("border:1px solid #549df8; border-radius:4px;}")
        prompt.setVisible(False)
        error.setVisible(False)
    elif num == 1:
        prompt.setVisible(True)
        error.setVisible(True)
        object.setStyleSheet("border:1px solid #ff5b5b; border-radius:4px;\n")

class Ui_Dialog3(QtWidgets.QWidget):
    def setupUi(self, Dialog, sock):
        Dialog.setObjectName("MainDialog")
        Dialog.setFixedSize(1330, 980)
        Dialog.setStyleSheet("QLineEdit{\n"
"border:none; color:#fff;}\n"
"QLabel#selfie{\n"
"border-radius:200px;}\n"
"QLabel{\n"
"border-right: 1px solid #24272c; color:#fff; border-radius: 20px}\n"
"\n"
"QPushButton{\n"
"background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);}\n"
"")
        self.sock = sock
        panel = QtWidgets.QHBoxLayout(Dialog)
        panel.setContentsMargins(0, 0, 0, 0)
        panel.setSpacing(0)

        self.sidebarContainer = QtWidgets.QWidget()
        self.sidebar = QtWidgets.QVBoxLayout(self.sidebarContainer)
        self.sidebar.setContentsMargins(15, 10, 0, 0)
        self.sidebarContainer.setStyleSheet("background-color:rgb(38, 41, 46);")
        
        self.infoContainer = QtWidgets.QWidget()
        self.info = QtWidgets.QHBoxLayout(self.infoContainer) # Self-info
        self.info.setContentsMargins(0, 0, 0, 0)
        self.info.setSpacing(0)
        
        self.selfie = QtWidgets.QLabel()
        setupIcon(self.selfie, 'Pic/Selfie-init.png', [50, 50])
        self.selfie.setObjectName('selfie')
        self.info.addWidget(self.selfie)
        self.info.setStretchFactor(self.selfie, 2)

        self.name = QtWidgets.QLabel()
        self.name.resize(200, 45)
        # self.name.setText("二立")
        self.name.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        self.info.addWidget(self.name)
        self.info.setStretchFactor(self.name, 6)

        self.add = QtWidgets.QLabel()
        setupIcon(self.add, 'Pic/add.png', [26, 26])
        self.add.setObjectName('Add')
        self.add.installEventFilter(self)
        self.info.addWidget(self.add)
        self.info.setStretchFactor(self.add, 2)

        self.sidebar.addWidget(self.infoContainer)
        self.sidebar.setStretchFactor(self.infoContainer, 3)
        self.sidebar.setSpacing(0)

        self.searchContainer = QtWidgets.QWidget()
        self.search = QtWidgets.QHBoxLayout(self.searchContainer) # Search
        self.search.setSpacing(0)
        self.search.setContentsMargins(0, 0, 0, 0)
        self.searchIcon = QtWidgets.QLabel()
        setupIcon(self.searchIcon, 'Pic/Search.png', [40, 40])
        self.search.addWidget(self.searchIcon)
        self.search.setStretchFactor(self.searchIcon, 1)

        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText("Search")
        self.searchInput.setFont(QtGui.QFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold)))
        self.search.addWidget(self.searchInput)
        self.search.setStretchFactor(self.searchInput, 25)

        self.searchContainer.setStyleSheet("background-color:#26292e; border-radius:2px;")
        self.sidebar.addWidget(self.searchContainer)
        self.sidebar.setStretchFactor(self.searchContainer, 2)

        self.ctrlContainer = QtWidgets.QWidget()
        self.ctrl = QtWidgets.QHBoxLayout(self.ctrlContainer) # Control for main Dialog
        self.ctrl.setContentsMargins(0, 0, 0, 0)
        self.ctrl.setSpacing(0)
        self.ctrl.addStretch(1)
        
        self.chatIcon = QtWidgets.QLabel()
        setupIcon(self.chatIcon, 'Pic/Chat-G.png', [50, 50])
        self.chatIcon.installEventFilter(self)
        self.ctrl.addWidget(self.chatIcon)
        self.ctrl.setStretchFactor(self.chatIcon, 4)

        self.friendIcon = QtWidgets.QLabel()
        setupIcon(self.friendIcon, 'Pic/Friend.png', [50, 50])
        self.friendIcon.installEventFilter(self)
        self.ctrl.addWidget(self.friendIcon)
        self.ctrl.setStretchFactor(self.friendIcon, 4)

        self.discoveryIcon = QtWidgets.QLabel()
        setupIcon(self.discoveryIcon, 'Pic/Discovery.png', [50, 50])
        self.discoveryIcon.installEventFilter(self)
        self.ctrl.addWidget(self.discoveryIcon)
        self.ctrl.setStretchFactor(self.discoveryIcon, 4)

        self.sidebar.addWidget(self.ctrlContainer)
        self.sidebar.setStretchFactor(self.ctrlContainer, 2)

        self.list_for_chatContainer = QtWidgets.QWidget()
        self.list_for_chat = QtWidgets.QVBoxLayout(self.list_for_chatContainer) # Chat
        self.sidebar.addWidget(self.list_for_chatContainer)
        self.sidebar.setStretchFactor(self.list_for_chatContainer, 40)
        self.list_for_chatContainer.setVisible(True)

        self.list_for_friendContainer = QtWidgets.QWidget()
        self.list_for_friend = QtWidgets.QVBoxLayout(self.list_for_friendContainer) # Friend
        self.sidebar.addWidget(self.list_for_friendContainer)
        self.sidebar.setStretchFactor(self.list_for_friendContainer, 25)
        self.list_for_friendContainer.setVisible(False)
        
        panel.addWidget(self.sidebarContainer)
        panel.setStretchFactor(self.sidebar, 5)

        self.sideDialog = QtWidgets.QWidget()
        panel.addWidget(self.sideDialog)
        panel.setStretchFactor(self.sideDialog, 14)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if object == self.chatIcon:
                self.switchtoChat(event)
            elif object == self.friendIcon:
                self.switchtoFriend(event)
            elif object == self.discoveryIcon:
                self.switchtoDiscovery(event)
            elif object == self.add:
                self.showAdd(event)

        elif event.type() == QtCore.QEvent.FocusIn:
            Ray(object, 0)
            prompt = object.parentWidget().findChild(QtWidgets.QLabel, "Prompt")
            if object == self.SearchfriendInput:
                prompt.setText("Name cannot be empty")
        
        elif event.type() == QtCore.QEvent.FocusOut:
            text = object.text()
            if len(text) == 0:
                Ray(object, 1)
            else:
                object.setStyleSheet("border: 1px solid #aaa; border-radius:4px;")
        
        return super(Ui_Dialog3, self).eventFilter(object, event)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Homepage"))

    def showAdd(self, event):
        print("In show")
        self.msgbox = QtWidgets.QDialog()
        self.msgbox.setStyleSheet("QPushButton{background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);}")
        self.msgbox.setFixedSize(200, 180)
        self.addbox = QtWidgets.QVBoxLayout(self.msgbox)
        
        self.addbox.setSpacing(0)
        self.createGroup = QtWidgets.QPushButton()
        self.createGroup.setText("Create groups")
        self.createGroup.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        self.createGroup.setObjectName("Create groups")
        self.addbox.addWidget(self.createGroup)
        self.addbox.setStretchFactor(self.createGroup, 5)
        self.addbox.addStretch(1)

        self.joinGroup = QtWidgets.QPushButton()
        self.joinGroup.setText("Join groups")
        self.joinGroup.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        self.joinGroup.setObjectName("Join groups")
        self.addbox.addWidget(self.joinGroup)
        self.addbox.setStretchFactor(self.joinGroup, 5)
        self.addbox.addStretch(1)

        self.addFriend = QtWidgets.QPushButton()
        self.addFriend.setText("Add friends")
        self.addFriend.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        self.addFriend.setObjectName("Add friends")
        self.addbox.addWidget(self.addFriend)
        self.addbox.setStretchFactor(self.addFriend, 5)

        self.createGroup.clicked.connect(self.groupCreate)
        self.joinGroup.clicked.connect(self.groupJoin)
        self.addFriend.clicked.connect(self.friendAdd)
        self.msgbox.show()

    def groupCreate(self):
        pass

    def groupJoin(self):
        pass

    def prompt(self, object, choice=0):
        prompt = object.parentWidget().findChild(QtWidgets.QLabel, "Prompt")
        if choice == 1:
            if object == self.SearchfriendInput:
                prompt.setText("Sorry, no person with that username/nickname")
            elif object == self.PasswordInput:
                prompt.setText("Password you have entered is incorrect")
        Ray(object, 1)

    def friendAdd(self):
        self.searchFriend = QtWidgets.QDialog()
        self.searchFriend.setFixedSize(850, 400)
        self.searchFriend.setStyleSheet("background-color:rgb(255, 255, 255);")

        plane = QtWidgets.QHBoxLayout(self.searchFriend)
        plane.setContentsMargins(0, 0, 0, 0)

        background = QtWidgets.QLabel()
        jpg = QtGui.QPixmap('Pic/searchFriend.jpg')
        background.resize(400, 400)
        background.setPixmap(jpg.scaled(background.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        background.setObjectName("Background")
        plane.addWidget(background)
        plane.addStretch(1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 20, 0, 0)

        setblock = block()
        self.Searchfriend = QtWidgets.QWidget()
        setblock.setupblock(self.Searchfriend, "Name")
        self.SearchfriendInput = self.Searchfriend.findChild(QtWidgets.QLineEdit, 'Name')
        self.SearchfriendInput.setPlaceholderText("Username/Nickname")
        self.SearchfriendInput.installEventFilter(self)
        vbox.addWidget(self.Searchfriend)
        vbox.setStretchFactor(self.Searchfriend, 2)
        vbox.addStretch(1)

        self.searchname = QtWidgets.QPushButton()
        self.searchname.setFont(QtGui.QFont(QtGui.QFont("Arial", 24)))
        self.searchname.setText("Find")
        self.searchname.setStyleSheet("background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);")
        self.searchname.clicked.connect(self.friendSearch)
        vbox.addWidget(self.searchname)
        vbox.setStretchFactor(self.searchname, 2)
        vbox.addStretch(1)

        self.list_for_searchnameContainer = QtWidgets.QWidget()
        self.list_for_searchname = QtWidgets.QVBoxLayout(self.list_for_searchnameContainer)
        vbox.addWidget(self.list_for_searchnameContainer)
        vbox.setStretchFactor(self.list_for_searchnameContainer, 8)
        
        plane.addLayout(vbox)
        plane.setStretchFactor(vbox, 6)
        plane.addStretch(1)
        self.searchFriend.show()
        self.msgbox.close()    

    def friendSearch(self):
        name = self.SearchfriendInput.text()
        if name=="":
            self.SearchfriendInput.setStyleSheet("border: 1px solid #ff5b5b; border-radius:4px focus{\nborder:1px solid #549df8;}\n")
            self.prompt(self.SearchfriendInput)
        else:
            header = serial_header_pack(MessageType.query_friend, [name])
            self.sock.conn.send(header)
            if self.handler_for_online not in callback_func:
                add_listener(self.handler_for_online)

    def handler_for_online(self, itype, header):
        if itype == MessageType.friend_found:
            self.friend_found(header)
        elif itype == MessageType.friend_not_found:
            self.friend_not_found(header)

    def friend_found(self, parameters):
        print('friend_found')
        friend = serial_data_unpack(self.sock)[0]
        print(friend)
        if self.handler_for_online in callback_func:
            callback_func.remove(self.handler_for_online)

    def friend_not_found(self, parameters):
        print('friend_not_found')
        self.prompt(self.SearchfriendInput, 1)
        if self.handler_for_online in callback_func:
            callback_func.remove(self.handler_for_online)

    def switchtoChat(self, event):
        print("In chat")
        setupIcon(self.chatIcon, 'Pic/Chat-G.png', [50, 50])
        setupIcon(self.friendIcon, 'Pic/Friend.png', [50, 50])
        setupIcon(self.discoveryIcon, 'Pic/Discovery.png', [50, 50])
    
    def switchtoFriend(self, event):
        print("In Friend")
        setupIcon(self.chatIcon, 'Pic/Chat.png', [50, 50])
        setupIcon(self.friendIcon, 'Pic/Friend-G.png', [50, 50])
        setupIcon(self.discoveryIcon, 'Pic/Discovery.png', [50, 50])

    def switchtoDiscovery(self, event):
        print("In Discovery")
        setupIcon(self.chatIcon, 'Pic/Chat.png', [50, 50])
        setupIcon(self.friendIcon, 'Pic/Friend.png', [50, 50])
        setupIcon(self.discoveryIcon, 'Pic/Discovery-G.png', [50, 50])

    def Info(self, data):
        self.name.setText(data['Nickname'])


class Dialog3(Ui_Dialog3):
    def __init__(self, sock, parent=None):
        super(Dialog3, self).__init__(parent)
        self.setupUi(self, sock)

