from app import *

#####################     Student login and register ####################################################

@app.route("/student",methods=["POST", "GET"])
def student_login():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'pwd' in request.form:
        username=request.form['username']
        pwd=request.form['pwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from student_details where student_password=%s and account_status =%s and student_contact =%s or student_email =%s',(pwd,'yes',username,username))
        student = cursor.fetchone()
        if student:
            return '''Success'''
        else:
            return render_template('students/login.html',msg='Invalid Credentials/ Account not Verified')


    return render_template('students/login.html',msg='')

@app.route("/student/register",methods=["POST", "GET"])
def student_register():
    msg=''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from school_details')
    school_details=cursor.fetchall()
    if request.method == 'POST':
        username=request.form['username']
        email=request.form['email']
        mobile=request.form['mobile']
        grade=request.form['grade']
        whatsapp=request.form['whatsapp']
        #state1=request.form['state1']
        #district1=request.form['district1']
        #board=request.form['board']

        school_name=request.form['school_name']


        password=request.form['password']

        cursor.execute('select * from student_details where student_email=%s ',[email])
        student=cursor.fetchone()
        if student:
            return render_template('students/register.html', school_details=school_details,msg='Account Already exists')


        else:
            cursor.execute ('select school_id from school_details where school_name =%s',[school_name])
            school=cursor.fetchone()

            cursor.execute('insert into student_details (student_name ,student_contact, student_email,student_grade,student_whatsapp,student_password,school_id,account_status) values(%s,%s,%s,%s,%s,%s,%s,%s)',(username,mobile,email,grade,whatsapp,password,school['school_id'],'No') )
            mysql.connection.commit()
            return render_template('students/register.html', school_details=school_details,msg='Registered Successfuly Check email/message for verification we will get you soon ')



    return render_template('students/register.html',school_details=school_details,msg='')


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