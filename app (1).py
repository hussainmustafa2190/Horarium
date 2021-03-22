from flask import Flask, render_template, request, url_for, flash, session, redirect
import pymysql
import os
app = Flask(__name__)
db = pymysql.connect("localhost","root","","htime")

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
            details = request.form
            email = details['email']
            password = details['password']
            cursor = db.cursor()
            if cursor.execute("SELECT email,password,authority FROM admin_reg WHERE email = %s and password = %s and authority = 1 ", (email,password)):
                return redirect(url_for('admindash'))

            elif cursor.execute("SELECT email,password,tauthority FROM tutor WHERE email = %s and password = %s and tauthority = 2 ", (email,password)):
                return render_template('/trainerdash')
            else:
                return render_template('/adminreg')
    else:
        return render_template('login.html', title = 'Login')

@app.route('/adminreg', methods=['POST','GET'])
def register():
    if request.method == 'POST':
            details = request.form
            institute = details['institute']
            admin = details['admin']
            email = details['email']
            password = details['password']
            institute_address = details['institute_address']
            phone = details['phone']
            authority = 1
            cursor = db.cursor()
            if cursor.execute("SELECT * FROM admin_reg WHERE institute = %s and authority = 1",institute):
                if cursor.fetchone() is not None:
                    return render_template('login.html', title = 'Register')
            else:
                cursor.execute("INSERT INTO admin_reg(institute,admin,email,password,institute_address,phone,authority) VALUES(%s, %s, %s, %s, %s, %s,%s)", (institute,admin,email,password,institute_address,phone,authority))
                db.commit()
                cursor.close()
                return redirect(url_for('login'))

    else:
        print("i am here in else")
        return render_template('adminreg.html', title = 'Admin Registration')


# @app.route('/adminlogin', methods=['POST','GET'])
# def adminlogin():
#     if request.method == 'POST':
#         try:
#             details = request.form
#             email = details['email']
#             password = details['password']
#             cursor = db.cursor()
#             cursor.execute("SELECT * FROM admin_reg WHERE email=%s and password=%s", (email, password))
#
#             if cursor.fetchone() is not None:
#                 # flash("Successfully Logged In !", "success")
#                 return redirect(url_for('admindash'))
#             else:
#                 flash("Incorrect email id or password", "danger")
#                 return redirect(url_for('adminlogin'))
#         except:
#             session['logged_in'] = True
#             session['email'] = email
#             cursor.close()
#             return redirect(url_for('adminlogin'))
#     else:
#         return render_template('adminlogin.html', title = 'Admin Login')

@app.route('/admindash')
def admindash():
    flash("Successfully Logged In !","success")
    return render_template('admindash.html', title='Admin')

@app.route('/bldgdetails', methods=['POST','GET'])
def bldgdetails():
    if request.method == 'POST':
        details = request.form
        building_name = details['building_name']
        building_number = details['building_number']
        number_of_floors = details['number_of_floors']
        number_of_labs = details['number_of_labs']
        number_of_class = details['number_of_class']
        cursor = db.cursor()
        cursor.execute("INSERT INTO buiild_detail(building_name,building_number,No_Of_Floors,No_Of_Labs,No_Of_Rooms) VALUES (%s,%s,%s,%s,%s) ",(building_name,building_number,number_of_floors,number_of_labs,number_of_class))
        db.commit()
        cursor.close()
        return render_template('admindash.html', title = 'Building Details')
    else:
        print("Is am in else")
        return render_template('bldgdetails.html', title = 'Building Details')


@app.route('/addnewdepart', methods=['POST','GET'])
def addnewdeparat():
    if request.method == 'POST':
            details = request.form
            department = details['department']
            semester = details['semester']
            start_day = details['start_day']
            end_day = details['end_day']
            cursor = db.cursor()
            cursor.execute("SELECT * FROM department WHERE Departments = %s and sem_no = %s", (department,semester))

            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO department(Departments,sem_no) VALUES(%s,%s)", (department, semester))
                db.commit()
                cursor.close()
                cursor = db.cursor()
                cursor.execute("INSERT INTO semester_timings(Semester_Start_DAY, Semester_End_DAY ) VALUES(%s,%s)", (start_day,end_day))
                # flash("Semester Successfully Entered !", "success")
                db.commit()
                cursor.close()
                return render_template('subjects.html', title = 'Subject', sem = semester)

            else:
                flash("Department already entered !", "danger")
                return redirect(url_for('addnewdepart'))
    else:
        print('pritam')
        return render_template('addnewdepart.html', title = 'Department')


