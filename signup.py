from PyQt5 import QtCore, QtGui, QtWidgets
from database_tmp import Db

class block(QtWidgets.QWidget):
    def setupblock(self, QWidget, name):
        self.box = QtWidgets.QVBoxLayout(QWidget)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        self.toInput = QtWidgets.QLineEdit()
        # self.toInput = MyLineEdit()
        self.toInput.setPlaceholderText(name)
        self.toInput.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        self.toInput.setObjectName(name)
        self.box.addWidget(self.toInput)
        self.box.setStretchFactor(self.toInput, 5)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0, 5, 0, 0)
        hbox.setSpacing(0)
        error = QtWidgets.QLabel()
        jpg2 = QtGui.QPixmap("Pic/error.png")
        error.resize(18, 18)
        error.setPixmap(jpg2.scaled(error.size(), aspectRatioMode= QtCore.Qt.KeepAspectRatio))
        error.setObjectName("Error")
        error.setVisible(False)
        hbox.addWidget(error)
        hbox.setStretchFactor(error, 1)
        # hbox.addStretch(1)

        prompt = QtWidgets.QLabel()
        prompt.resize(200, 50)
        if name.endswith("Again"):
            prompt.setText("You should confirm your password")
        else:
            prompt.setText(name + " cannot be empty")
        prompt.setObjectName("Prompt")
        prompt.setFont(QtGui.QFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold)))
        prompt.setVisible(False)
        hbox.addWidget(prompt)
        hbox.setStretchFactor(prompt, 19)
        hbox.setObjectName("Container")
        self.box.addLayout(hbox)

class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Signup")
        Dialog.setFixedSize(1200, 720)
        Dialog.setStyleSheet("QDialog{\n"
        "background-color:rgb(255, 255, 255);}\n}"
"QLineEdit{\n"
"background-color:rgb(255, 0, 0, 0); border: 1px solid #aaa; border-radius:4px;}\n"
"\n"
"QLabel{\n"
"color:#ff5b5b;}"
"\n"
"QPushButton{\n"
"background-color:#3487ff;background-image: qlineargradient(0deg,#398bff,#3083ff); color:rgb(255,255,255);}\n"
"")
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
        setblock.setupblock(self.Username, "Username")
        self.Username.findChild(QtWidgets.QLineEdit, "Username").installEventFilter(self)
        vbox.addWidget(self.Username)
        vbox.addStretch(1)

        self.Nickname = QtWidgets.QWidget()
        setblock.setupblock(self.Nickname, "Nickname")
        self.Nickname.findChild(QtWidgets.QLineEdit, "Nickname").installEventFilter(self)
        vbox.addWidget(self.Nickname)
        vbox.addStretch(1)

        self.Password = QtWidgets.QWidget()
        setblock.setupblock(self.Password, "Password")
        self.Password.findChild(QtWidgets.QLineEdit, "Password").setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password.findChild(QtWidgets.QLineEdit, "Password").installEventFilter(self)
        vbox.addWidget(self.Password)
        vbox.addStretch(1)

        self.Password2 = QtWidgets.QWidget()
        setblock.setupblock(self.Password2, "Password Again")
        self.Password2.findChild(QtWidgets.QLineEdit, "Password Again").setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password2.findChild(QtWidgets.QLineEdit, "Password Again").installEventFilter(self)
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
        #################### SignUp Button #############################
        self.btnBack.clicked.connect(self.BackButton)
        ################################################################
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
        error = layout.findChild(QtWidgets.QLabel, "Error")
        if event.type() == QtCore.QEvent.FocusIn:
            object.setStyleSheet("border:1px solid #549df8; border-radius:4px;}")
            prompt.setVisible(False)
            error.setVisible(False)

        elif event.type() == QtCore.QEvent.FocusOut:
            text = object.text()
            if len(text) == 0:
                object.setStyleSheet("border: 1px solid #ff5b5b; focus{\nborder:1px solid #549df8;}\n")
                prompt.setVisible(True)
                error.setVisible(True)
            else:
                object.setStyleSheet("border: 1px solid #aaa; focus{\nborder:1px solid #549df8;}\n")

        return super(Ui_Dialog, self).eventFilter(object, event)

    def SignupButton(self):
        username = self.txtUsername.text()
        nickname = self.txtNickname.text()
        password = self.txtPassword.text()
        password2 = self.txtPassword2.text()
        if self.checkFields(username,nickname,password,password2):
            return
        else:
            if(self.checkPassword(password,password2)):
                insertDb = Db()
                Db().insertTable(nickname,username,password)
                self.showMessage("Success","Registration successul")
                self.clearField()
            else:
                self.showMessage("Error","Passwords doesn't match")
    
    def BackButton(self):   
        self.signDialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog2()
        self.ui.setupUi(self.signDialog)
        self.signDialog.show()
        Dialog.close()

    def showMessage(self,title,msg):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        #msgBox.setTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chatroom"))
        self.btnSignup.setText(_translate("Dialog", "Sign Up"))
        self.btnSignup.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        self.btnBack.setText(_translate("Dialog", "Back"))
        self.btnBack.setFont(QtGui.QFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold)))
        
    def checkFields(self,username,nickname,password,password2):
        if username=="":
            return
        elif nickname=="":
            return
        elif password== "":
            return
        elif password2=="":
            return
        

    ############## check if password1 and password2 matches #############
    def checkPassword(self,password1, password2):
        return password1 == password2

    ##################### clear fields ##################
    def clearField(self):
        self.txtUsername.setText(None)
        self.txtPassword.setText(None)
        self.txtNickname.setText(None)
        self.txtPassword2.setText(None)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

