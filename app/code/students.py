from app import *

#####################     Student login  ####################################################

@app.route("/student",methods=["POST", "GET"])
def student_login():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'pwd' in request.form:
        msg = ''
        username=request.form['username']
        pwd=request.form['pwd']
        status='yes'
        find = ['@']
        query=''

        results = [item for item in find if item in username]

        if (results):

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute('select * from student_details where student_password=%s  and account_status =%s and student_email =%s', (pwd,status, username))
            student = cursor.fetchone()

            session['student_id'] = student['student_id']
            session['user_type']='student'


            if student:
                return redirect(url_for('home'))
            else:
                return render_template('students/login.html', msg='Invalid Credentials/ Account not Verified')
        else:

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from student_details where student_password=%s  and account_status =%s and student_contact =%s',(pwd, 'yes', username))
            student = cursor.fetchone()
            session['student_id'] = student['student_id']
            if student:
                return redirect(url_for('home'))
            else:
                return render_template('students/login.html', msg='Invalid Credentials/ Account not Verified')






    if (not session.get("student_id") is None):
        if (session.get("user_type") == 'student'):
            return redirect(url_for('home'))

    return render_template('students/login.html',msg='')

################################################### Student Register ##############################################################

@app.route("/student/register",methods=["POST", "GET"])
def student_register():
    msg=''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from school_details')
    school_details=cursor.fetchall()

    cursor.execute('select student_email from student_details')
    student = cursor.fetchall()
    print(student)
    if request.method == 'POST':
        username=request.form['username']
        email=request.form['email']
        mobile=request.form['mobile']
        grade=request.form['grade']
        whatsapp=request.form['whatsapp']
        #state1=request.form['state1']
        #district1=request.form['district1']
        #board=request.form['board']
        f = request.files['file']

        school_name=request.form['school_name']


        password=request.form['password']


        cursor.execute('select * from student_details where student_email=%s ',[email])
        student=cursor.fetchone()
        if student:
            return render_template('students/register.html', school_details=school_details,msg='Account Already exists')


        else:
            cursor.execute ('select school_id from school_details where school_name =%s',[school_name])
            school=cursor.fetchone()


            basepath = os.path.dirname(__file__)
            #file_path = os.path.join(basepath, secure_filename(f.filename))

            f.save(os.path.join(app.root_path, 'static/img/id_images/{0}-{1}.png'.format(username,mobile)))
            student_id= "img/id_images/{0}-{1}".format(username,mobile)

            cursor.execute('insert into student_details (student_name ,student_contact, student_email,student_grade,student_whatsapp,student_password,school_id,account_status,student_idcard) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(username,mobile,email,grade,whatsapp,password,school['school_id'],'No',student_id) )
            mysql.connection.commit()
            return render_template('students/register.html', school_details=school_details,msg='Registered Successfuly Check email/message for verification we will get you soon ')



    return render_template('students/register.html',school_details=school_details,msg='',student=student)


#########################################Student school register #############################################
@app.route("/student/school_register",methods=["POST", "GET"])
def student_school_register():
    msg=''
    if request.method == 'POST':
        schoolname=request.form['schoolname']
        state=request.form['state']
        district=request.form['district']
        board=request.form['board']
        pin=request.form['pin']
        phone=request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into school_details (school_name,school_state,school_district,school_board,school_pincode,school_contact,school_status) values(%s,%s,%s,%s,%s,%s,%s)',(schoolname,state,district,board,pin,phone,'No'))
        mysql.connection.commit()
        return render_template('students/register_school.html',msg='Registered successfully soon it will be added ')

    return render_template('students/register_school.html',msg=msg)


##################################   Student dashboard ########################################################################
@app.route("/student/home",methods=["POST", "GET"])
def home():
    if 'student_id' in session and session.get("user_type") == 'student':
        id=session.get('student_id')
        if request.method =='POST':
           filter_subject=tuple(request.form.getlist('filter_subject'))

           cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
           cursor.execute('select distinct subject.subject_name,subject.subject_id ,course_details.course_id,course_details.course_name,course_details.course_description,course_details.no_of_session,course_details.course_status from subject,course_details where course_details.subject_id and subject.subject_id in %s and course_details.subject_id=subject.subject_id',[filter_subject])
           courses = cursor.fetchall()

           cursor.execute('select * from subject')
           subject = cursor.fetchall()

           cursor.execute('select * from student_details where student_id=%s ',[id])
           student=cursor.fetchone()

           cursor.execute('select * from course_enroll_details where student_id=%s',[id])
           mycourse = cursor.fetchall()
           my_course=[]
           for i in range(len(mycourse)):
               my_course.append(mycourse[i]['course_id'])
           print(my_course)
           return render_template('students/home.html', courses=courses, len=len(courses), subject=subject,student=student,my_course=my_course)




        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select subject.subject_name,subject.subject_id ,course_details.course_id,course_details.course_name,course_details.course_description,course_details.no_of_session,course_details.course_status from subject,course_details where subject.subject_id=course_details.subject_id ')
            courses=cursor.fetchall()
            print(courses)
            cursor.execute('select * from subject')
            subject=cursor.fetchall()

            cursor.execute('select * from student_details where student_id=%s ', [id])
            student = cursor.fetchone()

            cursor.execute('select * from course_enroll_details where student_id=%s', [id])
            mycourse = cursor.fetchall()
            my_course = []
            for i in range(len(mycourse)):
                my_course.append(mycourse[i]['course_id'])
            print(my_course)
            return render_template('students/home.html', courses=courses, len=len(courses), subject=subject,student=student, my_course=my_course)

    else:
        return redirect(url_for('student_login'))



############################################ Student_profile #########################################################
@app.route("/student/profile",methods=["POST", "GET"])
def student_profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'student_id' in session and session.get("user_type") == 'student':
        if request.method =='POST':
            username=request.form['username']
            mobile=request.form['mobile']
            whatsapp=request.form['whatsapp']

            cursor.execute('update student_details set student_name=%s,student_contact=%s,student_whatsapp=%s',(username,mobile,whatsapp))
            mysql.connection.commit()



        id = session.get('student_id')
        cursor.execute('select * from student_details where student_id=%s ', [id])
        student = cursor.fetchone()
        school_id=student['school_id']


        cursor.execute('select * from school_details where school_id=%s ', [school_id])
        school=cursor.fetchone()

        return render_template('students/student_profile.html',student=student,school=school)
    else:
        return redirect(url_for('student_login'))


########################## change profile photo ######################################
@app.route("/student/profile_photo",methods=["POST", "GET"])
def change_photo():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'student_id' in session and session.get("user_type") == 'student' and request.method=='POST':

        id = session.get('student_id')




        f = request.files['change_profile']
        path = "static/img/profile_images/{0}.png".format(id)
        f.save(os.path.join(app.root_path, path))
        path="img/profile_images/{0}.png".format(id)


        cursor.execute('update student_details set student_profile=%s WHERE student_id  = %s', (path, id))
        mysql.connection.commit()
        flash("Profile Image Updated Successfully!")
        return redirect(url_for('student_profile'))

    else:
        return redirect(url_for('student_login'))

########################## My courses ######################################
@app.route("/student/my_courses",methods=["POST", "GET"])
def my_courses():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'student_id' in session and session.get("user_type") == 'student':
        id = session.get('student_id')
        cursor.execute('select * from student_details where student_id=%s ', [id])
        student = cursor.fetchone()




        cursor.execute('select subject.subject_name,subject.subject_id,course_details.course_id,course_details.course_name,course_details.course_description,course_details.no_of_session,course_details.course_status,course_enroll_details.course_id from course_details, course_enroll_details,subject where course_details.course_id=course_enroll_details.course_id and subject.subject_id=course_details.subject_id and  course_enroll_details.student_id=%s',[id])
        mycourse=cursor.fetchall()
        return render_template("/students/mycourses.html",mycourse=mycourse,student=student,len=len(mycourse))
    else:
        return redirect(url_for('student_login'))

############################## Add courses ############################################
@app.route("/student/add_courses",methods=["POST", "GET"])
def add_courses():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'student_id' in session and session.get("user_type") == 'student':
        id = session.get('student_id')

        course_id = request.args.get('a')
        print(course_id)
        cursor.execute('insert into course_enroll_details (course_id,student_id) values(%s,%s)', (course_id, id))
        mysql.connection.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('student_login'))



######################################## logout #######################################################
@app.route('/student_logout')
def student_logout():
    session.clear()
    return redirect(url_for('student_login'))



