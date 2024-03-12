from project import app, mongo, params
from flask import render_template, session, redirect, url_for, request, flash
from datetime import datetime
import os

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if ('admin' in session):
        return redirect(url_for("addpost"))
    else:
        if (request.method == "POST"):
            username = request.form.get("username")
            password = request.form.get("password")

            if username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD'):
                session['admin'] = username
                return redirect(url_for('admin_dashboard'))
        return render_template("login.html")
    
@app.route("/admin/dashboard")
def admin_dashboard():
    if ('admin' in session):
        blogs = mongo.db.blogs.find({})
        return render_template('dashboard.html', blogs=blogs)
    else:
        return redirect(url_for('admin_login'))


@app.route("/admin/add", methods=["GET", "POST"])
def addpost():
    if ('admin' in session):
        if (request.method == "POST"):
            title = request.form.get("title")
            tagline = request.form.get("tagline")
            content = request.form.get("content")

            mongo.db.blogs.insert_one({ "title": title, "tagline": tagline, "content": content, "updatedAt": datetime.now(), "createdAt": datetime.now() })
            flash("Your post has been added successfully!", "success")
            return redirect(url_for('admin_dashboard'))

        return render_template("add.html")
    else:
        return redirect(url_for('admin_login'))
    
@app.route("/admin/edit/<ObjectId:id>", methods=["GET", "POST"])
def editpost(id):
    if ('admin' in session):
        if (request.method == "POST"):
            title = request.form.get("title")
            tagline = request.form.get("tagline")
            content = request.form.get("content")

            mongo.db.blogs.find_one_and_update({"_id": id}, {"$set": { "title": title, "tagline": tagline, "content": content, "updatedAt": datetime.now()}})
            flash("Your post has been updated successfully!", "success")
            return redirect(url_for('admin_dashboard'))

        blog = mongo.db.blogs.find_one_or_404(id)
        return render_template("edit.html", blog=blog)
    else:
        return redirect(url_for('admin_login'))
    
@app.route("/admin/delete/<ObjectId:id>", methods=["GET"])
def deletepost(id):
    if ('admin' in session):
        mongo.db.blogs.find_one_and_delete({"_id": id})
        mongo.db.comments.delete_many({"post": id})
        flash("Your post has been deleted successfully!", "success")
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('admin_login'))
    
@app.route("/admin/logout")
def admin_logout():
    if 'admin' in session:
        session.pop('admin')
        flash("You hav been logged out successfully!", "success")
        return redirect(url_for('admin_login'))