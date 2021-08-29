from re import sub

from MySQLdb.cursors import Cursor
from app import *
@app.route("/data_entry/home", methods=["POST", "GET"])
def data_entry_home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':
        id=session.get('id')      

        home = arr.array('i', [0, 0, 0, 0])

        admin_name=session.get('name')
        cursor.execute('SELECT * FROM course_session_details')
        home[0] = len(cursor.fetchall())
      
        cursor.execute('SELECT * FROM student_details')
        home[1] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM course_details')
        home[2] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM faculty_details')
        home[3] = len(cursor.fetchall())
        # cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        # notifi = cursor.fetchall()
        return render_template('data_entry/index.html',admin_name=admin_name,count=home)
    else:
        return redirect(url_for('login'))





########################################### subject table ##########################################

@app.route("/data_entry/subject", methods=["POST", "GET"])
def data_entry_subject():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':
        id=session.get('id')  
        admin_name=session.get('name')
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['descr']                   
            try:
                cursor.execute("INSERT INTO subject (subject_name, subject_description) VALUES (%s, %s)",[name, description])
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')
        
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        # cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        # notifi = cursor.fetchall()
        return render_template('data_entry/subject.html',subject=subject,admin_name=admin_name)
    else:
        return redirect(url_for('login'))

@app.route('/data_entry/subject/select', methods=['GET', 'POST'])
def admin_adminuser_select():   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        subject = request.form['subject']
        print(subject)      
        cur.execute("SELECT * FROM subject WHERE subject_id = %s", [subject])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'subject_id': rs['subject_id'],
                    'subject_name': rs['subject_name'],
                    'subject_description': rs['subject_description']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)



@app.route("/data_entry/subject/update", methods=["POST", "GET"])
def data_entry_subject_update():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        subject_id = request.form['subject_id']
        subject_name = request.form['subject_name']
        subject_description = request.form['subject_description']    
        cursor.execute('update subject set subject_name=%s, subject_description = %s where subject_id=%s', [subject_name,subject_description,subject_id])
        mysql.connection.commit()
    return jsonify('success')   

####################################### subject table end ############################################


#########################################  Course Table ###############################################


@app.route("/data_entry/course", methods=["POST", "GET"])
def data_entry_course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':  
        id=session.get('id')
        count = arr.array('i', [0, 0, 0])
        admin_name=session.get('name')
        subject_id = request.args.get('course_id')  
        if request.method == 'POST':      
            adminid=session.get('id')
            subjectid = request.form['subjectid']
            cname = request.form['cname']
            grade = request.form['grade']
            cduration = request.form['duration']
            nosession = request.form['session']
            description = request.form['test1']                   
            try:
                cursor.execute("INSERT INTO course_details (subject_id, course_grade,course_name,course_description,course_duration,no_of_session,admin_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",[subjectid, grade,cname,description,cduration,nosession,adminid])
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')

        if subject_id:
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id and subject.subject_id=%s',[subject_id,])
            course = cursor.fetchall()
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id and subject.subject_id=%s',[subject_id,])
            count[0] = len(cursor.fetchall())      
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id and subject.subject_id=%s and course_details.course_status="open"',[subject_id,])
            count[1] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id and subject.subject_id=%s and course_details.course_status="close"',[subject_id,])
            count[2] = len(cursor.fetchall())
       
            
        else:
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
            course = cursor.fetchall()
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
            count[0] = len(cursor.fetchall())      
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id  and course_details.course_status="open"')
            count[1] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id  and course_details.course_status="close"')
            count[2] = len(cursor.fetchall())
            
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        for i in range(len(course)):
            # course[i]['course_description'] = html.unescape(course[i]['course_description'])
            print(course[i]['course_description'], i)

        # cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        # notifi = cursor.fetchall()
        return render_template('data_entry/course.html',course=course,subject=subject,count=count,admin_name=admin_name)
    else:
        return redirect(url_for('login'))



@app.route("/data_entry/course/update", methods=["POST", "GET"])
def data_entry_course_update():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':     
        if request.method == "POST":

            if request.form.get("delete"):
                result = request.form 
                id = result["delete"]
                cursor.execute('delete from course_details where course_id=%s;', [id])
                mysql.connection.commit()
                flash("Deleted ♥️")                
                return redirect(url_for('data_entry_course'))
    else:
        return redirect(url_for('login'))

