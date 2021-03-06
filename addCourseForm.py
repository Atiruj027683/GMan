from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
import plugin.databaseConnect as database

class addCourseUI(QMainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,None)
        self.setMinimumSize(900,600)
        self.setWindowTitle("Class Course")
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("resources/imagess/programBackground.png")))
        self.edu_logo = QPixmap("resources/images/educationLogo.png")
        self.setPalette(palette)
        self.bar = QPixmap("resources/images/topBarBackground.png")
        self.parent = parent
        self.UIinit()

    def UIinit(self):
        loader = QUiLoader()
        form = loader.load("resources/UI/addCourse.ui",None)
        self.setCentralWidget(form)
        
        #Upper Bar
        self.bar_group = form.findChild(QLabel,"barLabel")
        self.bar_group.setPixmap(self.bar)
        self.home_button = form.findChild(QPushButton,"homeButton")
        self.profile_button = form.findChild(QPushButton,"profileButton")
        self.faculties_button = form.findChild(QPushButton,"facultiesButton")
        self.majors_button = form.findChild(QPushButton,"majorsButton")
        self.course_button = form.findChild(QPushButton,"courseButton")
        self.other_button = form.findChild(QPushButton, "othersButton")

        #page properties
        self.home_button = form.findChild(QPushButton, "homeButton")
        self.status = form.findChild(QLabel,"status")
        self.course_code = form.findChild(QLineEdit,"courseCode")
        self.course_name = form.findChild(QLineEdit,"courseName")
        self.credits = form.findChild(QLineEdit,"credit")
        self.lecturer = form.findChild(QLineEdit,"lectName")
        self.period = form.findChild(QLineEdit,"period")
        self.year = form.findChild(QLineEdit,"year")
        self.term = form.findChild(QLineEdit,"term")
        self.faculty = form.findChild(QLineEdit,"faculty")
        self.major = form.findChild(QLineEdit,"major")
        self.student_limit = form.findChild(QLineEdit,"studentLimit")
        self.building = form.findChild(QLineEdit,"building")
        self.pre = form.findChild(QLineEdit, "pre")
        self.room = form.findChild(QLineEdit,"room")
        self.picture = form.findChild(QLabel,"picture")
        self.picture.setPixmap(self.edu_logo)

        self.save_button = form.findChild(QPushButton,"saveButton")
        self.clear_button = form.findChild(QPushButton,"clearButton")

        #Upper Bar pressed
        self.home_button.clicked.connect(self.goHome)
        self.faculties_button.clicked.connect(self.goFac)
        self.majors_button.clicked.connect(self.goMaj)
        self.other_button.clicked.connect(self.goOther)
        self.course_button.clicked.connect(self.goCourse)
        self.profile_button.clicked.connect(self.goProfile)

        #Internal Button Pressed
        self.save_button.clicked.connect(self.saveCourse)
        self.clear_button.clicked.connect(self.clearField)

    def goHome(self):
        self.parent.changePageLoginSection("home")

    def goProfile(self):
        self.parent.changePageLoginSection("profile")

    def goFac(self):
        self.parent.changePageLoginSection("addfaculties")

    def goMaj(self):
        self.parent.changePageLoginSection("addmajor")

    def goCourse(self):
        self.parent.changePageLoginSection("addcourse")

    def goOther(self):
        self.parent.changePageLoginSection("otherOption")
        
    ##Use to clear all textField##
    def clearField(self):
        self.course_code.setText("")
        self.course_name.setText("")
        self.credits.setText("")
        self.lecturer.setText("")
        self.period.setText("")
        self.year.setText("")
        self.term.setText("")
        self.faculty.setText("")
        self.major.setText("")
        self.student_limit.setText("")
        self.building.setText("")
        self.room.setText("")
        self.pre.setText("")

    ##Use for saving the course after enter Information##
    def saveCourse(self):
        temp = {}
        db = database.databaseCourse()
        temp["courseID"] = self.course_code.text()
        temp["courseName"] = self.course_name.text()
        temp["credit"] = self.credits.text()
        temp["lecturer"] = self.lecturer.text()
        temp["period"] = self.period.text()
        temp["year"] = self.year.text()
        temp["term"] = self.term.text()
        temp["facultyID"] = self.faculty.text()
        temp["majorID"] = self.major.text()
        temp["student_limit"] = self.student_limit.text()
        temp["building"] = self.building.text()
        temp["room"] = self.room.text()
        temp["pre"] = self.pre.text()
        status = db.addCourse(temp)
        if(status == 1):
            self.parent.showOK("Course Saved", "The course has been saved successfully")
            self.clearField()
        elif(status[0] == "22P02"):
            self.parent.showERROR("Data Integrity Error" + status[0] , "Invalid DataType or Incomplete Form.\nPlease check your fields.")
        elif(status[0] == "23505"):
            self.parent.showERROR("Data Duplication Error" + status[0], "CourseID already exists.")
        elif (status[0] == "23503"):
            self.parent.showERROR("Data Consistency Error" + status[0], "Either Professor ID, FacultyID, or Major ID is incorrect.")
