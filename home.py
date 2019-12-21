from PyQt5 import QtCore, QtGui, QtWidgets
from login import block
from event_handler import *
from handler_for_homepage import *
import threading

friendList = []
toclick = []
sender_lock = threading.Lock()
talker_lock = threading.Lock()
totalk = []
toshow = []
lastshow = -1
lasttalk = -1

# class MyLabel(QtGui.QLabel):
#     def __init__(self, parent=None):
#         super(MyLabel, self).__init__(parent)  

#     def resizeEvent(self, event):
#         self.formatText()
#         event.accept()

#     def formatText(self):
#         width = self.width()
#         text = self.text()
#         new = ''
#         for word in text.split():
#             if len(new.split('\n')[-1])<width*0.1:
#                 new = new + ' ' + word
#             else:
#                 new = new + '\n' + ' ' + word
#         self.setText(new)

class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        # when you want to destroy the dialog set this to True
        self._want_to_release = True

    def closeEvent(self, event):
        if self._want_to_release:
            global sender_lock
            sender_lock.release()
        super(MyDialog, self).closeEvent(event)

class Ui_Dialog3(QtWidgets.QWidget):
    clearSignal = QtCore.pyqtSignal(int)
    show_listSignal = QtCore.pyqtSignal(int)
    talk_Signal = QtCore.pyqtSignal(int)
    friend_Signal = QtCore.pyqtSignal(int, bool)
    message_Signal = QtCore.pyqtSignal(int, int)
    selfInformation = {}
    tosend = -1
    myfriend = []
    mymessage = []
    myscroll= []
    sender = None
    talker = None
    talker2 = None
    def setupUi(self, Dialog, sock):
        Dialog.setObjectName("MainDialog")
        Dialog.setFixedSize(1330, 980)
        Dialog.setStyleSheet("QLineEdit{\n"
"border:none; color:#fff;}\n"
"QLabel#selfie{\n"
"border-radius:200px;}\n"
"QLabel{\n"
"color:#fff; border-radius: 20px}\n"
"QLabel#Topbar{\n"
"padding-top: 10px; padding-right: 0px; padding-bottom: 10px; padding-left: 0px; \n" 
        "margin-top: 0px; margin-right: 19px; margin-bottom: 0px; margin-left: 19px; \n"
        "border-bottom: 1px solid #d6d6d6; background-color: #eee; color:rgb(0, 0, 0); border-radius: 0;}"
"QLabel#Text{\n"
"color:#000; padding-top: 9px; padding-right: 13px; padding-bottom: 9px; padding-left: 13px;}"
"QPushButton{\n"
"background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);}\n"
"QPushButton#SendButton{\n"
"background-color:#f8f8f8;color:#222;margin-right:19px;}\n"
"")

        self.sock = sock
        panel = QtWidgets.QHBoxLayout(Dialog)
        panel.setContentsMargins(0, 0, 0, 0)
        panel.setSpacing(0)
        self.talk_Signal.connect(self.talktofriend1)
        self.friend_Signal.connect(self.showFriend)
        self.message_Signal.connect(self.receive_message)
        
        self.sidebarContainer = QtWidgets.QWidget()
        self.sidebarContainer.setFixedWidth(330)
        self.sidebarContainer.setStyleSheet("border-radius: 4px;")
        self.sidebar = QtWidgets.QVBoxLayout(self.sidebarContainer)
        self.sidebar.setContentsMargins(15, 10, 15, 0)
        self.sidebarContainer.setStyleSheet("background-color:#292c33;")

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
        self.name.resize(150, 45)
        self.name.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        self.info.addWidget(self.name)
        self.info.setStretchFactor(self.name, 6)        
        # self.name.setText("二立")

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
        setupIcon(self.chatIcon, 'Pic/Chat.png', [50, 50])
        self.chatIcon.installEventFilter(self)
        self.ctrl.addWidget(self.chatIcon)
        self.ctrl.setStretchFactor(self.chatIcon, 4)

        self.friendIcon = QtWidgets.QLabel()
        setupIcon(self.friendIcon, 'Pic/Friend-G.png', [50, 50])
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
        self.list_for_chatContainer.setVisible(False)

        self.list_for_friendContainer = QtWidgets.QWidget()
        self.list_for_friend = QtWidgets.QVBoxLayout(self.list_for_friendContainer) # Friend
        self.sidebar.setStretchFactor(self.list_for_friendContainer, 25)
        self.list_for_friend.setSpacing(0)
        self.list_for_friend.setContentsMargins(0, 0, 0, 0)
        spacer = QtWidgets.QSpacerItem(300, 980, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.list_for_friend.addSpacerItem(spacer)
        self.list_for_friendContainer.setVisible(True)

        scroll = QtWidgets.QScrollArea()
        scroll.setStyleSheet("border:none;")
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(770)
        scroll.setWidget(self.list_for_friendContainer)
        scroll.setFixedWidth(300)
        scroll.setObjectName("Sidebar")
        self.sidebar.addWidget(scroll)
        
        panel.addWidget(self.sidebarContainer)

        self.sideDialogContainer = QtWidgets.QWidget()
        self.sideDialog = QtWidgets.QVBoxLayout(self.sideDialogContainer)
        self.sideDialog.setSpacing(0)
        self.sideDialog.setContentsMargins(0, 0, 0, 0)
        self.sideDialogContainer.setFixedWidth(1000)

        self.topbar = QtWidgets.QLabel()
        self.topbar.setFixedHeight(80)
        self.topbar.setFont(QtGui.QFont(QtGui.QFont("Arial", 24)))
        self.topbar.setAlignment(QtCore.Qt.AlignCenter)
        self.topbar.setObjectName("Topbar")
        self.sideDialog.addWidget(self.topbar)
        self.sideDialog.setStretchFactor(self.topbar, 1)

        spacer = QtWidgets.QSpacerItem(1000, 980, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.sideDialog.addSpacerItem(spacer)

        panel.addWidget(self.sideDialogContainer)
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
            elif object in toclick:
                self.tosend = toclick.index(object)
                self.friendImage(event)
            elif object in totalk:
                global lasttalk
                if lasttalk != -1:
                    totalk[lasttalk].setStyleSheet("background-color:#292c33;")
                self.talker = object.property("ID")
                self.talk_Signal.emit(self.talker)
                lasttalk = self.talker
                object.setStyleSheet("background-color:#3a3f45")

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

    def send(self):
        box = toshow[self.talker]
        msg = box.findChild(QtWidgets.QTextEdit, "MSG")
        text = msg.toPlainText()
        print(text)
        header = serial_header_pack(MessageType.send_message, [self.selfInformation, self.myfriend[self.talker]])
        data = serial_data_pack([text])
        self.sock.conn.send(header + data)
        msg.clear()
        history = {}
        history['Sender'] = self.selfInformation['ID']
        history['Receiver'] = self.myfriend[self.talker]['ID']
        history['Text'] = text
        history['Date'] = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        self.mymessage[self.talker].append(history)
        self.message_Signal.emit(self.talker, len(self.mymessage[self.talker]) - 1)

    def friendImage(self, event):
        self.image = QtWidgets.QDialog()
        self.image.setFixedSize(400, 400)
        self.image.setStyleSheet("background-color:rgb(255, 255, 255);")
        panel = QtWidgets.QVBoxLayout(self.image)
        
        panel.setContentsMargins(20, 0, 20, 0)
        panel.setSpacing(0)
        
        selfie = QtWidgets.QLabel()
        selfie.setAlignment(QtCore.Qt.AlignCenter)
        setupIcon(selfie, 'Pic/Selfie-init.png', [250, 250])
        selfie.setObjectName('selfie')
        panel.addWidget(selfie)
        panel.setStretchFactor(selfie, 6)

        name = QtWidgets.QLabel()
        name.resize(200, 45)
        name.setText(friendList[self.tosend]["Nickname"] + "(" + friendList[self.tosend]["Username"] + ")")
        name.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        name.setAlignment(QtCore.Qt.AlignCenter)
        panel.addWidget(name)
        panel.setStretchFactor(name, 2)
        panel.addStretch(1)

        line = QtWidgets.QHBoxLayout()
        line.addStretch(1)
        button = QtWidgets.QPushButton()
        button.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        button.setText("Add Him")
        button.setStyleSheet("background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);")
        button.clicked.connect(self.sendRequest)
        line.addWidget(button)
        line.setStretchFactor(button, 3)
        line.addStretch(1)
        button.setObjectName("Button")
        panel.addLayout(line)

        setblock = block()
        box = QtWidgets.QWidget()
        setblock.setupblock(box, "Finished", "Request has been sent successfully", False, False, True)
        panel.addWidget(box)
        panel.setStretchFactor(box, 2)
        panel.addStretch(1)

        self.image.show()

    def sendRequest(self):
        if self.tosend != -1:
            prompt = self.image.findChild(QtWidgets.QLabel, "Prompt")
            error = self.image.findChild(QtWidgets.QLabel, "Icon")
            if friendList[self.tosend]["ID"] == self.selfInformation["ID"]:
                prompt.setText("Sorry, but you're adding yourself")
                prompt.setStyleSheet("color: #ff5b5b;")
                jpg2 = QtGui.QPixmap("Pic/error.png")
                error.setPixmap(jpg2.scaled(error.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
            else:
                header = serial_header_pack(MessageType.add_friend, [self.selfInformation, friendList[self.tosend]])
                self.sock.conn.send(header)
                prompt.setText("Request has been sent successfully")
            prompt.setVisible(True)
            error.setVisible(True)

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

        panel = QtWidgets.QHBoxLayout(self.searchFriend)
        panel.setContentsMargins(0, 0, 0, 0)

        background = QtWidgets.QLabel()
        jpg = QtGui.QPixmap('Pic/searchFriend.jpg')
        background.resize(400, 400)
        background.setPixmap(jpg.scaled(background.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        background.setObjectName("Background")
        panel.addWidget(background)
        panel.addStretch(1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 20, 0, 20)

        setblock = block()
        self.Searchfriend = QtWidgets.QWidget()
        setblock.setupblock(self.Searchfriend, "Name", "Username/Nickname cannot be empty", True)
        self.SearchfriendInput = self.Searchfriend.findChild(QtWidgets.QLineEdit, 'Name')
        self.SearchfriendInput.setPlaceholderText("Username/Nickname")
        self.SearchfriendInput.installEventFilter(self)
        vbox.addWidget(self.Searchfriend)
        vbox.setStretchFactor(self.Searchfriend, 2)
        vbox.addStretch(1)

        self.clearSignal.connect(self.clearLayout)
        self.show_listSignal.connect(self.show_list)

        self.searchname = QtWidgets.QPushButton()
        self.searchname.setFont(QtGui.QFont(QtGui.QFont("Arial", 24)))
        self.searchname.setText("Find")
        self.searchname.setStyleSheet("background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);")
        self.searchname.clicked.connect(self.friendSearch)
        vbox.addWidget(self.searchname)
        vbox.setStretchFactor(self.searchname, 2)
        vbox.addStretch(1)

        scroll = QtWidgets.QScrollArea()
        scroll.setStyleSheet("border: 1px solid #D8D8D8; border-radius: 4px;")
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(210)

        self.list_for_searchnameContainer = QtWidgets.QWidget()
        self.list_for_searchname = QtWidgets.QVBoxLayout()
        self.list_for_searchnameContainer.setLayout(self.list_for_searchname)
        self.list_for_searchname.setSpacing(0)
        self.list_for_searchname.setContentsMargins(0, 0, 0, 0)
        spacer = QtWidgets.QSpacerItem(400, 210, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.list_for_searchname.addSpacerItem(spacer)

        scroll.setWidget(self.list_for_searchnameContainer)
        vbox.addWidget(scroll)
        vbox.setStretchFactor(scroll, 8)

        panel.addLayout(vbox)
        panel.setStretchFactor(vbox, 6)
        panel.addStretch(1)
        self.searchFriend.show()
        self.msgbox.close()    

    def friendSearch(self):
        name = self.SearchfriendInput.text()
        if name=="":
            self.SearchfriendInput.setStyleSheet("border: 1px solid #ff5b5b; border-radius:4px focus{\nborder:1px solid #549df8;}\n")
            self.prompt(self.SearchfriendInput)
            self.clearLayout(0)
            self.clearSignal.emit(0)
        else:
            header = serial_header_pack(MessageType.query_friend, [name])
            self.sock.conn.send(header)

    def agree_request(self):
        c = database.get_cursor()
        c.execute('update Friends set Accepted=1, Resolved=1 where Request_User_ID=? and Receive_User_ID=? and Accepted=0 and Resolved=0', [self.sender['ID'], self.selfInformation['ID']])
        header = serial_header_pack(MessageType.add_friend_successful_server, [self.sender, self.selfInformation])
        self.sock.conn.send(header)
        if self.sender not in self.myfriend:
            self.myfriend.append(self.sender)
            self.mymessage.append([])
        self.friend_Signal.emit(len(self.myfriend) - 1, False)
        self.request.close()

    def disagree_request(self):
        c = database.get_cursor()
        c.execute('update Friends set Accepted=0, Resolved=1 where Request_User_ID=? and Receive_User_ID=? and Accepted=0 and Resolved=0', [self.sender['ID'], self.selfInformation['ID']])
        self.request.close()

    def resolve_friend_request(self, parameters):
        global sender_lock
        sender_lock.acquire()
        print(parameters)
        
        parameters = parameters['Sender']
        self.sender = parameters
        self.request = MyDialog()
        self.request.setFixedSize(400, 400)
        self.request.setStyleSheet("background-color:rgb(255, 255, 255);")
        panel = QtWidgets.QVBoxLayout(self.request)
        
        panel.setContentsMargins(20, 0, 20, 0)
        panel.setSpacing(0)
        
        selfie = QtWidgets.QLabel()
        selfie.setAlignment(QtCore.Qt.AlignCenter)
        setupIcon(selfie, 'Pic/Selfie-init.png', [250, 250])
        selfie.setObjectName('selfie')
        panel.addWidget(selfie)
        panel.setStretchFactor(selfie, 6)

        name = QtWidgets.QLabel()
        name.resize(200, 45)
        name.setText(parameters["Nickname"] + "(" + parameters["Username"] + ")")
        name.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        name.setAlignment(QtCore.Qt.AlignCenter)
        panel.addWidget(name)
        panel.setStretchFactor(name, 2)
        panel.addStretch(1)

        words = QtWidgets.QLabel()
        words.setText("wants to make friends with you")
        words.setWordWrap(True)
        words.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        words.setAlignment(QtCore.Qt.AlignCenter)
        panel.addWidget(words)
        panel.setStretchFactor(words, 2)
        panel.addStretch(1)

        line = QtWidgets.QHBoxLayout()
        line.addStretch(1)
        button1 = QtWidgets.QPushButton()
        button1.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        button1.setText("Agree")
        button1.setStyleSheet("background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);")
        button1.clicked.connect(self.agree_request)
        line.addWidget(button1)
        line.setStretchFactor(button1, 3)
        line.addStretch(1)
        button1.setObjectName("Button1")

        button2 = QtWidgets.QPushButton()
        button2.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        button2.setText("Disagree")
        button2.setStyleSheet("background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);")
        button2.clicked.connect(self.disagree_request)
        line.addWidget(button2)
        line.setStretchFactor(button2, 3)
        line.addStretch(1)
        button2.setObjectName("Button2")
        panel.addLayout(line)

        setblock = block()
        box = QtWidgets.QWidget()
        setblock.setupblock(box, "Finished", "Response has been sent successfully", False, False, True)
        panel.addWidget(box)
        panel.setStretchFactor(box, 2)
        panel.addStretch(1)
        self.request.installEventFilter(self)

        self.request.show()

    def handler_for_online(self, itype, header):
        if itype == MessageType.friend_found:
            self.friend_found(header)
        elif itype == MessageType.friend_not_found:
            self.friend_not_found(header)
        elif itype == MessageType.add_friend_successful:
            self.add_friend_successful(header)
        elif itype == MessageType.resolve_friend_request:
            self.resolve_friend_request(header)
        elif itype == MessageType.receive_message:
            self.receive_message1(header)

    def receive_message1(self, parameters):
        history = {}
        history['Sender'] = parameters['Sender']['ID']
        text = serial_data_unpack(self.sock)[0]
        history['Receiver'] = self.selfInformation['ID']
        print(text)
        if 'Date' in text.keys():
            history['Date'] = text['Date']
        else:
            history['Date'] = parameters['Date']
        history['Text'] = text['Text']
        num = 0
        for i in range(len(self.myfriend)):
            if self.myfriend[i]['ID'] == history['Sender']:
                num = i
                history['Name'] = self.myfriend[i]['Nickname']
                break
        self.mymessage[num].append(history)
        self.message_Signal.emit(num, len(self.mymessage[num]) - 1)

    def receive_message(self, num, pos):
        history = self.mymessage[num][pos]
        if pos > 1:
            history1 = self.mymessage[num][pos - 1]
        else:
            history1 = None
        print(history)

        dialogContainer = QtWidgets.QWidget()
        dialogContainer.setFixedWidth(960)
        dialog = QtWidgets.QVBoxLayout(dialogContainer)
        dialog.setSpacing(0)
        message = QtWidgets.QHBoxLayout()
        message.setSpacing(0)
        message.setContentsMargins(0, 0, 0, 0)
        icon = QtWidgets.QLabel()
        jpg = QtGui.QPixmap('Pic/Selfie-init.png')
        icon.resize(50, 50)
        icon.setPixmap(jpg.scaled(icon.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        icon.setObjectName("Picture")

        words = QtWidgets.QLabel(feed(history['Text']))
        words.setMaximumWidth(1200)
        # words.setWordWrap(True)
        words.setAlignment(QtCore.Qt.AlignLeft)
        words.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        words.setObjectName("Text")
        
        if calculate(history1, history):
            Showtime = QtWidgets.QLabel()
            Showtime.setStyleSheet("color:#b2b2b2")
            # Showtime.setFixedWidth(400)
            Showtime.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
            Showtime.setText(history['Date'])
            Showtime.setFont(QtGui.QFont(QtGui.QFont("Arial", 18)))
            Showtime.setAlignment(QtCore.Qt.AlignCenter)
            dialog.addWidget(Showtime)
            tmp = QtWidgets.QLabel()
            tmp.setFixedHeight(20)
            dialog.addWidget(tmp)
        if history['Sender'] == self.selfInformation['ID']:
            spacer = QtWidgets.QSpacerItem(800, 10, QtWidgets.QSizePolicy.Expanding)
            message.addSpacerItem(spacer)
            message.addWidget(words)
            tmp = QtWidgets.QLabel()
            tmp.setFixedWidth(10)
            message.addWidget(tmp)
            icon.setAlignment(QtCore.Qt.AlignRight)
            message.addWidget(icon)
            words.setStyleSheet("border-top-left-radius: 3px;border-top-right-radius: 3px;\n"
        "border-bottom-right-radius: 3px; border-bottom-left-radius: 3px; background-color: #b2e281;")
            for i in range(len(self.myfriend)):
                if self.myfriend[i]['ID'] == history['Receiver']:
                    box = toshow[i]
                    break
        else:
            icon.setAlignment(QtCore.Qt.AlignLeft)
            tmp = QtWidgets.QLabel()
            tmp.setFixedWidth(30)
            message.addWidget(tmp)
            message.addWidget(icon)
            tmp = QtWidgets.QLabel()
            tmp.setFixedWidth(10)
            message.addWidget(tmp)
            message.addWidget(words)
            spacer = QtWidgets.QSpacerItem(800, 10, QtWidgets.QSizePolicy.Expanding)
            message.addSpacerItem(spacer)
            words.setStyleSheet("border-top-left-radius: 3px;border-top-right-radius: 3px;\n"
        "border-bottom-right-radius: 3px; border-bottom-left-radius: 3px; background-color: #fff;")
            for i in range(len(self.myfriend)):
                if self.myfriend[i]['ID'] == history['Sender']:
                    box = toshow[i]
                    break
        dialog.addLayout(message)
        box1 = box.findChild(QtWidgets.QVBoxLayout, "History")
        box1.insertWidget(box1.count() - 1, dialogContainer)
        bar = self.myscroll[num].verticalScrollBar()
        bar.rangeChanged.connect( lambda x,y: bar.setValue( 9999 ) )

    def clearLayout(self, num):
        if num == 0:
            layout = self.list_for_searchname
        i = layout.count()
        while i > 1:
            toRemove = layout.itemAt(i - 2).widget()
            # remove it from the layout list
            layout.removeWidget(toRemove)
            # remove it from the gui
            toRemove.setParent(None)
            i -= 1

    def show_list(self, num):
        self.clearSignal.emit(0)
        if num == 0:
            layout = self.list_for_searchname
        global toclick
        toclick.clear()
        for i in range(len(friendList)):
            Box = QtWidgets.QWidget()
            Username = QtWidgets.QLabel()
            Username.setFixedHeight(70)
            Username.setText(friendList[i]['Nickname'] + '(' + friendList[i]['Username'] + ')')
            Username.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
            Username.installEventFilter(self)
            layout.insertWidget(layout.count() - 1, Username)
            toclick.append(Username)

    def add_friend_successful(self, parameters):
        print(parameters)
        parameters = parameters['Receiver']
        self.image = QtWidgets.QDialog()
        self.image.setFixedSize(400, 400)
        self.image.setStyleSheet("background-color:rgb(255, 255, 255);")
        panel = QtWidgets.QVBoxLayout(self.image)
        self.myfriend.append(parameters)
        self.mymessage.append([])
        global talker_lock
        talker_lock.acquire()
        self.talker2 = len(self.myfriend) - 1
        self.talker = len(self.myfriend) - 1
        
        panel.setContentsMargins(20, 0, 20, 0)
        panel.setSpacing(0)
        
        selfie = QtWidgets.QLabel()
        selfie.setAlignment(QtCore.Qt.AlignCenter)
        setupIcon(selfie, 'Pic/Selfie-init.png', [250, 250])
        selfie.setObjectName('selfie')
        panel.addWidget(selfie)
        panel.setStretchFactor(selfie, 6)

        name = QtWidgets.QLabel()
        name.resize(200, 45)
        name.setText(parameters["Nickname"] + "(" + parameters["Username"] + ")")
        name.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        name.setAlignment(QtCore.Qt.AlignCenter)
        panel.addWidget(name)
        panel.setStretchFactor(name, 2)
        panel.addStretch(1)

        words = QtWidgets.QLabel()
        words.setText("has agreed your request")
        words.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        words.setAlignment(QtCore.Qt.AlignCenter)
        panel.addWidget(words)
        panel.setStretchFactor(words, 2)
        panel.addStretch(1)

        line = QtWidgets.QHBoxLayout()
        line.addStretch(1)
        button = QtWidgets.QPushButton()
        button.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        button.setText("Say hello to him")
        button.setStyleSheet("background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);")
        button.clicked.connect(self.talktofriend2)
        line.addWidget(button)
        line.setStretchFactor(button, 3)
        line.addStretch(1)
        button.setObjectName("Button")
        panel.addLayout(line)
        panel.setStretchFactor(line, 2)
        panel.addStretch(1)

        self.image.show()

    def talktofriend1(self, num):
        self.topbar.setText(self.myfriend[num]['Nickname'])
        global lastshow
        if lastshow != -1:
            toshow[lastshow].setVisible(False)
        toshow[num].setVisible(True)
        lastshow = num

    def talktofriend2(self, active=True):
        self.friend_Signal.emit(self.talker2, True)
        global talker_lock
        talker_lock.release()
        self.image.close()

    def friend_found(self, parameters):
        print('friend_found')
        global friendList
        if len(friendList) != 0:
            friendList.clear()
        friendList = serial_data_unpack(self.sock)
        self.show_listSignal.emit(0)

    def friend_not_found(self, parameters):
        print('friend_not_found')
        self.prompt(self.SearchfriendInput, 1)

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

    def showFriend(self, num, issue):
        User = QtWidgets.QWidget()
        User.setFixedWidth(280)
        User.setFixedHeight(70)
        Box = QtWidgets.QHBoxLayout(User)
        Box.setContentsMargins(10, 10, 0, 10)
        User.setProperty('ID', num)
        Pic = QtWidgets.QLabel()
        jpg = QtGui.QPixmap('Pic/Selfie-init.png')
        Pic.resize(50, 50)
        Pic.setPixmap(jpg.scaled(Pic.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        Pic.setObjectName("Picture")
        Box.addWidget(Pic)
        Box.setStretchFactor(Pic, 4)
        Box.addStretch(1)

        Name = QtWidgets.QLabel()
        Name.setText(self.myfriend[num]['Nickname'])
        Name.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        Name.installEventFilter(self)
        Name.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        Name.setObjectName("Name")
        Box.addWidget(Name)
        Box.setStretchFactor(Name, 22)
        User.installEventFilter(self)
        totalk.append(User)

        belowContainer = QtWidgets.QWidget()
        below = QtWidgets.QVBoxLayout(belowContainer)
        below.setContentsMargins(0, 0, 0, 0)
        below.setSpacing(0)

        historyContainer = QtWidgets.QWidget()
        historyContainer.setFixedWidth(975)
        history = QtWidgets.QVBoxLayout(historyContainer)
        historyContainer.setStyleSheet("background-color: #eee;")
        history.setSpacing(0)
        history.setContentsMargins(0, 0, 0, 0)
        history.setObjectName("History")
        scroll = QtWidgets.QScrollArea()
        scroll.setStyleSheet("border:none;")
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(620)
        scroll.setWidget(historyContainer)
        scroll.setObjectName("History")
        scroll.setFixedWidth(990)
        self.myscroll.append(scroll)

        spacer = QtWidgets.QSpacerItem(900, 980, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        history.addSpacerItem(spacer)

        below.addWidget(scroll)
        below.setStretchFactor(scroll, 8)

        msg = QtWidgets.QTextEdit()
        msg.setStyleSheet("margin-right: 19px; border-top: 1px solid #d6d6d6; background-color: #eee;")
        msg.setFixedHeight(200)
        msg.setFont(QtGui.QFont(QtGui.QFont("Arial", 16)))
        below.addWidget(msg)
        below.setStretchFactor(msg, 2)
        msg.setObjectName("MSG")

        line = QtWidgets.QHBoxLayout()
        line.setContentsMargins(0, 0, 0, 15)
        line.addStretch(13)
        sendButton = QtWidgets.QPushButton()
        sendButton.setFixedWidth(160)
        sendButton.setText("Send")
        sendButton.setFont(QtGui.QFont(QtGui.QFont("Arial", 20)))
        sendButton.clicked.connect(self.send)
        sendButton.setObjectName("SendButton")
        line.addWidget(sendButton)
        line.setStretchFactor(sendButton, 3)

        below.addLayout(line)
        below.setStretchFactor(line, 1)

        self.sideDialog.addWidget(belowContainer)
        self.sideDialog.setStretchFactor(belowContainer, 11)
        belowContainer.setVisible(False)
        toshow.append(belowContainer)

        if len(self.list_for_friend) <= 1:
            self.list_for_friend.insertWidget(self.list_for_friend.count() - 1, User)
        else:
            pos = 0
            for i in range(len(self.list_for_friend) - 1):
                name = self.list_for_friend.itemAt(i).widget().findChild(QtWidgets.QLabel, "Name").text()
                if self.myfriend[num]['Nickname'] > name:
                    pos = i + 1
                else:
                    break
            self.list_for_friend.insertWidget(pos, User)
        if issue:
            global lasttalk
            if lasttalk != -1:
                totalk[lasttalk].setStyleSheet("background-color:#292c33;")
            self.talk_Signal.emit(len(self.myfriend) - 1)
            User.setStyleSheet("background-color:#3a3f45")
            lasttalk = len(self.myfriend) - 1

    def Info(self, data, friend=False):
        self.name.setText(data['Nickname'])
        self.selfInformation['ID'] = data['ID']
        self.selfInformation['Username'] = data['Username']
        self.selfInformation['Nickname'] = data['Nickname']
        if friend:
            self.myfriend = data['Friend']
            self.mymessage = data['Message']
        for i in range(len(self.myfriend)):
            self.friend_Signal.emit(i, False)
            for j in range(len(self.mymessage[i])):
                self.message_Signal.emit(i, j)


class Dialog3(Ui_Dialog3):
    def __init__(self, sock, parent=None):
        super(Dialog3, self).__init__(parent)
        self.setupUi(self, sock)
