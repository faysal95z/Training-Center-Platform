import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import bcrypt
import mysql.connector as SQLc

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

app.secret_key = "your_secret_key_here"

# MySQL Configuration

mydb = SQLc.connect(
  host="localhost",
  user="alshain_python_user",
  password="password",
  database="Alshain"
)

class ManagingAddUsrForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    usertype = StringField("UserType", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Enregistrer")

    def validate_username(self,field):
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user :
            raise ValidationError("Username already taken")

class ManagingDelUsrForm(FlaskForm):
    userId = StringField("Id Utilisateur", validators=[DataRequired()])
    submit = SubmitField("Supprimer")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Connexion")

def getUserList():
    cursor = mydb.cursor()
    cursor.execute("SELECT user_id, username, usertype FROM users")
    USRlist = cursor.fetchall()
    cursor.close()
    return USRlist

USERLIST = getUserList()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/tool")
def tool():
    if "user_id" in session :
        user_id = session["user_id"]

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template("tool.html", user=user)
    
    return redirect(url_for("login"))

@app.route("/managingAddUsr", methods=["GET", "POST"])
def managingAddUsr():
    form = ManagingAddUsrForm()
    global USERLIST
    if "user_id" in session :
        user_id = session["user_id"]

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user[2] == "admin":
            if form.validate_on_submit():
                username = form.username.data
                usertype = form.usertype.data
                password = form.password.data

                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

                cursor = mydb.cursor()
                cursor.execute("INSERT INTO users (username, usertype, password) VALUES (%s, %s, %s)", (username, usertype, hashed_password))
                mydb.commit()
                cursor.close()
                USERLIST = getUserList()
                return redirect(url_for("managingAddUsr"))

            return render_template("managingAddUsr.html", form=form, USERLIST=USERLIST, user=user)
    
    return redirect(url_for("dashboard"))

@app.route("/managingDelUsr", methods=["GET", "POST"])
def managingDelUsr():
    form = ManagingDelUsrForm()
    global USERLIST
    if "user_id" in session :
        user_id = session["user_id"]

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user[2] == "admin":
            if form.validate_on_submit():
                userId = form.userId.data

                cursor = mydb.cursor()
                cursor.execute("DELETE FROM users WHERE user_id = %s", (userId,))
                mydb.commit()
                cursor.close()
                USERLIST = getUserList()
                return redirect(url_for("managingDelUsr"))

            return render_template("managingDelUsr.html", form=form, USERLIST=USERLIST, user=user)
    
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode("utf-8"), user[3]) :
            session["user_id"] = user[0]
            return redirect(url_for("dashboard"))
        else :
            flash("Login failed. Please check your credentials.")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)

@app.route("/dashboard")
def dashboard():
    if "user_id" in session :
        user_id = session["user_id"]

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template("dashboard.html", user=user)
    
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been successfully logged out")
    return redirect(url_for("login"))

@app.route("/prompt", methods=["POST"])
def prompt():
    messages = request.json["messages"]
    conversation = build_conversation_dict(messages)

    return Response(event_stream(conversation), mimetype="text/event-stream")

def build_conversation_dict(messages : list) -> list[dict]:
    return [
        {"role": "user" if i % 2 == 0 else "assistant", "content": message}
        for i, message in enumerate(messages)
    ]

def event_stream(conversation: list[dict]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        stream=True
    )
#gpt-4-turbo gpt-3.5-turbo

    for line in response:
        text = line.choices[0].delta.get('content', '')
        if len(text):
            yield text

if __name__ == "__main__" :
    app.run(debug=True, host="127.0.0.1", port=5000)