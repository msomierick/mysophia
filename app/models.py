from .import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .import login_manager
# Configure and initialize SQLAlchemy under this Flask webapp.
# join table between collegeprogram and college_course: giving us the
# common courses
collegeprogram_collegecourse = db.Table('collegeprogram_collegecourse',
                                        db.Column(
                                            'collegeprogram_id', db.Integer, db.ForeignKey('college_program.id')),
                                        db.Column(
                                            'collegecourse_id', db.Integer, db.ForeignKey('college_course.id'))
                                        )

# join table between student and college_course
student_collegecourse = db.Table('student_collegecourse',
                                 db.Column(
                                     'student_id', db.Integer, db.ForeignKey('student.id')),
                                 db.Column(
                                     'collegecourse_id', db.Integer, db.ForeignKey('college_course.id'))
                                 )


class Student(UserMixin, db.Model):
    '''
    This class holds all the important info for the student.
    '''

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_no = db.Column(db.String(20), nullable=False, unique=True)
    surname = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    second_name = db.Column(db.String(20))
    email = db.Column(db.String(50))  # Rem to check for the emailfield
    # is_class_rep = db.Column(db.Boolean, default=False): Lets have this in the program
    phone_no = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128))
    collegeprogram_id = db.Column(db.Integer, db.ForeignKey(
        'college_program.id'))  # A backref called 'collegeprogram' is defined in 'CollegeProgram'

    def __repr__(self):
        return "<Student(%d, %s %s %s)>" % (
            self.id, self.surname, self.first_name, self.second_name)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Lecturer(db.Model):
    '''
    This class holds all the important info for the lecturer
    '''

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    salutation = db.Column(db.Enum(
        'Mr', 'Mrs', 'Miss', 'Dr', 'Prof' 'Eng', name='salutations'), nullable=False, default='Dr')
    surname = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    second_name = db.Column(db.String(20))
    email = db.Column(db.String(50))  # Rem to check for the emailfield
    phone_no = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.String(50))

    collegedepart_id = db.Column(
        db.Integer, db.ForeignKey('college_department.id'))

    # many to one: courses taught by this lecturer
    courses = db.relationship(
        'CollegeCourse', backref='lecturer', lazy='dynamic')


class CollegeCourse(db.Model):
    '''
    This class holds all the important info for the college course
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(10))
    course_name = db.Column(db.String(50))
    course_year = db.Column(db.Integer())

    # the lecturer who teaches this course
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))

    def __repr__(self):
        return "<College Course(%d, %s, %d year)>" % (
            self.id, self.course_name, self.course_year)


class CollegeProgram(db.Model):
    '''
    This class holds all the important info for the college program: eg BCOM, BSc, Dip, Cert etc
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_type = db.Column(db.Enum(
        'Diploma', 'Degree', 'Masters', 'PhD', name='degree_types'), nullable=False, default='Degree')
    program_name = db.Column(db.String(50))
    program_code = db.Column(db.String(10))
    program_abrv = db.Column(db.String(10))  # eg BSc, BCom, Bed etc

    # one to many with student
    students = db.relationship(
        'Student', backref='college_program', lazy='dynamic')

    # class rep
    # class_rep_id = db.Column(db.Integer, db.ForeignKey('student.id'))  # the
    # student/class rep of this program of the program

    # many to one with department
    collegedepart_id = db.Column(
        db.Integer, db.ForeignKey('college_department.id'))

    # the lecturer in charge of the program
    program_coord_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))

    def __repr__(self):
        return "<College Program(%d, %s %s %s)>" % (
            self.id, self.program_code, self.program_abrv, self.program_name)


class CollegeDepartment(db.Model):
    '''
    This class holds all the important info for the college department
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_name = db.Column(db.String(80))

    # one to many with collegeprogram
    programs = db.relationship(
        'CollegeProgram', backref='college_department', lazy='dynamic')

    # many to one with college faculty
    collegefaculty_id = db.Column(
        db.Integer, db.ForeignKey('college_faculty.id'))

    # the head of department
   # hod_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))

    # the lecturers belonging to this department
    lecturers = db.relationship(
        'Lecturer', backref='college_department', lazy='dynamic')

    def __repr__(self):
        return "<College Department(%d, %s)>" % (
            self.id, self.dept_name)


class CollegeFaculty(db.Model):
    '''
    This class holds all the important info for the college faculty/school
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    faculty_name = db.Column(db.String(80))

    # the dean of this faculty
    # dean_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))

    # one to many with collegedepartment
    db.relationship(
        'CollegeDepartment', backref='college_faculty', lazy='dynamic')

    def __repr__(self):
        return "%s" % self.faculty_name

# the class representatative
class ProgramRep(db.Model):
    dept_id = db.Column(
        db.Integer, db.ForeignKey('college_department.id'), primary_key=True)
    classrep_id = db.Column(
        db.Integer, db.ForeignKey('student.id'), primary_key=True)
    date_began = db.Column(db.Date)
    date_ended = db.Column(db.Date)

# the head of department
class HOD(db.Model):
    __tablename__ = 'hod'
    dept_id = db.Column(
        db.Integer, db.ForeignKey('college_department.id'), primary_key=True)
    hod_id = db.Column(
        db.Integer, db.ForeignKey('lecturer.id'), primary_key=True)
    date_began = db.Column(db.Date)
    date_ended = db.Column(db.Date)

# the dean of school/faculty
class Dean(db.Model):
    faculty_id = db.Column(
        db.Integer, db.ForeignKey('college_faculty.id'), primary_key=True)
    dean_id = db.Column(
        db.Integer, db.ForeignKey('lecturer.id'), primary_key=True)
    date_began = db.Column(db.Date)
    date_ended = db.Column(db.Date)


@login_manager.user_loader
def load_user(email):
    return Student.query.get(email)

#================QUERIES=================
def get_students():
    return Student.query.all()


def get_faculties():
    return CollegeFaculty.query.all()
