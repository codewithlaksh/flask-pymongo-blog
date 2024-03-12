from project import app, mongo
from flask import request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/handlesignup", methods=["POST"])
def handlesignup():
    email = request.form.get("signup_email")
    password1 = request.form.get("signup_password1")
    password2 = request.form.get("signup_password2")
    path = request.form.get("path")
    username = email.split('@')[0];

    if mongo.db.users.find_one({"email": email}):
        flash("User email already exists!", "error")
        return redirect(path)
    else:
        if (password1 != password2):
            flash("Passwords do not match!", "error")
            return redirect(path)
        else:
            mongo.db.users.insert_one({"username": username, "email": email, "password": generate_password_hash(password1, salt_length=10)})
            flash("User account created successfully!", "success")
            return redirect(path)
        
@app.route("/handlelogin", methods=["POST"])
def handlelogin():
    email = request.form.get("login_email")
    password = request.form.get("login_password")
    path = request.form.get("path")
    username = email.split('@')[0];

    if mongo.db.users.find_one({"email": email}):
        user = mongo.db.users.find_one({"email": email})
        if check_password_hash(user['password'], password):
            session['user'] = username
            session['userID'] = str(user['_id'])
            flash("You have been logged in successfully!", "success")
            return redirect(path)
        else:
            flash("Invalid password! Please try again.", "error")
            return redirect(path)
    else:
        flash("No such user exists!")
        return redirect(path)
    
@app.route("/logout")
def handlelogout():
    if 'user' in session:
        session.pop('user')
        flash("You hav been logged out successfully!", "success")
        return redirect(url_for('home'))