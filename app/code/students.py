from app import *
#####################   Student Home ####################################################
@app.route("/student",methods=["POST", "GET"])
def student_home():
    return render_template('students/index.html', msg='')

#####################     Student login  ####################################################



@app.route("/student_login",methods=["POST", "GET"])
def student_login():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'pwd' in request.form:
        msg = ''
        username=request.form['username']

        passwd=request.form['pwd']
        password = hashlib.md5(passwd.encode())
        pwd=password.hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from student_details where student_password=%s and account_status =%s and student_contact =%s or student_email =%s',(pwd,'allow',username,username))
        student = cursor.fetchone()

        status='allow'
        find = ['@']
        query=''

        results = [item for item in find if item in username]

        if (results):

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute('select * from student_details where student_password=%s  and account_status =%s and student_email =%s', (pwd,status, username))
            student = cursor.fetchone()




            if student:
                session['student_id'] = student['student_id']
                session['user_type'] = 'student'
                return redirect(url_for('home'))
            else:
                return render_template('students/login.html', msg='error')

        else:

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from student_details where student_password=%s  and account_status =%s and student_contact =%s',(pwd, 'allow', username))
            student = cursor.fetchone()
            session['student_id'] = student['student_id']
            if student:
                return redirect(url_for('home'))
            else:
                return render_template('students/login.html', msg='error')






    if (not session.get("student_id") is None):
        if (session.get("user_type") == 'student'):
            return redirect(url_for('home'))

    return render_template('students/login.html', msg='')

################################################### Student Register ##############################################################

