from re import sub
from app import *
@app.route("/data_entry/home", methods=["POST", "GET"])
def data_entry_home():
    if 'id' in session and session.get("user_type") == 'data_entry':
        return render_template('data_entry/index.html')
    else:
        return redirect(url_for('login'))

@app.route("/data_entry/subject", methods=["POST", "GET"])
def data_entry_subject():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':
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
        return render_template('data_entry/subject.html',subject=subject)
    else:
        return redirect(url_for('login'))




@app.route("/data_entry/course", methods=["POST", "GET"])
def data_entry_course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':        
        if request.method == 'POST':      
            adminid=session.get('id')
            subjectid = request.form['subjectid']
            cname = request.form['cname']
            grade = request.form['grade']
            cduration = request.form['duration']
            nosession = request.form['session']
            description = request.form['coursedes']                   
            try:
                cursor.execute("INSERT INTO course_details (subject_id, course_grade,course_name,course_description,course_duration,no_of_session,admin_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",[subjectid, grade,cname,description,cduration,nosession,adminid])
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')
        
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        return render_template('data_entry/course.html',course=course,subject=subject)
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




@app.route("/data_entry/session", methods=["POST", "GET"])
def data_entry_session():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'data_entry':
        if request.method == 'POST':      
            adminid=session.get('id')
            cname = request.form['cname']
            sduration = request.form['sduration']
            sname = request.form['sname']
            desc = request.form['desc']
            sdate = request.form['sdate']
            stime = request.form['stime']
            etime = request.form['etime']          
            fid = request.form['fid']                   
         
            try:
                cursor.execute("INSERT INTO course_session_details (course_id, session_duration ,faculty_id,session_name,session_discription,session_date,session_starttime,session_endtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",[cname,sduration,fid,sname,desc,sdate,stime,etime])
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')

        
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
        cursor.execute('SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=course_session_details.course_id')
        sess = cursor.fetchall()
        return render_template('data_entry/course session table.html',session=sess,course=course,faculty=faculty)
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

@app.route("/data_entry/faculty", methods=["POST", "GET"])
def data_entry_faculty():
    if 'id' in session and session.get("user_type") == 'data_entry':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
        return render_template('data_entry/Faculty table.html',faculty=faculty)
    else:
        return redirect(url_for('login'))

@app.route("/data_entry/student", methods=["POST", "GET"])
def data_entry_student():
    if 'id' in session and session.get("user_type") == 'data_entry':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_details')
        student = cursor.fetchall()
        return render_template('data_entry/student details table.html',student=student)
    else:
        return redirect(url_for('login'))