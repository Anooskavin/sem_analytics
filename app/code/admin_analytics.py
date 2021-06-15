from re import sub

from MySQLdb.cursors import Cursor
from app import *
@app.route("/admin_analytics/home", methods=["POST", "GET"])
def admin_analytics_home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        home = arr.array('i', [0, 0, 0, 0])

        admin_name=session.get('name')
        print(admin_name)
        cursor.execute('SELECT * FROM course_session_details')
        home[0] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM student_details')
        home[1] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM course_details')
        home[2] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM faculty_details')
        home[3] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        return render_template('admin_analytics/index.html',admin_name=admin_name,count=home,subject=subject,course=course)
    else:
        return redirect(url_for('login'))





########################################### subject table ##########################################

@app.route("/admin_analytics/subject", methods=["POST", "GET"])
def admin_analytics_subject():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name=session.get('name')


        
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()

        return render_template('admin_analytics/subject.html',subject=subject,admin_name=admin_name,course=course)
    else:
        return redirect(url_for('login'))



####################################### subject table end ############################################


#########################################  Course Table ###############################################


@app.route("/admin_analytics/course", methods=["POST", "GET"])
def admin_analytics_course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name=session.get('name')


        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()

        return render_template('admin_analytics/course.html',course=course,subject=subject,admin_name=admin_name,)
    else:
        return redirect(url_for('login'))





####################################### Course table end ############################################


#########################################  session Table ###############################################


@app.route("/admin_analytics/session/", methods=["POST", "GET"])
def admin_analytics_session():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name=session.get('name')
        course_id=request.args.get('a')
        course_name = request.args.get('b')



        
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
        if course_id == None:
            cursor.execute('SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=course_session_details.course_id')
            sess = cursor.fetchall()
        else:

            cursor.execute('SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=%s and course_session_details.course_id=%s',(course_id,course_id))
            sess = cursor.fetchall()

        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        return render_template('admin_analytics/course session table.html',session=sess,subject=subject,course=course,faculty=faculty,admin_name=admin_name)
    else:
        return redirect(url_for('login'))




####################################### Session table end ############################################


#########################################  Faculty Table ###############################################





@app.route("/admin_analytics/faculty", methods=["POST", "GET"])
def admin_analytics_faculty():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name=session.get('name')

        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        return render_template('admin_analytics/Faculty table.html',faculty=faculty,subject=subject,admin_name=admin_name,course=course)
    else:
        return redirect(url_for('login'))







####################################### Faculty table end ############################################


#########################################  Student Table ###############################################






@app.route("/admin_analytics/student", methods=["POST", "GET"])
def admin_analytics_student():
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name=session.get('name')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_details order by student_name ASC')
        student = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        return render_template('admin_analytics/student details table.html',subject=subject,student=student,admin_name=admin_name,course=course)
    else:
        return redirect(url_for('login'))






####################################### Student table end ############################################


#########################################   ###############################################
@app.route("/admin_analytics/attendance", methods=["POST", "GET"])
def attendance():
    if 'id' in session and session.get("user_type") == 'admin':
        session_id=request.args.get('b')
        admin_name = session.get('name')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select DISTINCT student_details.student_name,student_details.school_grade, course_session_details.session_id,course_session_details.session_name from student_details, course_session_details, course_details, student_attendance where course_session_details.course_id = course_details.course_id and student_details.student_id = student_attendance.student_id and course_session_details.session_id =%s and  student_attendance.session_id=%s',(session_id, session_id))
        attendance= cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        return render_template('admin_analytics/attendance.html',attendance=attendance,admin_name=admin_name,subject=subject,course=course)
    else:
        return redirect(url_for('login'))
        
