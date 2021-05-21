import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__,template_folder='templates')


app.secret_key = 'Harsha'

# database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root1234'
app.config['MYSQL_DB'] = 'pro39'

# Intialize MySQL
mysql = MySQL(app)
 
@app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:

        username = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (username, password,))
        account = cursor.fetchone()


        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            with open('reply.aiml', 'r') as f:
            	return render_template('content.html', text=f.read(),msg="Open")
            
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'


    return render_template('index.html', msg='')


@app.route('/saveaiml/', methods=['GET', 'POST'])
def saveaiml():
	msg = ''
	if request.method=="POST" and 'content' in request.form:
		cont=request.form['content']
		with open('reply.aiml','w') as outfile:
			newcontent=str(cont)
			outfile.write(newcontent)
			msg='Information Updated Successfully!'

	with open ('reply.aiml', 'r') as f:
		return render_template('content.html', text=f.read(),msg=msg)





@app.route('/register/', methods=['GET', 'POST'])
def register():
	msg=''
	if request.method=="POST" and 'email' in request.form and 'password' in request.form:
		username=request.form['email']
		password=request.form['password']
		# Existing Acc
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE email = %s', (username,))
		account=cursor.fetchone()
		# If account exists show error and validation checks
		if account:
			msg='Account already exists!'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
			msg='Invalid email address!'
		elif not username or not password:
			msg='Please fill out the form!'
		else:
			cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (username, password,))
			mysql.connection.commit()
			msg='You have successfully registered!'
	elif request.method=="POST":
		msg='Please Fill out the Form!'
	return render_template('registration.html',msg=msg)


@app.route('/logout/')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(port=5000,debug=True)
