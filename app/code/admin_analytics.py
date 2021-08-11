from re import sub

from MySQLdb.cursors import Cursor
from app import *


@app.route("/admin_analytics/home", methods=["POST", "GET"])
def admin_analytics_home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        home = arr.array('i', [0, 0, 0, 0])

        admin_name = session.get('name')
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
        return render_template('admin_analytics/index.html', admin_name=admin_name, count=home, subject=subject,
                               course=course)
    else:
        return redirect(url_for('login'))


########################################### subject table ##########################################

@app.route("/admin_analytics/subject", methods=["POST", "GET"])
def admin_analytics_subject():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')

        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()

        return render_template('admin_analytics/subject.html', subject=subject, admin_name=admin_name, course=course)
    else:
        return redirect(url_for('login'))


####################################### subject table end ############################################
@app.route('/admin/course/select', methods=['GET', 'POST'])
def admin_entry_course_select():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        print('hi1')
        course_id = request.form['course_id']
        cur.execute(
            "SELECT * FROM course_details,subject WHERE course_details.subject_id=subject.subject_id and course_id = %s",
            [course_id])
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

                'course_approval_status': rs['course_approval_status'],
                'course_description': rs['course_description']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)


@app.route("/admin/course/change", methods=["POST", "GET"])
def admin_entry_course_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        print('hi')
        course_id = request.form['course_id']
        course_name = request.form['course_name']
        course_duration = request.form['course_duration']
        course_grade = request.form['course_grade']
        no_of_session = request.form['no_of_session']
        #status = request.form['status']
        course_approval_status = request.form['course_approval_status']
        print(course_approval_status)
        course_description = request.form['course_description']
        cursor.execute(
            'update course_details set course_name=%s, course_duration = %s ,course_grade=%s,no_of_session=%s , course_approval_status=%s ,course_description=%s where course_id=%s',
            [course_name, course_duration,course_grade, no_of_session, course_approval_status, course_description, course_id])
        mysql.connection.commit()
    return jsonify('success')


#########################################  Course Table ###############################################


@app.route("/admin_analytics/course", methods=["POST", "GET"])
def admin_analytics_course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')

        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()

        return render_template('admin_analytics/course.html', course=course, subject=subject, admin_name=admin_name)
    else:
        return redirect(url_for('login'))


@app.route("/admin_analytics/approval_course", methods=["POST", "GET"])
def admin_approval_course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        course_id = int(request.args.get('a'))
        status = request.args.get('b')
        print(course_id)
        print(status)
        print(type(course_id))

        cursor.execute('update course_details set course_approval_status=%s Where course_id=%s', (status, course_id))
        mysql.connection.commit()
        return redirect(url_for('admin_analytics_course'))


####################################### Course table end ############################################


#########################################  session Table ###############################################


@app.route("/admin_analytics/session", methods=["POST", "GET"])
def admin_analytics_session():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')
        course_id = request.args.get('a')
        course_name = request.args.get('b')

        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
        if course_id == None:
            cursor.execute(
                'SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=course_session_details.course_id')
            sess = cursor.fetchall()
        else:

            cursor.execute(
                'SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=%s and course_session_details.course_id=%s',
                (course_id, course_id))
            sess = cursor.fetchall()

        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        return render_template('admin_analytics/course session table.html', session=sess, subject=subject,
                               course=course, faculty=faculty, admin_name=admin_name)
    else:
        return redirect(url_for('login'))