@app.route('/data_entry/course/select', methods=['GET', 'POST'])
def data_entry_course_select():   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        course_id = request.form['course_id']
        cur.execute("SELECT * FROM course_details,subject WHERE course_details.subject_id=subject.subject_id and course_id = %s", [course_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'course_id': rs['course_id'],
                    'subject_name': rs['subject_name'],
                    'course_name': rs['course_name'],
                    'course_grade': rs['course_grade'],
                    'course_duration': rs['course_duration'],
                    'no_of_session': rs['no_of_session'],
                    'status': rs['course_status'],
                    'approval_status': rs['course_approval_status'],
                    'course_description': rs['course_description']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)

@app.route("/data_entry/course/change", methods=["POST", "GET"])
def data_entry_course_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":        
        course_id = request.form['course_id']
        course_name = request.form['course_name']
        course_duration = request.form['course_duration']
        no_of_session = request.form['no_of_session']
        status = request.form['status']
        course_description = request.form['test']
        cursor.execute('update course_details set course_name=%s, course_duration = %s ,no_of_session=%s , course_status=%s ,course_description=%s where course_id=%s', [course_name,course_duration,no_of_session,status,course_description,course_id])
        mysql.connection.commit()
    return jsonify('success')   


####################################### Course table end ############################################




#########################################  Course registered student Table ###############################################


@app.route("/data_entry/course/registered", methods=["POST", "GET"])
def data_entry_course_registered():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':  
        id=session.get('id')
        count = arr.array('i', [0, 0, 0])
        admin_name=session.get('name')
        subject_id = request.args.get('course_id')  
        # if request.method == 'POST':      
        #     adminid=session.get('id')
        #     subjectid = request.form['subjectid']
        #     cname = request.form['cname']
        #     grade = request.form['grade']
        #     cduration = request.form['duration']
        #     nosession = request.form['session']
        #     description = request.form['coursedes']                   
        #     try:
        #         cursor.execute("INSERT INTO course_details (subject_id, course_grade,course_name,course_description,course_duration,no_of_session,admin_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",[subjectid, grade,cname,description,cduration,nosession,adminid])
        #         mysql.connection.commit()
        #         return jsonify('success')
        #     except Exception as  Ex:
        #         return jsonify('error')

        if subject_id:
            cursor.execute('SELECT * FROM course_enroll_details,student_details Where course_enroll_details.student_id=student_details.student_id and course_enroll_details.course_id=%s',[subject_id,])
            course = cursor.fetchall()
            cursor.execute('SELECT * FROM course_enroll_details,student_details Where course_enroll_details.student_id=student_details.student_id and course_enroll_details.course_id=%s',[subject_id,])
            count[0] = len(cursor.fetchall())      
            # cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id and subject.subject_id=%s and course_details.course_status="open"',[subject_id,])
            # count[1] = len(cursor.fetchall())
            # cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id and subject.subject_id=%s and course_details.course_status="close"',[subject_id,])
            # count[2] = len(cursor.fetchall())
       
            
        else:
            cursor.execute('SELECT * FROM school_management.course_details,school_management.course_enroll_details,school_management.student_details Where course_details.course_id=course_enroll_details.course_id and course_enroll_details.student_id=student_details.student_id')
            course = cursor.fetchall()
            print(course)
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
            count[0] = len(cursor.fetchall())      
          
            
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        notifi = cursor.fetchall()
        print(course)
        return render_template('data_entry/course_registered.html',course=course,subject=subject,count=count,admin_name=admin_name,notifi=notifi,id=subject_id)

    else:

        return redirect(url_for('login'))



@app.route("/data_entry/course/registerd/student_mail", methods=["POST", "GET"])
def data_entry_course_registered_student_mail():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry': 

        if request.method == "POST" and 'id_stu' in request.form:
            studentid = request.form['id_stu']
            print(studentid)
            subject = request.form['subject']
            

            message = request.form['test']
            cursor.execute('select * from student_details where student_id =%s',[studentid])
            student = cursor.fetchone()
            
            a=email(student['student_email'],subject,message)
                            
            return jsonify('success')
        elif request.method == "POST" and 'course_id' in request.form:
            courseid = request.form['course_id']
            print(courseid)
            print('vbnm')
            subject = request.form['subject1']

            message = request.form['groupmail']
            cursor.execute('select student_details.student_email , course_enroll_details.course_id from student_details,course_enroll_details where course_enroll_details.student_id = student_details.student_id and course_enroll_details.course_id=%s',[courseid])
            student = cursor.fetchall()
            print(student)

            mail_list=[]
            for i in range (len(student)):
                mail_list.append(student[i]['student_email'])
            print(mail_list)

            a = email_group(mail_list, subject, message)

            return jsonify('success')
    else:
        return redirect(url_for('login'))



# @app.route("/data_entry/course/registerd/csv", methods=["POST", "GET"])
# def data_entry_course_registered_csv():
#     # if 'id' in session and session.get("user_type") == 'data_entry': 
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     subject_id = request.args.get('course_id')     
#     try:        
       # cursor.execute("SELECT * FROM course_enroll_details,student_details Where course_enroll_details.student_id=student_details.student_id and course_enroll_details.course_id=%s",[subject_id])
       # result = cursor.fetchall()
       # output = io.StringIO()
       # writer = csv.writer(output)
            
       # line = ['Emp Id, Emp First Name, Emp Last Name, Emp Designation']
       # writer.writerow(line)
       # for row in result:
          #  line = [str(row['student_id']) + ',' + row['student_name'] + ',' + row['student_name'] + ',' + row['student_email']]
          #  writer.writerow(line)
        #output.seek(0)
		
       # return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})
   	# except Exception as e:
    #     print(e)
    
        # try:            
        #     cursor.execute("SELECT * FROM course_enroll_details,student_details Where course_enroll_details.student_id=student_details.student_id and course_enroll_details.course_id=%s",[subject_id])
        #     result = cursor.fetchall()

        #     output = io.StringIO()
        #     writer = csv.writer(output)
            
        #     line = ['Emp Id, Emp First Name, Emp Last Name, Emp Designation']
        #     writer.writerow(line)

        #     for row in result:
        #         line = [str(row['emp_id']) + ',' + row['emp_first_name'] + ',' + row['emp_last_name'] + ',' + row['emp_designation']]
        #         writer.writerow(line)

        #     output.seek(0)
            
        #     return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})
	    # except Exception as e:
		#     print(e)
    

# @app.route('/data_entry/course/select', methods=['GET', 'POST'])
# def data_entry_course_select():   
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     if request.method == 'POST': 
#         course_id = request.form['course_id']
#         cur.execute("SELECT * FROM course_details,subject WHERE course_details.subject_id=subject.subject_id and course_id = %s", [course_id])
#         rsemployee = cur.fetchall()
#         employeearray = []
#         for rs in rsemployee:
#             employee_dict = {
#                     'course_id': rs['course_id'],
#                     'subject_name': rs['subject_name'],
#                     'course_name': rs['course_name'],
#                     'course_grade': rs['course_grade'],
#                     'course_duration': rs['course_duration'],
#                     'no_of_session': rs['no_of_session'],
#                     'status': rs['course_status'],
#                     'approval_status': rs['course_approval_status'],
#                     'course_description': rs['course_description']}
#             employeearray.append(employee_dict)
#         return json.dumps(employeearray)

# @app.route("/data_entry/course/change", methods=["POST", "GET"])
# def data_entry_course_change():
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     if request.method == "POST":        
#         course_id = request.form['course_id']
#         course_name = request.form['course_name']
#         course_duration = request.form['course_duration']
#         no_of_session = request.form['no_of_session']
#         status = request.form['status']
#         course_description = request.form['course_description']
#         cursor.execute('update course_details set course_name=%s, course_duration = %s ,no_of_session=%s , course_status=%s ,course_description=%s where course_id=%s', [course_name,course_duration,no_of_session,status,course_description,course_id])
#         mysql.connection.commit()
#     return jsonify('success')   


####################################### Course registered student table end ############################################







#########################################  session Table ###############################################


@app.route("/data_entry/session", methods=["POST", "GET"])
def data_entry_session():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':
        count = arr.array('i', [0, 0, 0])
        id=session.get('id')
        admin_name=session.get('name')
        session_ids = request.args.get('session_id')  
        print(session_ids)
        if request.method == 'POST':      
            adminid=session.get('id')
            cname = request.form['cname']
            sduration = request.form['sduration']
            sname = request.form['sname']
            desc = request.form['test1']
            print(desc,"******")
            sdate = request.form['sdate']
            stime = request.form['stime']
            etime = request.form['etime']          
            fid = request.form['fid']    
                           
            try:
                cursor.execute("INSERT INTO course_session_details (course_id, session_duration ,faculty_id,session_name,session_discription,session_date,session_starttime,session_endtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",[cname,sduration,fid,sname,desc,sdate,stime,etime])
                mysql.connection.commit()
                last_id = cursor.lastrowid
                print(last_id)
                cursor.execute('INSERT INTO session_content (session_id) values(%s)',[last_id,])
                mysql.connection.commit()                
                cursor.execute('INSERT INTO student_attendance (session_id,student_id) SELECT %s,student_id FROM course_enroll_details where course_id=%s'% (last_id,cname))
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')

        if session_ids:
            cursor.execute('SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=course_session_details.course_id and course_details.course_id=%s',[session_ids,])
            sess = cursor.fetchall()
            cursor.execute('SELECT * FROM course_session_details,course_details where course_details.course_id=course_session_details.course_id and course_details.course_id=%s',[session_ids,])
            count[0] = len(cursor.fetchall())      
            cursor.execute('SELECT * FROM course_session_details,course_details where course_details.course_id=course_session_details.course_id and course_details.course_id=%s and course_session_details.session_status="open"',[session_ids,])
            count[1] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM course_session_details,course_details where course_details.course_id=course_session_details.course_id and course_details.course_id=%s and course_session_details.session_status="close"',[session_ids,])
            count[2] = len(cursor.fetchall())
       
        else:
            cursor.execute('SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=course_session_details.course_id')
            sess = cursor.fetchall()
            cursor.execute('SELECT * FROM course_session_details,course_details where course_details.course_id=course_session_details.course_id')
            count[0] = len(cursor.fetchall())      
            cursor.execute('SELECT * FROM course_session_details,course_details where course_details.course_id=course_session_details.course_id and course_session_details.session_status="open"')
            count[1] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM course_session_details,course_details where course_details.course_id=course_session_details.course_id and course_session_details.session_status="close"')
            count[2] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id and course_details.course_approval_status="approved" and course_details.course_status="open"')
        course = cursor.fetchall()
        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
    
        for i in range(len(sess)):
            # print(sess)
            # sess[i]['session_discription'] = html.unescape(sess[i]['session_discription'])
            print(sess[i]['session_discription'], i)
        # cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        # notifi = cursor.fetchall()
        return render_template('data_entry/course session table.html',session=sess,course=course,count=count,faculty=faculty,admin_name=admin_name)
    else:
        return redirect(url_for('login'))

@app.route("/data_entry/session/update", methods=["POST", "GET"])
def data_entry_session_update():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':     
        
        if request.method == "POST":
            if request.form.get("delete"):
                result = request.form 
                id = result["delete"]
                cursor.execute('delete from course_session_details where session_id=%s;', [id])
                mysql.connection.commit()
                flash("Deleted ♥️")                                         
                return redirect(url_for('data_entry_session'))
    else:
        return redirect(url_for('login'))



@app.route('/data_entry/session/select', methods=['GET', 'POST'])
def data_entry_session_select():   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        sessio_id = request.form['sessio_id']
        print(sessio_id)      
        cur.execute("SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=course_session_details.course_id and session_id = %s", [sessio_id])
        rsemployee = cur.fetchall()
        for i in range(len(rsemployee)):
            # print(sess)
            # rsemployee[i]['session_discription'] = html.unescape(rsemployee[i]['session_discription'])
            print(rsemployee[i]['session_discription'], i,"bye")
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'session_id': rs['session_id'],
                    'course_name': rs['course_name'],
                    'session_name': rs['session_name'],
                    'session_discription': rs['session_discription'],
                    'session_date': rs['session_date'],
                    'status': rs['session_status'],
                    'session_starttime': rs['session_starttime'],
                    'session_endtime': rs['session_endtime'],
                    'faculty_name': rs['faculty_name']}
            employeearray.append(employee_dict)
        print(employeearray)
        return json.dumps(employeearray)

