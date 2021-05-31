from app import *
@app.route("/data_entry/home", methods=["POST", "GET"])
def data_entry_home():
    return render_template('data_entry/index.html')

@app.route("/data_entry/subject", methods=["POST", "GET"])
def data_entry_subject():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM subject')
    subject = cursor.fetchall()
    return render_template('data_entry/subject.html',subject=subject)

@app.route("/data_entry/course", methods=["POST", "GET"])
def data_entry_course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
    course = cursor.fetchall()
    return render_template('data_entry/course.html',course=course)



@app.route("/data_entry/session", methods=["POST", "GET"])
def data_entry_session():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=course_session_details.course_id')
    session = cursor.fetchall()
    return render_template('data_entry/course session table.html',session=session)

@app.route("/data_entry/faculty", methods=["POST", "GET"])
def data_entry_faculty():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM faculty_details')
    faculty = cursor.fetchall()
    return render_template('data_entry/Faculty table.html',faculty=faculty)

@app.route("/data_entry/student", methods=["POST", "GET"])
def data_entry_student():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM student_details')
    student = cursor.fetchall()
    return render_template('data_entry/student details table.html',student=student)