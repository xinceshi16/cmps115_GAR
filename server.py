import mysql.connector

from bottle import get, route, run, template, view, static_file, request, post
__author__ = 'kai'

from flask import Flask

app = Flask(__name__)

@get('/')
def index():
    return template('login_temp')


@get('/register')
def register():
    return template("register_temp")

def register_connectDB(username,password):
    mydb = mysql.connector.connect(
        host = "localhost",
        user="root",
        passwd="password",
        database="gar_database"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT username FROM user")
    myresult = mycursor.fetchall()
    usern = ""
    for x in myresult:
        usern = x[0]
    if usern == username:
        print "username already exist"
        return False
    else:
        sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        return True

    mydb.close()


@post('/register', methods='post')
def register():
    register_username = request.forms.get('username')
    register_password = request.forms.get('password')
    print register_username
    if register_password == "" and register_username == "":
        return template("login_temp")
    if register_connectDB(register_username,register_password) == True:
        return template("register_succeed")
    else:
        return template("register_temp")

@get('/register-succeed')
def register_succeed():
    return template("register_succeed")

@get('/login-succeed')
def login_succeed():
    return template("login_succeed")

@get('/find-password-succeed')
def password_succeed():
    return template("password-succeed")

@get('/findpw')
def find_pw():
    return template("findPW_temp")

@get('/main')
def main():
    return template("main_temp")


# Let's add some code to serve jpg images from our static images directory.
@route('/images/<filename:re:.*\.*>')
def serve_image(filename):
    return static_file(filename, root='images', mimetype='image/png jpg')

def login_connectDB(username, password):
    str_sql = "SELECT PASSWORD FROM user where username ='" + username  + "'"
    mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd="password",
    database="gar_database"
)
    mycursor = mydb.cursor()
    print ("sql: "+ str(str_sql))
    mycursor.execute(str_sql)
    myresult = mycursor.fetchone()
    print ("myresult: " + str(myresult))
    if myresult is not None:
        for x in myresult:
            psw = x
        if psw == password:
            print "password is correct"
            return True
        else:
            print "password is wrong"
            return False
    else:
        return False
    mydb.close()



@post('/login')
def login():
    login_username = request.forms.get('username')
    login_password = request.forms.get('password')
    print("login_username: " + str(login_username))
    print("login_password: " + str(login_password))
    if login_connectDB(login_username,login_password)== False:
        return template("login_wrong")
    else:
        return template("login_succeed")


# Code for serving css stylesheets from /css directory.
@route('/css/<filename:re:.*.css>')
def serve_css(filename):
    return static_file(filename, root='css', mimetype='text/css')


run(reloader=True, host='localhost', port=3005)

