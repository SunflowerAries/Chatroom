from PyQt5 import QtCore, QtGui, QtWidgets
from database_tmp import Db #importing database.py
from home import Ui_MainWindow
from signup import Ui_Dialog


class Ui_Dialog2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
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

        self.txtUsername = QtWidgets.QLineEdit()
        self.txtUsername.setPlaceholderText("Username")
        self.txtUsername.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        self.txtUsername.setObjectName("txtUsername")
        vbox.addWidget(self.txtUsername)
        vbox.setStretchFactor(self.txtUsername, 5)
        vbox.addStretch(1)

        self.txtPassword = QtWidgets.QLineEdit()
        self.txtPassword.setPlaceholderText("Password")
        ################## make the password invisible ############
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        ###########################################################
        self.txtPassword.setObjectName("txtPassword")
        self.txtPassword.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        vbox.addWidget(self.txtPassword)
        vbox.setStretchFactor(self.txtPassword, 5)        
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
        #################### SignUp Button #############################
        self.btnSignup.clicked.connect(self.signupButton)
        ################################################################
        ending.addWidget(self.btnSignup)
        ending.setStretchFactor(self.btnSignup, 1)
        vbox.addLayout(ending)
        vbox.setStretchFactor(ending, 2)

        plane.addLayout(vbox)
        plane.setStretchFactor(vbox, 8)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chatroom"))
        self.btnSignin.setText(_translate("Dialog", "Sign in"))
        self.btnSignin.setFont(QtGui.QFont(QtGui.QFont("Times", 24, QtGui.QFont.Bold)))
        self.btnSignup.setText(_translate("Dialog", "Sign Up"))
        self.btnSignup.setFont(QtGui.QFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold)))
        
    def welcomePage(self):
        self.homWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.homWindow)
        self.homWindow.show()
        
    def SigninCheck(self):
        username = self.txtUsername.text()
        password = self.txtPassword.text()
        getDb = Db()        
        result = getDb.SigninCheck(username,password)
        if(result):
            self.welcomePage()
            self.clearField()
            print(result)
        else:
            print("password wrong")
            self.showMessage("Warning","Invalid Username and Password")
            
    def showMessage(self,title,msg):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        #msgBox.setTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def signupButton(self):   
        self.signDialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.signDialog)
        self.signDialog.show()
        Dialog.close()
                
    def clearField(self):
        self.txtUsername.setText(None)
        self.txtPassword.setText(None)
        

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog2()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

