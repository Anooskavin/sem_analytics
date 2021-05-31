from app import *

@app.route("/", methods=["POST", "GET"])
def login():
    msg=''
    if request.method == 'POST' and 'admin' in request.form and 'pwd' in request.form:
        user = request.form['admin']
        pwd = request.form['pwd']
        print(user)
        print(pwd)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE admin_username = %s AND admin_password= %s',(user,pwd))
        admin_l = cursor.fetchone()


        if admin_l:
            return jsonify({'success' : 'Account found'})

        else :
            return jsonify({'error' : 'Incorrect email/password'})



    return render_template('login.html',msg=msg)




@app.route("/user", methods=["POST", "GET"])
def user():
    return render_template('upload.html')

if __name__ == '__main__':
   app.run(debug=True)