@app.route('/trainerdash', methods=['POST','GET'])
def trainerdash():
    return render_template('trainerdash.html')



@app.route('/subjects', methods=['POST','GET'])
def addnewsubs():
    if request.method == 'POST':
        details = request.form
        subject = details['subject']
        loadhr = details['load_hour']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM subjects WHERE Subjects = %s and load_hour = %s", (subject, loadhr))

        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO subjects(Subjects, load_hour) VALUES(%s,%s)", (subject, loadhr))
            print("department")
            db.commit()
            cursor.close()
            return render_template('subjects.html', title = 'Subjects', sem = semester)
        else:
            return render_template('subjects.html')
    else:
        print("Else Part")
        return render_template('subjects.html', title='Subjects')

@app.route('/trainerreg', methods=['POST','GET'])
def trainer_reg():
    if request.method == 'POST':
        details = request.form
        Tutor_Name = details['Tutor_Name']
        Tutor_Id = details['Tutor_Id']
        email = details['email']
        password = details['password']
        phone = details['phone']
        Load_hour = details['Load_hour']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM   tutor WHERE  Tutor_Id = %s AND  password = %s", (Tutor_Id, password))
        if cursor.fetchone() is not None:
            return render_template('admindash.html', title='Trainer')
        else:
            cursor.execute("INSERT INTO tutor(Tutor_Name,Tutor_Id,email,password,phone,Load_hour,tauthority) VALUES(%s,%s,%s,%s,%s,%s,2)",(Tutor_Name, Tutor_Id, email, password, phone, Load_hour))
            db.commit()
            cursor.close()
            return render_template('trainerreg.html')
    else:
        print("ia m in trainer reg else")
        return render_template('trainerreg.html', title ='Trainer')

@app.route('/trainerlogin', methods=['POST','GET'])
def trainerlogin():
    if request.method == 'POST':
        details = request.form
        email = details['email']
        password = details['password']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tutor WHERE email=%s and password=%s", (email, password))

        if cursor.fetchone() is not None:
            #flash("Successfully Logged In !", "success")
            return redirect(url_for('trainerdash'))
        else:
            #flash("Incorrect email id or password", "danger")
            return render_template('trainerlogin.html')

    else:
        print("i am in this else")
        return render_template('trainerlogin.html', title='Admin Login')



# @app.route('/studentlogin')
# def data():
#     return render_template('students.html', title = 'Student Login')


