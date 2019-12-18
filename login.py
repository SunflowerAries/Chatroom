from PyQt5 import QtCore, QtGui, QtWidgets
from message import *
from event_handler import *
from listen import Dialogs

class block(QtWidgets.QWidget):
    def setupblock(self, QWidget, name, words=None, toinput=True, error=True):
        self.box = QtWidgets.QVBoxLayout(QWidget)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        if toinput == True:
            self.toInput = QtWidgets.QLineEdit()
            self.toInput.setPlaceholderText(name)
            self.toInput.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
            self.toInput.setObjectName(name)
            self.toInput.setStyleSheet("background-color:rgba(255, 0, 0, 0); border: 1px solid #aaa; border-radius:4px;")
            self.box.addWidget(self.toInput)
            self.box.setStretchFactor(self.toInput, 5)
        self.prompt(words, error)
        self.box.addLayout(self.hbox)

    def prompt(self, reason, error=True):
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.setContentsMargins(0, 5, 0, 0)
        self.hbox.setSpacing(0)
        icon = QtWidgets.QLabel()
        prompt = QtWidgets.QLabel()
        if error:
            jpg2 = QtGui.QPixmap("Pic/error.png")
            prompt.setStyleSheet("color: #ff5b5b;")
        else:
            jpg2 = QtGui.QPixmap("Pic/Finished.png")
            prompt.setStyleSheet("color: #91ED61;")
        
        prompt.setText(reason)
        icon.resize(18, 18)
        icon.setPixmap(jpg2.scaled(icon.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        icon.setObjectName("Icon")
        icon.setVisible(False)
        self.hbox.addWidget(icon)
        self.hbox.setStretchFactor(icon, 1)

        prompt.resize(200, 50)
        
        prompt.setObjectName("Prompt")
        prompt.setFont(QtGui.QFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold)))
        prompt.setVisible(False)
        self.hbox.addWidget(prompt)
        self.hbox.setStretchFactor(prompt, 19)
        