@app.route("/data_entry/session/change", methods=["POST", "GET"])
def data_entry_session_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":        
        session_id = request.form['session_id']
        print("session"+ session_id)
        session_name = request.form['session_name']
        session_date = request.form['session_date']
        session_starttime = request.form['session_starttime']
        session_endtime = request.form['session_endtime']
        session_status= request.form['status']
        session_discription = request.form['test']
        print(session_discription)
        cursor.execute('update course_session_details set session_name=%s, session_date = %s ,session_starttime=%s , session_endtime=%s ,session_status=%s ,session_discription = %s where session_id=%s', [session_name,session_date,session_starttime,session_endtime,session_status,session_discription,session_id])
        mysql.connection.commit()
    return jsonify('success')   



####################################### Session table end ############################################





########################################  Attendance Table ############################################




@app.route("/data_entry/session/attendance", methods=["POST", "GET"])
def data_entry_attendance():
    count = arr.array('i', [0, 0, 0])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':
        id=session.get('id')
        admin_name=session.get('name')
        session_ids = request.args.get('session_id')  
        session_name = request.args.get('session_name')  

        print(session_name)
        if session_ids:
            cursor.execute('select sa.*,sd.*,ssf.* from student_attendance sa left join student_details sd on sd.student_id = sa.student_id left join student_session_feedback ssf on ssf.student_id = sa.student_id where sa.session_id =%s',[session_ids,])
            attendance = cursor.fetchall()
            
            cursor.execute('SELECT * FROM student_attendance,student_details WHERE student_attendance.student_id=student_details.student_id and student_attendance.session_id=%s',[session_ids,])
            count[0] = len(cursor.fetchall())      
            cursor.execute('SELECT * FROM student_attendance,student_details WHERE student_attendance.student_id=student_details.student_id and student_attendance.session_id=%s and student_attendance.satt_present="YES"',[session_ids,])
            count[1] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM student_attendance,student_details WHERE student_attendance.student_id=student_details.student_id and student_attendance.session_id=%s and student_attendance.satt_present="NO"',[session_ids,])
            count[2] = len(cursor.fetchall())
        else:
            return redirect(url_for('login'))  

        cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        notifi = cursor.fetchall()
        return render_template('data_entry/attendance_table.html',attendance=attendance,session_name=session_name,admin_name=admin_name,count=count)
    else:
        return redirect(url_for('login'))

