from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
import plugin.databaseConnect as database
import plugin.user as curUser
from forgetPasswordForm import forgetPasswordUI

class LoginUI(QMainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,None)
        self.setMinimumSize(900, 600)
        self.setWindowTitle("Login")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("resources/images/programBackground.png")))
        self.logo = QPixmap("resources/images/programLogo.png")
        self.setPalette(palette)
        self.parent = parent
        self.UIinit()

    def UIinit(self):
        loader = QUiLoader()
        form = loader.load("resources/UI/login.ui", None)
        self.setCentralWidget(form)
        self.logolabel = form.findChild(QLabel,"label_2")
        self.logolabel.setPixmap(self.logo)
        self.wronglabel = form.findChild(QLabel,"wrong")
        self.wronglabel.setStyleSheet('color: red')
        self.user_id = form.findChild(QLineEdit, "usernameinp")
        self.password = form.findChild(QLineEdit, "pwinp")

        self.login_button = form.findChild(QPushButton, "loginButton")
        self.forgetpw_button = form.findChild(QCommandLinkButton, "forgetButton")

        self.status = form.findChild(QLabel,"status_2")
        self.password.returnPressed.connect(self.logIn)
        self.login_button.clicked.connect(self.logIn)
        self.forgetpw_button.clicked.connect(self.forgetpass)
        
        try:
            self.login = database.databaseLogin()
            self.data = database.databaseUser()
            self.status.setText("Online")
        except database.invalidQueryException as e:
            self.wronglabel.setText(str(e))
            self.status.setText("Offline")
            
    ##Checking Log-in by using user ID and password##    
    def logIn(self):
        try:
            #DEFAULTPASS123456
            if(self.user_id.text() == "" or self.password.text() ==""):
                raise database.invalidQueryException("Fields cannot be Empty")
            status = self.login.userLogin(self.user_id.text(), self.password.text())
            if(status[0]):
                self.wronglabel.setText("")
                self.user_id.setText("")
                self.password.setText("")
                user_data = self.data.getInfo(status)
                user_address = self.data.getAddress(status)
                if (status[4] == 1):
                    self.parent.showERROR("User Suspended", "You have been suspended from the system.")
                    raise database.invalidQueryException("User Suspended")
                if(status[2] == 0):
                    faculty = self.data.getFaculty(user_data.facultyID)
                    major = self.data.getMajor(user_data.majorID)
                    student = curUser.student(user_data, status[3], user_address, faculty, major)
                    self.parent.setCurrentUser(student)
                    self.parent.changePageLoginSection("home")
                if(status[2] == 1):
                    faculty = self.data.getFaculty(user_data.facultyID)
                    professor= curUser.professor(user_data, status[3], user_address, faculty)
                    self.parent.setCurrentUser(professor)
                    self.parent.changePageLoginSection("home")
                if (status[2] == 2):
                    admin = curUser.admin(user_data, status[3], user_address)
                    self.parent.setCurrentUser(admin)
                    self.parent.changePageLoginSection("home")
                if(status[3] == 3):
                    self.parent.showERROR("User Suspended","You have been suspended from the system.")
                    self.wronglabel.setText("User Suspended")
        except database.invalidQueryException as e:
            self.wronglabel.setText(str(e))
            self.user_id.setText("")
            self.password.setText("")       

    ##For user that forget their password##
    def forgetpass(self):
        self.forget = forgetPasswordUI(parent = self.parent)
        self.forget.show()
        