@app.route('/timetable',methods=['POST','GET'])
def timetable():
    def take2(elem):
       return elem.priority
    class Teacher():
        def __init__(self, thours, tname):
            self.tname = tname
            self.thours = thours
            self.tpriority = thours

    class Subject:
        def __init__(self, name, lhs, teacher):
            self.name = name
            self.lhs = lhs
            self.priority = lhs
            self.teacher = teacher

        def __str__(self):
            return self.name + ":" + self.priority

        cursor = db.cursor()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 1 ")
        t1 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 2 ")
        t2 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 3 ")
        t3 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 4 ")
        t4 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 5 ")
        t5 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 6 ")
        t6 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 7 ")
        t7 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 8 ")
        t8 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 9 ")
        t9 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 10 ")
        t10 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 11  ")
        t11 = cursor.fetchone()
        cursor.execute("SELECT Tutor_Name FROM tutor WHERE ID = 12 ")
        t12 = cursor.fetchone()


        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 1 ")
        s1 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 2 ")
        s2 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 3 ")
        s3 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 4 ")
        s4 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 5 ")
        s5 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 6 ")
        s6 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 7 ")
        s7 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 8 ")
        s8 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 9 ")
        s9 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 10 ")
        s10 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 11 ")
        s11 = cursor.fetchone()
        cursor.execute("SELECT Subjects  FROM subjects WHERE Subject_Id = 12 ")
        s12 = cursor.fetchone()

        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 1 ")
        lhs1 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 2 ")
        lhs2 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 3 ")
        lhs3 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 4 ")
        lhs4 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 5 ")
        lhs5 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 6 ")
        lhs6 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 7 ")
        lhs7 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 8 ")
        lhs8 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 9 ")
        lhs9 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 10 ")
        lhs10 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 11 ")
        lhs11 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM subjects WHERE Subject_Id = 12 ")
        lhs12 = cursor.fetchone()

        cursor.execute("SELECT  load_hour FROM tutor WHERE ID = 1 ")
        lh1 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM tutor WHERE ID = 2 ")
        lh2 = cursor.fetchone()
        cursor.execute("SELECT  load_hour FROM tutor WHERE ID = 3 ")
        lh3 = cursor.fetchone()
        cursor.execute("SELECT  Load_hour FROM tutor WHERE ID = 4 ")
        lh4 = cursor.fetchone()
        cursor.execute("SELECT  Load_hour FROM tutor WHERE ID = 5 ")
        lh5 = cursor.fetchone()
        cursor.execute("SELECT  Load_hour FROM tutor WHERE ID = 6 ")
        lh6 = cursor.fetchone()
        cursor.execute("SELECT  Load_hour FROM tutor WHERE ID = 7 ")
        lh7 = cursor.fetchone()
        cursor.execute("SELECT  Load_hour FROM tutor WHERE ID = 8 ")
        lh8 = cursor.fetchone()
        cursor.execute("SELECT  Load_hour FROM tutor WHERE ID = 9 ")
        lh9 = cursor.fetchone()
        cursor.execute("SELECT  Load_hour FROM tutor WHERE ID = 10 ")
        lh10 = cursor.fetchone()
        cursor.execute("SELECT  Load_hour FROM tutor WHERE ID = 11 ")
        lh11 = cursor.fetchone()
        cursor.execute("SELECT  Load_hour FROM tutor WHERE ID = 12 ")
        lh12 = cursor.fetchone()
        print('BHAILOG DATABASE TOH BHARO')
        print('')
        print(lh1)
        print("aaaaaa")



    teacher1 = Teacher('lh1', 't1')
    teacher2 = Teacher('lh2', 't2')
    teacher3 = Teacher('lh3', 't3')
    teacher4 = Teacher('lh4', 't4')
    teacher5 = Teacher('lh5', 't5')
    teacher6 = Teacher('lh6', 't6')
    teacher7 = Teacher('lh7', 't7')
    teacher8 = Teacher('lh8', 't8')
    teacher9 = Teacher('lh9', 't9')
    teacher10 = Teacher('lh10', 't10')
    teacher11 = Teacher('lh11', 't11')
    teacher12 = Teacher('lh12', 't12')


    subject1 = Subject('s1',  'lhs1', teacher1)
    subject2 = Subject('s2',  'lhs2', teacher2)
    subject3 = Subject('s3',  'lhs3', teacher3)
    subject4 = Subject('s4',  'lhs4', teacher4)
    subject5 = Subject('s5',  'lhs5', teacher5)
    subject6 = Subject('s6',  'lhs6', teacher6)
    subject7 = Subject('s7',  'lhs7', teacher7)
    subject8 = Subject('s8',  'lhs8', teacher8)
    subject9 = Subject('s9',  'lhs9', teacher9)
    subject10 = Subject('s10',  'lhs10', teacher10)
    subject11 = Subject('s11',  'lhs11', teacher11)
    subject12 = Subject('s12',  'lhs12', teacher12)

    mylist = [subject1, subject2, subject3, subject4, subject5, subject6, subject7, subject8, subject9, subject10,
              subject11, subject12]
    mylist2 = [teacher1, teacher2, teacher3, teacher4, teacher5, teacher6, teacher7, teacher8, teacher9, teacher10,
               teacher11, teacher12]

    mylist = list(sorted(mylist, key=take2, reverse=True))

    class Day:
        def __init__(self):
            self.t1 = None
            self.t2 = None
            self.t3 = None
            self.t4 = None
            self.t5 = None
            self.t6 = None
            self.t7 = None
            self.slots = [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7]

        def __str__(self):
            for slot in self.slots:
                print(slot)
            return ''

    monday = Day()
    tuesday = Day()
    wednesday = Day()
    thursday = Day()
    friday = Day()
    saturday = Day()

    # MONDAY
    # subject logic

    for i in range(7):
        for element in mylist:
            if element.priority == 0:
                mylist.remove(element)
        monday.slots[i] = mylist[i % len(mylist)].name, mylist[i % len(mylist)].teacher.tname
        # print(monday.slots[i])
        mylist[i % len(mylist)].priority = int(mylist[i % len(mylist)].priority) - 1
        print("BBBBBBBBBBBBBBBB")
        mylist[i % len(mylist)].teacher.tpriority = mylist[i % len(mylist)].teacher.tpriority - 1

    timeslot = ['9-10', '10-11', '11-12', '12-13', '14-15', '15-16', '16-17']
    '''
    count2 = 0
    for slot in [timeslot, monday.slots]:
        count= 0
        if count2 == 0:
            print("Time", end='\t')
            count2 = count2 + 1
        elif count2 == 1:
            print("MON", end='\t')
            count2 = 0
        else:
            pass
        for slot2 in slot:
            if count!=6:
                print(slot2, end='\t')
                count = count + 1 
            else:
                print(slot2, end='\t')
                print('\n')
    '''

    # TUESDAY

    # print(mylist)
    for element in mylist:
        if element.priority == 0:
            mylist.remove(element)

    for i in range(7):
        tuesday.slots[i] = mylist[i % len(mylist)].name, mylist[i % len(mylist)].teacher.tname

        # print(monday.slots[i])
        mylist[i % len(mylist)].priority = mylist[i % len(mylist)].priority - 1
        mylist[i % len(mylist)].teacher.tpriority = mylist[i % len(mylist)].teacher.tpriority - 1

    '''
    for slot in [tuesday.slots]:
        count= 0

        if count2 == 0:
            print("TUE", end='\t')
            count2 = 0 
        else:
            pass
        for slot2 in slot:
            if count!=6:
                print(slot2, end='\t')
                count = count + 1 
            else:
                print(slot2, end='\t')
                print('\n')
    '''

    # WEDNESDAY

    for i in range(7):
        for element in mylist:
            if element.priority == 0:
                mylist.remove(element)
        wednesday.slots[i] = mylist[i % len(mylist)].name, mylist[i % len(mylist)].teacher.tname
        # print(monday.slots[i])
        mylist[i % len(mylist)].priority = mylist[i % len(mylist)].priority - 1
        mylist[i % len(mylist)].teacher.tpriority = mylist[i % len(mylist)].teacher.tpriority - 1

    '''
    for slot in [wednesday.slots]:
        count= 0

        if count2 == 0:
            print("WED", end='\t')
            count2=0
        else:
            pass
        for slot2 in slot:
            if count!=6:
                print(slot2, end='\t')
                count = count + 1 
            else:
                print(slot2, end='\t')
                print('\n')
    '''

    # THURSDAY

    for i in range(7):
        for element in mylist:
            if element.priority == 0:
                mylist.remove(element)

        thursday.slots[i % len(mylist)] = mylist[i % len(mylist)].name, mylist[i % len(mylist)].teacher.tname

        # print(monday.slots[i])
        mylist[i % len(mylist)].priority = mylist[i % len(mylist)].priority - 1
        mylist[i % len(mylist)].teacher.tpriority = mylist[i % len(mylist)].teacher.tpriority - 1

    '''    
    for slot in [thursday.slots]:
        count= 0

        if count2 == 0:
            print("THU", end='\t')
            count2=0
        else:
            pass
        for slot2 in slot:
            if count!=6:
                print(slot2, end='\t')
                count = count + 1 
            else:
                print(slot2, end='\t')
                print('\n')

    '''

    # FRIDAY

    for i in range(7):
        for element in mylist:
            if element.priority == 0:
                mylist.remove(element)

        friday.slots[i] = mylist[i % len(mylist)].name, mylist[i % len(mylist)].teacher.tname

        # print(monday.slots[i])
        mylist[i % len(mylist)].priority = mylist[i % len(mylist)].priority - 1
        mylist[i % len(mylist)].teacher.tpriority = mylist[i % len(mylist)].teacher.tpriority - 1

    '''
    for slot in [friday.slots]:
        count= 0

        if count2 == 0:
            print("FRI", end='\t')
            count2=0
        else:
            pass
        for slot2 in slot:
            if count!=6:
                print(slot2, end='\t')
                count = count + 1 
            else:
                print(slot2, end='\t')
                print('\n')                     
    '''

    days_slots = [monday, tuesday, wednesday, thursday, friday]

    '''for slot in days_slots:
        print(slot)

    '''

    '''
    Print remaining Load Hours
    for subject in mylist:
        print(subject.priority)
    print("a")
    for t in mylist2:
        print(t.thours-t.tpriority)
    '''
    #monday_slots = [monday.t1, monday.t2, monday.t3, monday.t4, monday.t5, monday.t6, monday.t7, ]
    #print(days_slots[1].slots[0])
    return render_template('timetable.html', posts=days_slots)

# @app.route('/register', methods=['POST', 'GET'])
# def register():
#    if request.method == 'POST':
#        details = request.form
#        email = details['email']
#        password = details['password']
#        cursor = db.cursor()
#        cursor.execute("INSERT INTO users(email, password) VALUES(%s, %s)", (email, password))
#        db.commit()
#        cursor.close()
#        return "OVER"
#     else:

@app.route('/timetable2')
def timetable2():
    return render_template('timetable2.html')



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