@app.route("/student/register",methods=["POST", "GET"])
def student_register():
    msg=''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from school_details')
    school_details=cursor.fetchall()
    cursor.execute('select student_email from student_details')
    student = cursor.fetchall()
    if request.method == 'POST':
        username=request.form['username']
        emails=request.form['email']
        mobile=request.form['mobile']
        grade=request.form['grade']
        whatsapp=request.form['whatsapp']
        #state1=request.form['state1']
        #district1=request.form['district1']
        #board=request.form['board']
        f = request.files['file']

        school_name=request.form['school_name']


        passwd=request.form['password']
        passd = hashlib.md5(passwd.encode())
        password=passd.hexdigest()


        cursor.execute('select * from student_details where student_email=%s ',[emails])

        student=cursor.fetchone()
        if student:
            return render_template('students/register.html', school_details=school_details,msg='error')


        else:
            cursor.execute ('select school_id from school_details where school_name =%s',[school_name])
            school=cursor.fetchone()

            cursor.execute('select * from email_content where emailc_id =1') # student register id
            email_mail = cursor.fetchone()
            subject = email_mail['email_subject']
            message = email_mail['email_message']

            a=email(emails,subject,message)

            basepath = os.path.dirname(__file__)
            #file_path = os.path.join(basepath, secure_filename(f.filename))

            f.save(os.path.join(app.root_path, 'static/img/id_images/{0}-{1}.png'.format(username,mobile)))
            student_id= "img/id_images/{0}-{1}.png".format(username,mobile)

            cursor.execute('insert into student_details (student_name ,student_contact, student_email,student_grade,student_whatsapp,student_password,school_id,account_status,student_idcard) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(username,mobile,emails,grade,whatsapp,password,school['school_id'],'waiting',student_id) )

            mysql.connection.commit()
            
            return render_template('students/register.html', school_details=school_details,msg='success')



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
        cursor.execute('insert into school_details (school_name,school_state,school_district,school_board,school_pincode,school_contact,school_status) values(%s,%s,%s,%s,%s,%s,%s)',(schoolname,state,district,board,pin,phone,'notapproved'))
        mysql.connection.commit()
        return render_template('students/register_school.html',msg='Registered successfully soon it will be added ')

    return render_template('students/register_school.html',msg=msg)


##################################   Student dashboard ########################################################################
@app.route("/student/home",methods=["POST", "GET"])
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'student_id' in session and session.get("user_type") == 'student':
        id=session.get('student_id')
        if request.method =='POST':
           filter_subject=request.form['subject']
           status=request.form['status']
           print(filter_subject)
           print(status)
           if status =='all' and filter_subject =='all':
               cursor.execute('select subject.subject_name,subject.subject_id ,course_details.course_id,course_details.course_duration,course_details.course_name,course_details.course_description,course_details.no_of_session,course_details.course_status from subject,course_details where subject.subject_id=course_details.subject_id and course_details.course_approval_status="approved"')
               courses = cursor.fetchall()
               current=['All','All']
           elif status =='all' and filter_subject!='all':
               print('hi')
               cursor.execute('select distinct subject.subject_name,subject.subject_id ,course_details.course_id,course_details.course_duration,course_details.course_name,course_details.course_description,course_details.no_of_session,course_details.course_status from subject,course_details where course_details.subject_id and subject.subject_id = %s and course_details.subject_id=subject.subject_id  and course_details.course_approval_status="approved"',[filter_subject])
               courses = cursor.fetchall()
               current = [courses[0]['subject_name'], 'All']
           elif status !='all' and filter_subject=='all':
               cursor.execute('select subject.subject_name,subject.subject_id,course_details.course_id,course_details.course_name,course_details.course_description,course_details.no_of_session,course_details.course_status,course_enroll_details.course_id from course_details, course_enroll_details,subject where course_details.course_id=course_enroll_details.course_id and subject.subject_id=course_details.subject_id and  course_enroll_details.student_id=%s',[id])
               courses = cursor.fetchall()
               current = ['All', 'Enrolled']

           else:
               cursor.execute('select subject.subject_name,subject.subject_id,course_details.course_id,course_details.course_name,course_details.course_description,course_details.no_of_session,course_details.course_status,course_enroll_details.course_id from course_details, course_enroll_details,subject where course_details.course_id=course_enroll_details.course_id and subject.subject_id=course_details.subject_id and  course_enroll_details.student_id=%s and subject.subject_id = %s  and course_details.course_approval_status="approved"',(id,filter_subject))
               courses = cursor.fetchall()
               print(courses)
               if courses:
                current = [courses[0]['subject_name'], 'Enrolled']
               current=['None','None']



           cursor.execute('select * from subject')
           subject = cursor.fetchall()

           cursor.execute('select * from student_details where student_id=%s ',[id])
           student=cursor.fetchone()

           cursor.execute('select * from course_enroll_details where student_id=%s',[id])
           mycourse = cursor.fetchall()
           my_course=[]
           for i in range(len(mycourse)):
               my_course.append(mycourse[i]['course_id'])

           return render_template('students/home.html', courses=courses,current=current, len=len(courses), subject=subject,student=student,my_course=my_course)




        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select subject.subject_name,subject.subject_id ,course_details.course_id,course_details.course_duration,course_details.course_name,course_details.course_description,course_details.no_of_session,course_details.course_status from subject,course_details where subject.subject_id=course_details.subject_id and course_details.course_approval_status="approved" ')
            courses=cursor.fetchall()

            cursor.execute('select * from subject')
            subject=cursor.fetchall()

            cursor.execute('select * from student_details where student_id=%s ', [id])
            student = cursor.fetchone()

            cursor.execute('select * from course_enroll_details where student_id=%s', [id])
            mycourse = cursor.fetchall()
            my_course = []
            for i in range(len(mycourse)):
                my_course.append(mycourse[i]['course_id'])
            current=['All','All'] # subject and enrollement status

            return render_template('students/home.html', courses=courses, len=len(courses), subject=subject,student=student,current=current ,my_course=my_course)

    else:
        return redirect(url_for('student_login'))



############################################ Student_profile #########################################################
@app.route("/student/profile",methods=["POST", "GET"])
def student_profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'student_id' in session and session.get("user_type") == 'student':
        id = session.get('student_id')
        if request.method =='POST':
            username=request.form['username']
            mobile=request.form['mobile']
            whatsapp=request.form['whatsapp']

            cursor.execute('update student_details set student_name=%s,student_contact=%s,student_whatsapp=%s where student_id=%s',(username,mobile,whatsapp,id))
            mysql.connection.commit()
            return redirect(url_for('student_profile'))




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
        return redirect(url_for('home'))

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



######################################## student_forget_password #######################################################


@app.route("/student/forget_password",methods=["POST", "GET"])
def student_forget_password():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method=='POST':
        emailid=request.form['username']

        cursor.execute('select * from student_details where student_email=%s and account_status="allow"',[emailid])
        student=cursor.fetchone()
        if student:
            message_bytes = emailid.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            mail = base64_bytes.decode('ascii')

            cursor.execute('select * from email_content where emailc_id = 4')
            email_mail = cursor.fetchone()
            subject = email_mail['email_subject']
            message = email_mail['email_message']

            message=message+": <a href='http://127.0.0.1:5000/student/forget_password/verify?code={0}'</a>click here </a>".format(mail)
            print(message)
            email(emailid,subject,message)

            return render_template('/students/forget_password.html',msg='success')


        else:
            return render_template('/students/forget_password.html',msg='error')

    return render_template('/students/forget_password.html',msg='')





######################################## student_forget_password change password #######################################################


@app.route("/student/forget_password/verify",methods=["POST", "GET"])
def student_forget_password_verify():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method=='POST':
        password=request.form['password']
        email=request.form['email']
        passwd = hashlib.md5(password.encode())
        pwd=passwd.hexdigest()
        
        print(email)
        print(pwd)
        cursor.execute('update student_details set student_password=%s where student_email=%s',[pwd,email])
        mysql.connection.commit()
        return render_template('students/login.html', msg='success')



    code=request.args.get('code')
    base64_bytes = code.encode('ascii')
    mail = base64.b64decode(base64_bytes)
    emailid = mail.decode('ascii')
    return render_template('/students/forget_password_change.html',emailid=emailid,msg='')










###################################### change password ########################################



@app.route("/student/change_password",methods=["POST", "GET"])
def change_password():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'student_id' in session and session.get("user_type") == 'student':
        email=request.form['email']
        passwd = request.form['password']
        passd = hashlib.md5(passwd.encode())
        password = passd.hexdigest()
        cursor.execute('update student_details set student_password=%s WHERE student_email = %s', (password, email))
        mysql.connection.commit()

        return redirect(url_for('student_profile'))






######################################## logout #######################################################
@app.route('/student_logout')
def student_logout():
    session.clear()
    return redirect(url_for('student_login'))