@app.route('/admin/session/select', methods=['GET', 'POST'])
def admin_entry_session_select():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print("hi")
    if request.method == 'POST':
        print('hi1')
        session_id = request.form['session_id']
        cur.execute(
            "SELECT * FROM course_details,course_session_details,faculty_details WHERE course_session_details.course_id=course_details.course_id and course_session_details.faculty_id=faculty_details.faculty_id and session_id = %s",
            [session_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                'session_id': rs['session_id'],
                'course_name': rs['course_name'],
                'session_name': rs['session_name'],
                'faculty_name': rs['faculty_name'],
                'session_status': rs['session_status'],
                'session_starttime': rs['session_starttime'],
                'session_endtime': rs['session_endtime'],
                'session_discription': rs['session_discription']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)
####################################### Session table end ############################################


#########################################  Faculty Table ###############################################


@app.route("/admin_analytics/faculty", methods=["POST", "GET"])
def admin_analytics_faculty():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')

        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        return render_template('admin_analytics/Faculty table.html', faculty=faculty, subject=subject,
                               admin_name=admin_name, course=course)
    else:
        return redirect(url_for('login'))


####################################### Faculty table end ############################################


#########################################  Student Table ###############################################


@app.route("/admin_analytics/student", methods=["POST", "GET"])
def admin_analytics_student():
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_details order by student_name ASC')
        student = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        return render_template('admin_analytics/student details table.html', subject=subject, student=student,
                               admin_name=admin_name, course=course)
    else:
        return redirect(url_for('login'))


####################################### Student table end ############################################


#########################################  attendance details ###############################################
@app.route("/admin_analytics/attendance", methods=["POST", "GET"])
def attendance():
    if 'id' in session and session.get("user_type") == 'admin':
        session_id = request.args.get('b')
        admin_name = session.get('name')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'select DISTINCT student_details.student_name,student_details.student_contact,student_details.school_grade, student_attendance.satt_present,course_session_details.session_name from student_details, course_session_details, course_details, student_attendance where course_session_details.course_id = course_details.course_id and student_details.student_id = student_attendance.student_id and course_session_details.session_id =%s and  student_attendance.session_id=%s',
            (session_id, session_id))
        attendance = cursor.fetchall()

        cursor.execute(
            "SELECT count(satt_present) as present from student_attendance  where satt_present='YES' and  session_id=%s",
            (session_id))
        present = cursor.fetchone()

        cursor.execute(
            "SELECT count(satt_present) as absent from student_attendance  where satt_present='NO' and  session_id=%s",
            (session_id))
        absent = cursor.fetchone()

        return render_template('admin_analytics/attendance.html', attendance=attendance, admin_name=admin_name,
                               present=present, absent=absent)
    else:
        return redirect(url_for('login'))


#########################################  attendance details end ###############################################


#########################################  User Table ###############################################


@app.route("/admin_analytics/adminuser", methods=["POST", "GET"])
def admin_analytics_user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        id = session.get('id')
        admin_name = session.get('name')
        if request.method == 'POST':
            adminid = session.get('id')
            name = request.form['name']
            username = request.form['username']
            passwd = request.form['passwd']
            user_type = request.form['user_type']

            try:
                cursor.execute(
                    "INSERT INTO admin (admin_name, admin_username ,admin_password,admin_usertype) VALUES (%s, %s, %s,%s)",
                    [name, username, passwd, user_type])
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')
        cursor.execute('SELECT * FROM admin')
        user = cursor.fetchall()
        cursor.execute(
            'SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',
            [id])
        notifi = cursor.fetchall()
        return render_template('admin_analytics/admin_user.html', user=user, admin_name=admin_name, notifi=notifi)
    else:
        return redirect(url_for('login'))


@app.route("/admin_analytics/adminuser/update", methods=["POST", "GET"])
def admin_analytics_user_update():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        if request.method == "POST":
            if request.form.get("delete"):
                result = request.form
                id = result["delete"]
                cursor.execute('delete from admin where admin_id=%s;', [id])
                mysql.connection.commit()
                flash("Deleted ♥️")
                return redirect(url_for('admin_analytics_user'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_analytics/adminuser/select', methods=['GET', 'POST'])
def admin_analytics_user_select():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        print(admin_id)
        cur.execute("SELECT * FROM admin where admin_id = %s", [admin_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                'admin_id': rs['admin_id'],
                'admin_name': rs['admin_name'],
                'admin_username': rs['admin_username'],
                'admin_password': rs['admin_password'],
                'admin_status': rs['admin_status'],
                'admin_usertype': rs['admin_usertype']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)


@app.route("/admin_analytics/adminuser/change", methods=["POST", "GET"])
def admin_analytics_user_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        admin_id = request.form['admin_id']
        admin_name = request.form['admin_name']
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']
        admin_status = request.form['status']
        admin_usertype = request.form['user_type']

        cursor.execute(
            'update admin set admin_name=%s, admin_username = %s ,admin_password=%s ,admin_status=%s , admin_usertype = %s where admin_id=%s',
            [admin_name, admin_username, admin_password, admin_status, admin_usertype, admin_id])
        mysql.connection.commit()
    return jsonify('success')

####################################### User table end ############################################
