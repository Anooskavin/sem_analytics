from app import *

@app.route('/feedback')
def feedback():
    base64_message = request.args.get('id')
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    id = message_bytes.decode('ascii')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM course_session_details,course_details where course_details.course_id = course_session_details.course_id and session_id=%s',[id])
    feedback = cursor.fetchone()

    if feedback['session_status']=='open':
        cursor.execute('SELECT * FROM student_details,school_details,course_enroll_details,course_session_details WHERE student_details.student_id=course_enroll_details.student_id AND student_details.school_id = school_details.school_id AND course_session_details.course_id=course_enroll_details.course_id AND course_session_details.session_id = %s',[id])
        student = cursor.fetchall()

        return render_template('feedback/index.html',feedback=feedback,student=student)
    else:
        return render_template('feedback/formclosed.html')

@app.route('/feedback/submit', methods=["POST", "GET"])
def feedback_submit():
    if request.method=='POST':
        student_id=request.form['student_id']
        student_feedback = request.form['feedback']
        choice=request.form['choice']
        session_id=request.form['session_id']
        print(student_id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM course_session_details where session_id=%s',[session_id])
        feedback = cursor.fetchone()


        if feedback['session_status']=='open':
            print("enter")


            cursor.execute('SELECT * FROM student_details where student_id=%s and account_status=%s', (student_id,'allow'))

            student = cursor.fetchone()
            if student:
                cursor.execute('SELECT * FROM student_attendance where student_id=%s and session_id=%s and satt_present="YES"',
                               (student_id,session_id))
                attendance = cursor.fetchone()

                if attendance:
                    return jsonify('responded')
                else:
                    cursor.execute('SELECT * FROM student_attendance where student_id=%s and session_id=%s',(student_id,session_id))
                    ass = cursor.fetchone()

                    try:

                        cursor.execute('update student_attendance set satt_present="YES" where student_id =%s and session_id =%s ',(student['student_id'],session_id))
                        mysql.connection.commit()

                        cursor.execute('insert into student_session_feedback (student_id,session_id,stu_session_feedback,stu_session_willingness,satt_id) values(%s,%s,%s,%s,%s) ',
                                       (student['student_id'], session_id,student_feedback,choice,ass['satt_id']))
                        mysql.connection.commit()

                        return jsonify('submit')

                    except Exception as Ex:
                        print('Error in Attendance: %s'%(Ex))
      
            else:
                return jsonify('close')
        else:
            return jsonify('close')




@app.route('/feedback/close')
def feedback_close():
    return render_template('feedback/formclosed.html')


@app.route('/feedback/alreadyresponded')
def feedback_responded():
    return render_template('feedback/alredyresponded.html')


@app.route('/feedback/submited')
def feedback_submited():
    return render_template('feedback/success.html')









