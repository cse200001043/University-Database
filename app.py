from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mayank.123@localhost/faculty'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Admin(db.Model):
    User_id = db.Column(db.Integer, primary_key=True)
    User_name = db.Column(db.String(25), nullable=False)
    Password = db.Column(db.String(25), nullable=False)

class Department(db.Model):
    Department_id = db.Column(db.Integer, primary_key=True)
    Department_name = db.Column(db.String(50), nullable=False)

class Professor(db.Model):
    Professor_id = db.Column(db.Integer, primary_key=True)
    Professor_name = db.Column(db.String(50), nullable=False)
    Department_id = db.Column(db.Integer, db.ForeignKey('department.Department_id'))

class Course(db.Model):
    Course_id = db.Column(db.Integer, primary_key=True)
    Course_code = db.Column(db.String(15), nullable=False)
    Course_name = db.Column(db.String(50), nullable=False)
    Room_no = db.Column(db.String(15), nullable=False)
    No_of_students_registered = db.Column(db.Integer, nullable=False)
    Department_id = db.Column(db.Integer, db.ForeignKey('department.Department_id'))
    Professor_id = db.Column(db.Integer, db.ForeignKey('professor.Professor_id'))
    Semester = db.Column(db.String(20), nullable=False)

class Timetable(db.Model):
    Course_id = db.Column(db.Integer, db.ForeignKey('course.Course_id'), primary_key=True)
    Monday = db.Column(db.String(15))
    Tuesday = db.Column(db.String(15))
    Wednesday = db.Column(db.String(15))
    Thursday = db.Column(db.String(15))
    Friday = db.Column(db.String(15))
    Saturday = db.Column(db.String(15))




@app.route('/')
def login():
    flash('You are already registered. Please login!')
    return render_template('admin-login.html')

@app.route('/register')
def register():
    return render_template('admin-register.html')

@app.route('/department')
def department():
    return render_template('add-department.html')

@app.route('/professor')
def professor():
    return render_template('add-professor.html')

@app.route('/course')
def course():
    return render_template('add-course.html')

@app.route('/choose')
def choose():
    return render_template('choose.html')

@app.route('/chooseadd')
def chooseadd():
    return render_template('chooseadd.html')

@app.route('/choosefind')
def choosefind():
    return render_template('choosefind.html')