#########################################  Attendance Table end ###############################################

#########################################  Faculty Table ###############################################





@app.route("/data_entry/faculty", methods=["POST", "GET"])
def data_entry_faculty():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':
        id=session.get('id')
        admin_name=session.get('name')
        if request.method == 'POST':      
            adminid=session.get('id')
            fname = request.form['fname']
            email = request.form['email']
            contact = request.form['contact']              
            try:
                cursor.execute("INSERT INTO faculty_details (faculty_name, faculty_email ,faculty_contact) VALUES (%s, %s, %s)",[fname,email,contact])
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')
        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
        cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        notifi = cursor.fetchall()
        return render_template('data_entry/Faculty table.html',faculty=faculty,admin_name=admin_name)
    else:
        return redirect(url_for('login'))


@app.route("/data_entry/faculty/update", methods=["POST", "GET"])
def data_entry_faculty_update():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':     
        if request.method == "POST":
            if request.form.get("delete"):
                result = request.form 
                id = result["delete"]
                cursor.execute('delete from faculty_details where faculty_id=%s;', [id])
                mysql.connection.commit()
                flash("Deleted ♥️")                                         
                return redirect(url_for('data_entry_faculty'))
    else:
        return redirect(url_for('login'))




@app.route('/data_entry/faculty/select', methods=['GET', 'POST'])
def data_entry_faculty_select():   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        faculty_id = request.form['faculty_id']
        print(faculty_id)      
        cur.execute("SELECT * FROM faculty_details where faculty_id = %s", [faculty_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'faculty_id': rs['faculty_id'],
                    'faculty_name': rs['faculty_name'],
                    'faculty_email': rs['faculty_email'],
                    'faculty_contact': rs['faculty_contact']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)

@app.route("/data_entry/faculty/change", methods=["POST", "GET"])
def data_entry_faculty_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":        
        faculty_id = request.form['faculty_id']
        print("faculty_id"+ faculty_id)
        faculty_name = request.form['faculty_name']
        faculty_email = request.form['faculty_email']
        faculty_contact = request.form['faculty_contact']

        cursor.execute('update faculty_details set faculty_name=%s, faculty_email = %s ,faculty_contact=%s where faculty_id=%s', [faculty_name,faculty_email,faculty_contact,faculty_id])
        mysql.connection.commit()
    return jsonify('success')   




####################################### Faculty table end ############################################


#########################################  Student Table ###############################################






@app.route("/data_entry/student", methods=["POST", "GET"])
def data_entry_student():
    if 'id' in session and session.get("user_type") == 'data_entry':
        id=session.get('id')
        count = arr.array('i', [0, 0, 0, 0])
        school_id = request.args.get('school_id')  
        status = request.args.get('status')  

        admin_name=session.get('name')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if school_id:
            cursor.execute('SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s',[school_id,])
            student = cursor.fetchall()
            cursor.execute('SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s',[school_id,])
            count[0] = len(cursor.fetchall())  
    
            cursor.execute('SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s and student_details.account_status="allow"',[school_id,])
            count[1] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s and student_details.account_status="block"',[school_id,])
            count[2] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s and student_details.account_status="waiting"',[school_id,])
            count[3] = len(cursor.fetchall())
        elif status == "new":
            cursor.execute('SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.account_status="waiting"')
            student = cursor.fetchall()
            cursor.execute('SELECT * FROM student_details')
            count[0] = len(cursor.fetchall())      
            cursor.execute('SELECT * FROM student_details where account_status="allow"')
            count[1] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM student_details where account_status="block"')
            count[2] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM student_details where account_status="waiting"')
            count[3] = len(cursor.fetchall())
        else:
            cursor.execute('SELECT * FROM student_details')
            student = cursor.fetchall()
            cursor.execute('SELECT * FROM student_details')
            count[0] = len(cursor.fetchall())      
            cursor.execute('SELECT * FROM student_details where account_status="allow"')
            count[1] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM student_details where account_status="block"')
            count[2] = len(cursor.fetchall())
            cursor.execute('SELECT * FROM student_details where account_status="waiting"')
            count[3] = len(cursor.fetchall())

        # cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        # notifi = cursor.fetchall()
        return render_template('data_entry/student details table.html',student=student,count=count,admin_name=admin_name)
    else:
        return redirect(url_for('login'))




@app.route('/data_entry/student/select', methods=['GET', 'POST'])
def data_entry_student_select():   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        student_id = request.form['student_id']
        print(student_id)      
        cur.execute("SELECT * FROM student_details,school_details where student_details.school_id=school_details.school_id and student_id = %s", [student_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'student_id': rs['student_id'],
                    'student_name': rs['student_name'],
                    'student_contact': rs['student_contact'],
                    'school_name': rs['school_name'],
                    'school_board': rs['school_board'],
                    'school_pincode': rs['school_pincode'],
                    'student_email': rs['student_email'],
                    'student_grade': rs['student_grade'],             
                    'student_whatsapp': rs['student_whatsapp'],
                    'student_profile': rs['student_profile'],
                    'account_status': rs['account_status'],
                'student_idcard': rs['student_idcard'],
                'url_path': app.static_url_path

                    }
            employeearray.append(employee_dict)
        return json.dumps(employeearray)

@app.route("/data_entry/student/change", methods=["POST", "GET"])
def data_entry_student_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":        
        student_id = request.form['student_id']
        student_name = request.form['student_name']
        student_contact = request.form['student_contact']
        student_email = request.form['student_email']
        student_whatsapp = request.form['student_whatsapp']
        status = request.form['status']

        cursor.execute('select account_status from student_details where student_id=%s',[student_id])
        stu_status=cursor.fetchone()
        if(stu_status['account_status']!=status):
            if (status=='allow'):
                cursor.execute('select * from email_content where emailc_id = 2')
                email_mail= cursor.fetchone()
                subject= email_mail['email_subject']
                message= email_mail['email_message']
                a= email(student_email,subject,message)

            elif (status=='block'):
                cursor.execute('select * from email_content where emailc_id = 3')
                email_mail = cursor.fetchone()
                subject = email_mail['email_subject']
                message = email_mail['email_message']
                a = email(student_email, subject, message)





        
       
        cursor.execute('update student_details set student_name=%s, student_contact = %s ,student_email=%s , student_whatsapp=%s , account_status=%s where student_id=%s',
        [student_name,student_contact,student_email,student_whatsapp,status,student_id])
        mysql.connection.commit()
    return jsonify('success')   

####################################### Student table end ############################################


#########################################  School Table ###############################################





@app.route("/data_entry/school_details", methods=["POST", "GET"])
def data_entry_school_details():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':
        count = arr.array('i', [0, 0, 0, 0])

        id=session.get('id')
        status = request.args.get('status')  

        admin_name=session.get('name')
        if request.method == 'POST':      
            adminid=session.get('id')
            school_name = request.form['school_name']
            school_state = request.form['school_state']
            school_district = request.form['school_district']
            school_pincode = request.form['school_pincode']
            school_board = request.form['school_board']
            school_contact = request.form['school_contact']
           
           
            try:
                cursor.execute("INSERT INTO school_details (school_name, school_state ,school_district,school_pincode,school_board,school_contact) VALUES (%s, %s, %s, %s, %s, %s)",[school_name,school_state,school_district,school_pincode,school_board,school_contact])
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')
        if(status):
            cursor.execute('SELECT * FROM school_details where school_status=%s',[status,])
            school = cursor.fetchall()

        else:
            cursor.execute('SELECT * FROM school_details')
            school = cursor.fetchall()
        cursor.execute('SELECT * FROM school_details')
        count[0] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM school_details where school_status="approved"')
        count[1] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM school_details where school_status="rejected"')
        count[2] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM school_details where school_status="notapproved"')
        count[3] = len(cursor.fetchall())
        # cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        # notifi = cursor.fetchall()
        return render_template('data_entry/school_details.html',school=school,count=count,admin_name=admin_name)
    else:
        return redirect(url_for('login'))


# @app.route("/data_entry/faculty/update", methods=["POST", "GET"])
# def data_entry_faculty_update():
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     if 'id' in session and session.get("user_type") == 'data_entry':     
#         if request.method == "POST":
#             if request.form.get("delete"):
#                 result = request.form 
#                 id = result["delete"]
#                 cursor.execute('delete from faculty_details where faculty_id=%s;', [id])
#                 mysql.connection.commit()
#                 flash("Deleted ♥️")                                         
#                 return redirect(url_for('data_entry_faculty'))
#     else:
#         return redirect(url_for('login'))




@app.route('/data_entry/school_details/select', methods=['GET', 'POST'])
def data_entry_school_details_select():   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        school_id = request.form['school_id']
        print(school_id)      
        cur.execute("SELECT * FROM school_details where school_id = %s", [school_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'school_id': rs['school_id'],
                    'school_name': rs['school_name'],
                    'school_state': rs['school_state'],
                    'school_district': rs['school_district'],
                    'school_pincode': rs['school_pincode'],
                    'school_board': rs['school_board'],
                    'school_contact': rs['school_contact'],
                    'school_status': rs['school_status']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)

@app.route('/data_entry/school_details/import', methods=['GET', 'POST'])
def data_entry_school_details_import():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        school_id = request.form['school_id']
        print(school_id)
        cur.execute("SELECT * FROM school_details where school_id = %s", [school_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                'school_id': rs['school_id'],
                'school_name': rs['school_name']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)


        ### import function ###

@app.route('/data_entry/school_details/import_student', methods=['GET', 'POST'])
def data_entry_school_details_import_student():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":

        school_id = request.form['import_school_id']
        f = request.files['student_import']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, secure_filename(f.filename))

        f.save('temp.csv')

        cols=['student_name','student_contact','student_email','student_grade','student_whatsapp']
        df = pd.read_csv('temp.csv')
        result_cols = []

        for col in df.columns:
            print(col)
            result_cols.append(col)

        if collections.Counter(cols) == collections.Counter(result_cols):
            student_name=df['student_name'].to_list()
            student_contact = df['student_contact'].to_list()
            student_email = df['student_email'].to_list()
            student_grade = df['student_grade'].to_list()
            student_whatsapp = df['student_whatsapp'].to_list()

            for i in range(len(df.student_name)):
                    cursor.execute("SELECT * FROM student_details where student_email = %s", [student_email[i],])
                    data = cursor.fetchall()
                    if(data):
                        flash('Duplicate Data', 'error')

                        return redirect(url_for('data_entry_school_details'))
                    else:
                        cursor.execute('insert into student_details (student_name,student_contact,student_email,student_grade,student_whatsapp,student_password,school_id,account_status) values(%s,%s,%s,%s,%s,%s,%s,%s)',(student_name[i].upper(),student_contact[i],student_email[i],student_grade[i],student_whatsapp[i],student_contact[i],school_id,'allow'))
                        mysql.connection.commit()

                
            flash('Inserted success', 'success')

            return redirect(url_for('data_entry_school_details'))
            #return '''Success visit  <a href ="http://127.0.0.1:5000/data_entry/student">click here</a> to see changes'''

        else:
            flash('Invalid File', 'error')
            return redirect(url_for('data_entry_school_details'))
            #return '''Import failed check csv file fields and entry'''








@app.route("/data_entry/school_details/change", methods=["POST", "GET"])
def data_entry_school_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":        
        school_id = request.form['school_id']
        print("faculty_id"+ school_id)
        school_name = request.form['school_name']
        school_state = request.form['school_state']
        school_district = request.form['school_district']
        school_pincode = request.form['school_pincode']
        school_contact = request.form['school_contact']
        school_status = request.form['school_status']

        cursor.execute('update school_details set school_name=%s, school_state = %s ,school_district=%s,school_pincode=%s,school_contact=%s,school_status=%s where school_id=%s', [school_name,school_state,school_district,school_pincode,school_contact,school_status,school_id])
        mysql.connection.commit()
    return jsonify('success')   




####################################### Faculty table end ############################################


#######################################data entry pssword change ###################################

@app.route("/data_entry/password/change", methods=["POST", "GET"])
def change_dataentry_password():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':
        id = session.get('id')
        passwd = request.form['password']
        passd = hashlib.md5(passwd.encode())
        password = passd.hexdigest()

        cursor.execute('update admin set admin_password =%s where admin_id=%s',(password,id))
        mysql.connection.commit()
        flash('Password updated', 'success')

        return redirect(url_for('data_entry_home'))

################################end of data entry password change############################


################################email category ####################################
@app.route("/data_entry/email_category", methods=["POST", "GET"])
def data_entry_email_category():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method=='POST':
        print('123')
        cemail =request.form['cemail']
        subject = request.form['subject']
        message = request.form['test1']
        # message=html.unescape(message)

        cursor.execute('update email_content set email_subject =%s , email_message =%s where emailc_id=%s',(subject,message,cemail))
        mysql.connection.commit()
        return jsonify('success')
    elif 'id' in session and session.get("user_type") == 'data_entry':
        id = session.get('id')

        home = arr.array('i', [0, 0, 0, 0])

        admin_name = session.get('name')

        # cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        # notifi = cursor.fetchall()

        cursor.execute('select * from email_content')
        email=cursor.fetchall()
        for i in range(len(email)):
            # email[i]['email_message'] = html.unescape(email[i]['email_message'])
            print(email[i]['email_message'], i)


        return render_template('data_entry/email.html', admin_name=admin_name,email=email,len=len(email))




    else:
        return redirect(url_for('login'))
