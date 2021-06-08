from app import *

@app.route('/feedback')
def feedback():
    id = request.args.get('id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM course_session_details,course_details where course_details.course_id = course_session_details.course_id and session_id=%s',[id])
    feedback = cursor.fetchone()

    if feedback['session_status']=='open':
        return render_template('feedback/index.html',feedback=feedback)
    else:
        return render_template('feedback/formclosed.html')

@app.route('/feedback/submit', methods=["POST", "GET"])
def feedback_submit():
    if request.method=='POST':
        name=request.form['text1']
        email = request.form['email']
        mobile = request.form['mobile']
        grade = request.form['grade']
        whatsapp = request.form['whatsapp']
        schoolname = request.form['schoolname']
        state=request.form['state']
        district = request.form['district']
        pin= request.form['pin']
        board = request.form['board']
        student_feedback = request.form['feedback']
        choice=request.form['choice']
        session_id=request.form['session_id']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM course_session_details where session_id=%s',[session_id])
        feedback = cursor.fetchone()


        if feedback['session_status']=='open':


            cursor.execute('SELECT * FROM student_details where student_name=%s and student_contact=%s', (name,mobile))
            student = cursor.fetchone()
            if student:
                cursor.execute('SELECT * FROM student_attendance where student_id=%s and session_id=%s',
                               (student['student_id'],session_id))
                attendance = cursor.fetchone()

                if attendance:
                    return render_template('feedback/alredyresponded.html')
                else:

                    try:

                        cursor.execute('insert into student_attendance (student_id,session_id) values(%s,%s) ',(student['student_id'],session_id))
                        mysql.connection.commit()

                        cursor.execute('insert into student_session_feedback (student_id,session_id,stu_session_feedback,stu_session_willingness) values(%s,%s,%s,%s) ',
                                       (student['student_id'], session_id,student_feedback,choice))
                        mysql.connection.commit()


                    except Exception as Ex:
                        print('Error in Attendance: %s'%(Ex))

                    return render_template('feedback/success.html')
            else:
                try:

                    cursor.execute('insert into student_details(student_name,student_contact,student_email,school_name,school_grade,school_state,school_district,school_pincode,student_whatsapp,school_board) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ', (name, mobile,email,schoolname,grade,state,district,pin,whatsapp,board))
                    mysql.connection.commit()
                    last_id = cursor.lastrowid
                    cursor.execute('insert into student_attendance (student_id,session_id) values(%s,%s) ',
                                   (last_id, session_id))
                    mysql.connection.commit()
                    cursor.execute(
                        'insert into student_session_feedback (student_id,session_id,stu_session_feedback,stu_session_willingness) values(%s,%s,%s,%s) ',
                        (last_id, session_id, student_feedback, choice))
                    mysql.connection.commit()
                except Exception as Ex:
                    print('Error in Student Insertion: %s'%(Ex))
                return render_template('feedback/success.html')

        else:
            return render_template('feedback/formclosed.html')





















