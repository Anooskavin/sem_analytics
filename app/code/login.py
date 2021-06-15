from app import *

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == 'POST' and 'admin' in request.form and 'pwd' in request.form:
        user = request.form['admin']
        pwd = request.form['pwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE admin_username = %s AND admin_password= %s',(user,pwd))
        user = cursor.fetchone()
        if user['admin_usertype']=='data_entry':

            session['user_type'] = 'data_entry'
            session['id'] = user['admin_id']
            session['name'] = user['admin_name']

            #return redirect(url_for('data_entry_home'))
            return jsonify({'success' : 'data_entry'})

        elif user['admin_usertype']=='admin':
            print('admin')
            session['user_type'] = 'admin'
            session['id'] = user['admin_id']
            session['name'] = user['admin_name']
            return jsonify({'success' : 'admin'})
            #return jsonify({'error' : 'Incorrect email/password'})

    if(not session.get("id") is None):
        if(session.get("user_type") == 'data_entry'):
            return redirect(url_for('data_entry_home'))
        elif(session.get("user_type") == 'admin'):
            return redirect(url_for('admin_analytics_home'))


    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



@app.route("/user", methods=["POST", "GET"])
def user():
    return render_template('upload.html')

