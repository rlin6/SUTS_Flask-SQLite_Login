from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3
import hashlib

app = Flask(__name__)

def check_password(hashed_password, user_password):
    return hashed_password == user_password

def validate(username, password):
    con = sqlite3.connect('static/User.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username:
                        completion=check_password(dbPass, password)
    return completion


def check(username, password):
    con = sqlite3.connect('static/User.db')
    unique = True
    cur = con.cursor()

    if password != "":
        with con:
            cur.execute("SELECT * FROM Users")
            rows = cur.fetchall()
            for row in rows:
                dbUser = row[0]
                if username == dbUser:
                    unique = False
    else:
        unique = False
                
    if unique == True:
        sql = "INSERT INTO USERS(Username,Password) " \
              "VALUES(?,?)"
        info = (username, password)
        cur.execute(sql, info)
        con.commit()
        cur.close()
        con.close()

    return unique;
        
@app.route('/', methods=['GET', 'POST'])

def index():
    return render_template('/index.html')
    
@app.route('/login', methods=['GET', 'POST'])

def login():
    
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))

    return render_template('login.html',error=error)

@app.route('/register', methods=['GET', 'POST'])

def register():
    
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        unique = check(username, password)

        if unique == True:
            return redirect(url_for('success'))
        else:
            error = 'Username or password is invalid. Please try again.'
            
    return render_template('register.html',error=error)
            
@app.route('/secret')
def secret():
    return "You have successfully logged in"

@app.route('/success')
def success():
    return '''
            You have successfully registered. Press the button to go back.
            <br>
            
            <button onclick="window.location.href='/'"> Back </button>
            '''
            
if __name__ == '__main__':
    app.run(debug=True)

    
