"""
Auhtor: Vishal Deshmukh
Program:Web using oauth and sqlite3 db
"""

from flask import Flask, redirect,request, url_for, session,render_template
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import sqlite3 as sql

# App config
app = Flask(__name__)
# Session config
app.config["SECRET_KEY"]="SECRET KEY"
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="Google_ClientID",#enter google client id from creditinals
    client_secret="google_secret_key",# enter google client key from creditinals
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/')
def hello_world():
    email = dict(session).get("email")
    return f'Hello, you are logged in as {email}!'

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()
    session['profile'] = user_info
    session.permanent = True
    return redirect(url_for("register"))

@app.route("/register",methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            email=request.form['email']
            password = request.form['password']
            name = request.form['Name']
            phone=request.form['phone']
            address=request.form['address']
            skills=request.form['skills']
            education=request.form['education']
            certifications=request.form['certifications']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (email,password,name,phone,address,skills,education,certifications)VALUES(?, ?, ?, ?,?,?,?,?)",(email,password,name,phone,address,skills,education,certifications) )

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            con.row_factory = sql.Row
            cur = con.cursor()
            rows = cur.execute('select * from students').fetchall()
            return render_template("about.html", rows=rows)
            con.close()
    return render_template("register.html")


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from students ")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