@app.route('/register1', methods = ['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        password = request.form.get('password')

        user = Admin.query.filter_by(User_id=user_id).first()

        if user:
            return "Sorry this Email is already registered !"
            return redirect('/register')

        entry = Admin(User_id=user_id, User_name=user_name, Password=password)
        db.session.add(entry)
        db.session.commit()

    return redirect('/choose')


@app.route('/1', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')

        user = Admin.query.filter_by(User_id=user_id).first()

        if not user:
            return "You are not registered !"
            return redirect('/register')

        user_pass = Admin.query.filter_by(User_id=user_id, Password=password).first()
         
        if not user_pass:
            return "You entered wrong password"
            return redirect('/')

        return redirect('/choose')
        

@app.route('/adddepartment', methods = ['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        department_id = request.form.get('department_id')
        department_name = request.form.get('department_name')

        department = Department.query.filter_by(Department_id=department_id).first()
        
        if department:
            return "Sorry the department is already registered !"
            return redirect('/department')

        entry = Department(Department_id=department_id, Department_name=department_name)
        db.session.add(entry)
        db.session.commit()

        return "Your change was successful !"

    return redirect('/department')


@app.route('/addprofessor', methods = ['GET', 'POST'])
def add_professor():
    if request.method == 'POST':
        professor_id = request.form.get('professor_id')
        professor_name = request.form.get('professor_name')
        department_name = request.form.get('department_name')

        professor = Professor.query.filter_by(Professor_id=professor_id).first()

        if professor:
            return "Sorry the professor is already registered !"
            return redirect('/professor')

        dep = Department.query.filter_by(Department_name=department_name).first()
        dep_id = dep.Department_id

        entry = Professor(Professor_id=professor_id, Professor_name=professor_name, Department_id=dep_id)
        db.session.add(entry)
        db.session.commit()

        return "Your change was successful !"

    return redirect('/professor')


@app.route('/addcourse', methods = ['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        course_code = request.form.get('course_code')
        course_name = request.form.get('course_name')
        room_no = request.form.get('room_no')
        no_of_students_registered = request.form.get('no_of_students_registered')
        department_name = request.form.get('department_name')
        professor_name = request.form.get('professor_name')
        semester = request.form.get('semester')
        monday = request.form.get('monday')
        tuesday = request.form.get('tuesday')
        wednesday = request.form.get('wednesday')
        thursday = request.form.get('thursday')
        friday = request.form.get('friday')
        saturday = request.form.get('saturday')

        course = Course.query.filter_by(Course_id=course_id).first()

        if course:
            return "Sorry the Course id is already registered !"
            return redirect('/course')

        dep = Department.query.filter_by(Department_name=department_name).first()
        dep_id = dep.Department_id

        pro = Professor.query.filter_by(Professor_name=professor_name).first()
        pro_id = pro.Professor_id





        entry1 = Course(Course_id=course_id, Course_code=course_code, Course_name=course_name, Room_no=room_no, No_of_students_registered=no_of_students_registered, Department_id=dep_id,  Professor_id=pro_id, Semester=semester)
        db.session.add(entry1)
        db.session.commit()

        entry2 = Timetable(Course_id=course_id, Monday=monday, Tuesday=tuesday, Wednesday=wednesday, Thursday=thursday, Friday=friday, Saturday=saturday)
        db.session.add(entry2)
        db.session.commit()

        return "Your change was successful !"


    return redirect('/course')

@app.route('/finddepartment')
def finddepartment():
    dep = Department.query.filter_by().all()
    return render_template('finddepartment.html', dep=dep)

@app.route('/findcourse')
def findcourse():
    dep = Department.query.filter_by().all()
    prop = Professor.query.filter_by().all()
    return render_template('findcourse.html', dep=dep, prop=prop)

@app.route('/findprofessor')
def findprofessor():
    dep = Department.query.filter_by().all()
    course = Course.query.filter_by().all()
    return render_template('findprofessor.html', dep=dep, course=course)

@app.route('/findcourse1', methods = ['GET', 'POST'])
def findcourse1():
    if request.method == 'POST':
        department_name = request.form.get('department_name')
        professor_name = request.form.get('professor_name')
        semester = request.form.get('semester')

        dep = Department.query.filter_by(Department_name=department_name).first()
        dep_id = dep.Department_id

        pro = Professor.query.filter_by(Professor_name=professor_name).first()
        pro_id = pro.Professor_id

        course = Course.query.filter_by(Professor_id=pro_id, Department_id=dep_id, Semester=semester).all()

        if not course:
            return "No such course exists !"
            return redirect('/findcourse')

        return render_template('display-course.html', course=course)
    
    return redirect('findcourse')


@app.route('/findprofessor1', methods = ['GET', 'POST'])
def findprofessor1():
    if request.method == 'POST':
        department_name = request.form.get('department_name')
        course_name = request.form.get('course_name')
        semester = request.form.get('semester')

        dep = Department.query.filter_by(Department_name=department_name).first()
        dep_id = dep.Department_id

        # pro = Professor.query.filter_by(Professor_name=professor_name).first()
        # pro_id = pro.Professor_id

        professor = Course.query.filter_by(Course_name=course_name, Department_id=dep_id, Semester=semester).all()

        if not professor:
            return "No such professor exists !"
            return redirect('/findprofessor')

        professor1 = []

        for x in professor:
            professor1 += Professor.query.filter_by(Professor_id=x.Professor_id).all()

        return render_template('display-professor.html', professor=professor1)
    
    return redirect('findprofessor')


    # dep = Department.query.filter_by().all()
    # prop = Professor.query.filter_by().all()
    # return render_template('finddepartment.html', dep=dep, prop=prop)








if __name__ =='__main__':
    app.run(debug=True)