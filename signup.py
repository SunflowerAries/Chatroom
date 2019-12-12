from PyQt5 import QtCore, QtGui, QtWidgets
from database_tmp import Db

class MyLineEdit(QtWidgets.QLineEdit):
    def focusInEvent(self, event):
        



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Signup")
        Dialog.setFixedSize(1200, 720)
        Dialog.setStyleSheet("QDialog{\n"
        "background-color:rgb(255, 255, 255);}\n}"
"QLineEdit{\n"
"background-color:rgb(255, 0, 0, 0); border: 2px solid #aaa; border-radius:4px}\n"
"\n"
"Q{\n"
"font: 75 italic 14pt \"Century Schoolbook L\";\n"
"\n"
"}\n"
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

        txtUsername = QtWidgets.QLineEdit()
        txtUsername.setPlaceholderText("Username")
        txtUsername.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        txtUsername.setObjectName("txtUsername")
        vbox.addWidget(txtUsername)
        vbox.setStretchFactor(txtUsername, 5)
        # txtUsername.focusInEvent()
        vbox.addStretch(1)

        txtNickname = QtWidgets.QLineEdit()
        txtNickname.setPlaceholderText("Nickname")
        txtNickname.setObjectName("txtNickname")
        txtNickname.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        vbox.addWidget(txtNickname)
        vbox.setStretchFactor(txtNickname, 5)
        vbox.addStretch(1)

        txtPassword = QtWidgets.QLineEdit()
        txtPassword.setPlaceholderText("Password")
        ################## make the password invisible ############
        txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        ###########################################################
        txtPassword.setObjectName("txtPassword")
        txtPassword.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        txtPassword.focusInEvent(self.FocusInput)
        vbox.addWidget(txtPassword)
        vbox.setStretchFactor(txtPassword, 5)
        vbox.addStretch(1)
        
        txtPassword2 = QtWidgets.QLineEdit()
        txtPassword2.setPlaceholderText("Password Again")
        ################## make the password invisible ############
        txtPassword2.setEchoMode(QtWidgets.QLineEdit.Password)
        ###########################################################
        txtPassword2.setObjectName("txtPassword")
        txtPassword2.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        vbox.addWidget(txtPassword2)
        vbox.setStretchFactor(txtPassword2, 5)
        vbox.addStretch(1.5)

        self.btnSignup = QtWidgets.QPushButton()
        self.btnSignup.setObjectName("btnSignup")
        ################## Signup button#########################
        self.btnSignup.clicked.connect(self.SignupButton)
        ###########################################################
        vbox.addWidget(self.btnSignup)
        vbox.setStretchFactor(self.btnSignup, 6)

        plane.addLayout(vbox)
        plane.setStretchFactor(vbox, 8)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def FocusInput(self):
        
        pass

    def SignupButton(self):
        username = txtUsername.text()
        nickname = txtNickname.text()
        password = txtPassword.text()
        password2 = txtPassword2.text()
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
        
    def loginPage(self):
        self.loginWindow = QtWidgets.QDialog()
        self.ui = Ui_Dialog2()
        self.ui.setupUi(self.loginWindow)
        self.loginWindow.show()
        
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
        txtUsername.setText(None)
        txtPassword.setText(None)
        txtNickname.setText(None)
        txtPassword2.setText(None)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