class Ui_Dialog2(QtWidgets.QDialog):
    def setupUi(self, Dialog, sock):
        Dialog.setObjectName("Signup")
        Dialog.setFixedSize(1200, 720)
        Dialog.setStyleSheet("QDialog{\n"
        "background-color:rgb(255, 255, 255);}\n}"
"QLineEdit{\n"
"background-color:rgba(255, 0, 0, 0); border: 2px solid #aaa; border-radius:4px}\n"
"\n"
"QLabel{\n"
"color:#ff5b5b;}"
"\n"
"QPushButton{\n"
"background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);}\n"
"")
        self.sock = sock
        plane = QtWidgets.QHBoxLayout(Dialog)
        plane.setContentsMargins(0, 0, 0, 0)

        background = QtWidgets.QLabel()
        jpg = QtGui.QPixmap('Pic/signup.jpg')
        background.resize(510, 720)
        background.setPixmap(jpg.scaled(background.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        background.setObjectName("Background")
        plane.addWidget(background)  
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.setContentsMargins(100, 0, 100, 100)
        vbox.setSpacing(0)
        
        icon = QtWidgets.QLabel()
        jpg1 = QtGui.QPixmap('Pic/Icon.jpg')
        icon.resize(350, 70)
        icon.setPixmap(jpg1.scaled(icon.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        icon.setObjectName("Icon")
        icon.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(icon)
        vbox.setStretchFactor(icon, 5)

        setblock = block()

        self.Username = QtWidgets.QWidget()
        setblock.setupblock(self.Username, "Username", "Username cannot be empty", True)
        self.UsernameInput = self.Username.findChild(QtWidgets.QLineEdit, "Username")
        self.UsernameInput.installEventFilter(self)
        vbox.addWidget(self.Username)
        vbox.addStretch(1)

        self.Nickname = QtWidgets.QWidget()
        setblock.setupblock(self.Nickname, "Nickname", "Nickname cannot be empty", True)
        self.NicknameInput = self.Nickname.findChild(QtWidgets.QLineEdit, "Nickname")
        self.NicknameInput.installEventFilter(self)
        vbox.addWidget(self.Nickname)
        vbox.addStretch(1)

        self.Password = QtWidgets.QWidget()
        setblock.setupblock(self.Password, "Password", "Password cannot be empty", True)
        self.PasswordInput = self.Password.findChild(QtWidgets.QLineEdit, "Password")
        self.PasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordInput.installEventFilter(self)
        vbox.addWidget(self.Password)
        vbox.addStretch(1)

        self.Password2 = QtWidgets.QWidget()
        setblock.setupblock(self.Password2, "Re-enter password", "Two passwords should be consistent", True)
        self.PasswordInput2 = self.Password2.findChild(QtWidgets.QLineEdit, "Re-enter password")
        self.PasswordInput2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordInput2.installEventFilter(self)
        vbox.addWidget(self.Password2)
        vbox.addStretch(1.5)

        self.btnSignup = QtWidgets.QPushButton()
        self.btnSignup.setObjectName("btnSignup")
        ################## Signup button#########################
        self.btnSignup.clicked.connect(self.SignupButton)
        ###########################################################
        vbox.addWidget(self.btnSignup)
        vbox.setStretchFactor(self.btnSignup, 6)
        vbox.addStretch(0.5)

        ending = QtWidgets.QHBoxLayout()
        ending.setContentsMargins(0, 20, 0, 0)
        ending.setSpacing(0)
        ending.addStretch(2)

        self.btnBack = QtWidgets.QPushButton()
        self.btnBack.setObjectName("btnBack")
        self.btnBack.clicked.connect(self.BackButton)

        ending.addWidget(self.btnBack)
        ending.setStretchFactor(self.btnBack, 1)
        vbox.addLayout(ending)
        vbox.setStretchFactor(ending, 2)

        plane.addLayout(vbox)
        plane.setStretchFactor(vbox, 8)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def eventFilter(self, object, event):        
        layout = object.parentWidget()
        prompt = layout.findChild(QtWidgets.QLabel, "Prompt")
        error = layout.findChild(QtWidgets.QLabel, "Icon")
        if event.type() == QtCore.QEvent.FocusIn:
            object.setStyleSheet("border:1px solid #549df8; border-radius:4px;}")
            prompt.setVisible(False)
            error.setVisible(False)
            if object == self.UsernameInput:
                prompt.setText("Username cannot be empty")

        elif event.type() == QtCore.QEvent.FocusOut:
            text = object.text()
            if len(text) == 0:
                object.setStyleSheet("border: 1px solid #ff5b5b; focus{\nborder:1px solid #549df8;}\n")
                prompt.setVisible(True)
                error.setVisible(True)
            else:
                object.setStyleSheet("border: 1px solid #aaa; focus{\nborder:1px solid #549df8;}\n")

        return super(Ui_Dialog2, self).eventFilter(object, event)

    def BackButton(self):
        self.clearField()
        if self.handler_for_login_logup in callback_func:
            callback_func.remove(self.handler_for_login_logup)
        self.close()

    def handler_for_login_logup(self, itype, header):
        if itype == MessageType.register_successful:
            self.register_successful(header)
        elif itype == MessageType.username_taken:
            self.username_taken(header)

    def register_successful(self, parameters):
        print('register_successful', parameters)
        self.clearField()
        if self.handler_for_login_logup in callback_func:
            callback_func.remove(self.handler_for_login_logup)
        if Dialogs[2].handler_for_online not in callback_func:
            add_listener(Dialogs[2].handler_for_online)
        Dialogs[2].Info(parameters)
        Dialogs[2].show()
        self.close()

    def username_taken(self, parameters):
        print('username_taken')
        self.prompt(self.UsernameInput, 1)
        print(parameters)

    def SignupButton(self):
        username = self.UsernameInput.text()
        nickname = self.NicknameInput.text()
        password = self.PasswordInput.text()
        password2 = self.PasswordInput2.text()
        if self.checkFields(username,nickname,password,password2):
            return
        else:
            if self.checkPassword(password,password2):
                header = serial_header_pack(MessageType.register, [username, password, nickname])
                self.sock.conn.send(header)
                if self.handler_for_login_logup not in callback_func:
                    add_listener(self.handler_for_login_logup)# TODO
            else:
                self.prompt(self.PasswordInput2)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chatroom"))
        self.btnSignup.setText(_translate("Dialog", "Sign Up"))
        self.btnSignup.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        self.btnBack.setText(_translate("Dialog", "Back"))
        self.btnBack.setFont(QtGui.QFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold)))
        
    def checkFields(self,username,nickname,password,password2):
        if username=="":
            self.prompt(self.UsernameInput)
            return True
        elif nickname=="":
            self.prompt(self.NicknameInput)
            return True
        elif password== "":
            self.prompt(self.PasswordInput)
            return True
        elif password2=="":
            self.prompt(self.PasswordInput2)
            return True
        return False

    def prompt(self, object, choice=0):
        layout = object.parentWidget()
        prompt = layout.findChild(QtWidgets.QLabel, "Prompt")
        error = layout.findChild(QtWidgets.QLabel, "Icon")
        if choice == 1 and object == self.UsernameInput:
            prompt.setText("This username has been taken")
        object.setStyleSheet("border: 1px solid #ff5b5b; focus{\nborder:1px solid #549df8;}\n")
        prompt.setVisible(True)
        error.setVisible(True)

    def hide(self, object):
        object.setText(None)
        layout = object.parentWidget()
        prompt = layout.findChild(QtWidgets.QLabel, "Prompt")
        error = layout.findChild(QtWidgets.QLabel, "Icon")
        object.setStyleSheet("border: 1px solid #aaa; focus{\nborder:1px solid #549df8;}\n")
        prompt.setVisible(False)
        error.setVisible(False)

    ############## check if password1 and password2 matches #############
    def checkPassword(self,password1, password2):
        return password1 == password2

    ##################### clear fields ##################
    def clearField(self):
        self.hide(self.UsernameInput)
        self.hide(self.NicknameInput)
        self.hide(self.PasswordInput)
        self.hide(self.PasswordInput2)

class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog, sock):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(1200, 720)
        Dialog.setStyleSheet("QDialog{\n"
        "background-color:rgb(255, 255, 255);}\n}"
"QLineEdit{\n"
"background-color:rgba(255, 0, 0, 0); border: 2px solid #aaa; border-radius:4px}\n"
"\n"
"QLabel{\n"
"color:#ff5b5b;}"
"\n"
"QPushButton{\n"
"background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);}\n"
"")
        self.sock = sock
        plane = QtWidgets.QHBoxLayout(Dialog)
        plane.setContentsMargins(0, 0, 0, 0)

        background = QtWidgets.QLabel()
        jpg = QtGui.QPixmap('Pic/signin.jpg')
        background.resize(510, 720)
        background.setPixmap(jpg.scaled(background.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        background.setObjectName("Background")
        plane.addWidget(background)
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.setContentsMargins(100, 70, 100, 100)
        vbox.setSpacing(0)

        icon = QtWidgets.QLabel()
        jpg1 = QtGui.QPixmap('Pic/Icon.jpg')
        icon.resize(350, 70)
        icon.setPixmap(jpg1.scaled(icon.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        icon.setObjectName("Icon")
        icon.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(icon)
        vbox.setStretchFactor(icon, 5)

        setblock = block()

        self.Username = QtWidgets.QWidget()
        setblock.setupblock(self.Username, "Username", "Username cannot be empty", True)
        self.UsernameInput = self.Username.findChild(QtWidgets.QLineEdit, "Username")
        self.UsernameInput.installEventFilter(self)
        vbox.addWidget(self.Username)
        vbox.addStretch(1)

        self.Password = QtWidgets.QWidget()
        setblock.setupblock(self.Password, "Password", "Password cannot be empty", True)
        self.PasswordInput = self.Password.findChild(QtWidgets.QLineEdit, "Password")
        self.PasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordInput.installEventFilter(self)
        vbox.addWidget(self.Password)
        vbox.addStretch(1.5)

        self.btnSignin = QtWidgets.QPushButton()
        self.btnSignin.setObjectName("btnSignin")
        ################## Signup button#########################
        self.btnSignin.clicked.connect(self.SigninCheck)
        ###########################################################
        vbox.addWidget(self.btnSignin)
        vbox.setStretchFactor(self.btnSignin, 6)
        vbox.addStretch(0.5)

        ending = QtWidgets.QHBoxLayout()
        ending.setContentsMargins(0, 20, 0, 0)
        ending.setSpacing(0)
        ending.addStretch(2)

        self.btnSignup = QtWidgets.QPushButton()
        self.btnSignup.setObjectName("btnSignup")
        self.btnSignup.clicked.connect(self.SignupButton)
        ending.addWidget(self.btnSignup)
        ending.setStretchFactor(self.btnSignup, 1)
        vbox.addLayout(ending)
        vbox.setStretchFactor(ending, 2)

        plane.addLayout(vbox)
        plane.setStretchFactor(vbox, 8)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def handler_for_login_logup(self, itype, header):
        if itype == MessageType.login_successful:
            self.login_successful(header)
        elif itype == MessageType.user_not_exist:
            self.user_not_exist(header)
        elif itype == MessageType.wrong_password:
            self.wrong_password(header)

    def login_successful(self, parameters):
        print('login_successful')
        # print(parameters)
        self.clearField()
        if self.handler_for_login_logup in callback_func:
            callback_func.remove(self.handler_for_login_logup)
        data = serial_data_unpack(self.sock)

        if Dialogs[2].handler_for_online not in callback_func:
            add_listener(Dialogs[2].handler_for_online)
        Dialogs[2].Info(parameters)
        Dialogs[2].show()
        print(data)
        self.close()

    def user_not_exist(self, parameters):
        print('user_not_exist')
        self.prompt(self.UsernameInput, 1)
        print(parameters)

    def wrong_password(self, parameters):
        print('wrong_password')
        self.prompt(self.PasswordInput, 1)
        print(parameters)

    def eventFilter(self, object, event):        
        layout = object.parentWidget()
        prompt = layout.findChild(QtWidgets.QLabel, "Prompt")
        error = layout.findChild(QtWidgets.QLabel, "Icon")
        if event.type() == QtCore.QEvent.FocusIn:
            object.setStyleSheet("border:1px solid #549df8; border-radius:4px;}")
            prompt.setVisible(False)
            error.setVisible(False)
            if object == self.UsernameInput:
                prompt.setText("Username cannot be empty")
            elif object == self.PasswordInput:
                prompt.setText("Password cannot be empty")    

        elif event.type() == QtCore.QEvent.FocusOut:
            text = object.text()
            if len(text) == 0:
                object.setStyleSheet("border: 1px solid #ff5b5b; focus{\nborder:1px solid #549df8;}\n")
                prompt.setVisible(True)
                error.setVisible(True)
            else:
                object.setStyleSheet("border: 1px solid #aaa; focus{\nborder:1px solid #549df8;}\n")

        return super(Ui_Dialog, self).eventFilter(object, event)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chatroom"))
        self.btnSignin.setText(_translate("Dialog", "Sign in"))
        self.btnSignin.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        self.btnSignup.setText(_translate("Dialog", "Sign Up"))
        self.btnSignup.setFont(QtGui.QFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold)))
        
    def SigninCheck(self):
        username = self.UsernameInput.text()
        password = self.PasswordInput.text()
        if self.checkFields(username,password):
            return
        else:
            header = serial_header_pack(MessageType.login, [username, password])
            self.sock.conn.send(header)
            if self.handler_for_login_logup not in callback_func:
                add_listener(self.handler_for_login_logup)
    
    def checkFields(self,username,password):
        if username=="":
            self.prompt(self.UsernameInput)
            return True
        elif password== "":
            self.prompt(self.PasswordInput)
            return True
        return False

    def prompt(self, object, choice=0):
        layout = object.parentWidget()
        prompt = layout.findChild(QtWidgets.QLabel, "Prompt")
        error = layout.findChild(QtWidgets.QLabel, "Icon")
        object.setStyleSheet("border: 1px solid #ff5b5b; focus{\nborder:1px solid #549df8;}\n")
        if choice == 1:
            if object == self.UsernameInput:
                prompt.setText("Username does not exist")
            elif object == self.PasswordInput:
                prompt.setText("Password you have entered is incorrect")
        prompt.setVisible(True)
        error.setVisible(True)

    def hide(self, object):
        object.setText(None)
        layout = object.parentWidget()
        prompt = layout.findChild(QtWidgets.QLabel, "Prompt")
        error = layout.findChild(QtWidgets.QLabel, "Icon")
        object.setStyleSheet("border: 1px solid #aaa; focus{\nborder:1px solid #549df8;}\n")
        prompt.setVisible(False)
        error.setVisible(False)

    def SignupButton(self):   
        self.clearField()
        if self.handler_for_login_logup in callback_func:
            callback_func.remove(self.handler_for_login_logup)
        self.close()
                
    def clearField(self):
        self.hide(self.UsernameInput)
        self.hide(self.PasswordInput)

class Dialog(Ui_Dialog):
    def __init__(self, sock, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self, sock)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

class Dialog2(Ui_Dialog2):
    def __init__(self, sock, parent=None):
        super(Dialog2, self).__init__(parent)
        self.setupUi(self, sock)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Window1 = Dialog()
#     Window2 = Dialog2()
    
#     Window1.btnSignup.clicked.connect(Window2.show)
#     Window2.btnBack.clicked.connect(Window1.show)
#     Window1.show()

#     sys.exit(app.exec_())
