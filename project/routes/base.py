from project import app, mongo, params
from flask import render_template, request, redirect, url_for, session, abort, flash
from bson import ObjectId
from datetime import datetime
import math

@app.route("/")
def home():
    blogs = []
    limit = int(params["limit"])

    if (request.args.get('page')):
        page = int(request.args.get('page'))
    else:
        page = 1

    count = 0
    for i in mongo.db.blogs.find({}):
        blogs.append(i)
        count += 1

    blogs = blogs[(page-1)*limit: page*limit]
    totalPages = math.ceil(count / limit)
    
    if (page > 1):
        prev = page - 1
    else:
        prev = None

    if (page < totalPages):
        nxt = page + 1
    else:
        nxt = None

    return render_template("index.html", blogs=blogs, count=count, totalPages=totalPages, page=page, nxt=nxt, prev=prev)

@app.route("/post/<ObjectId:id>")
def post(id):
    blog = mongo.db.blogs.find_one_or_404(id)
    nxtBlog = mongo.db.blogs.find_one({"createdAt": {
        "$gt": blog['createdAt']
    }})
    prevBlog = mongo.db.blogs.find_one({"createdAt": {
        "$lt": blog['createdAt']
    }})
    comments = []
    replies = []
    comments_count = 0
    for i in mongo.db.comments.find({ "post": blog['_id'] }):
        if i['parent'] is None:
            comments.append({
                '_id': i['_id'],
                'comment': i['comment'],
                'user': mongo.db.users.find_one({"_id": i['user']})['username'],
                'createdAt': i['createdAt']
            })
            comments_count += 1
        else:
            replies.append({
                '_id': i['_id'],
                'comment': i['comment'],
                'parent': i['parent'],
                'user': mongo.db.users.find_one({"_id": i['user']})['username'],
                'createdAt': i['createdAt']
            })
    repDict = {}

    for reply in replies:
        if reply['parent'] not in repDict:
            repDict[reply['parent']] = [reply]
        else:
            repDict[reply['parent']].append(reply)

    return render_template("post.html", blog=blog, comments=comments, repDict=repDict, comments_count=comments_count, nxtBlog=nxtBlog, prevBlog=prevBlog)

@app.route("/search")
def search_page():
    query = request.args.get('query')
    if (query):
        blogs = []
        limit = int(params["limit"])

        if (request.args.get('page')):
            page = int(request.args.get('page'))
        else:
            page = 1

        count = 0
        for i in mongo.db.blogs.find({"title": {
            "$regex": query,
            "$options": 'i'
        }}):
            blogs.append(i)
            count += 1

        blogs = blogs[(page-1)*limit: page*limit]
        totalPages = math.ceil(count / limit)
        
        if (page > 1):
            prev = page - 1
        else:
            prev = None

        if (page < totalPages):
            nxt = page + 1
        else:
            nxt = None

        return render_template("search.html", blogs=blogs, count=count, totalPages=totalPages, page=page, nxt=nxt, prev=prev, query=query)
    else:
        return redirect(url_for('home'))
    
@app.route("/addcomment", methods=["POST"])
def handle_comment_add():
    if 'user' in session:
        parent = request.form.get("parent")
        post = request.form.get("post")
        path = request.form.get("path")
        comment = request.form.get("comment")

        if not parent:
            mongo.db.comments.insert_one({
                "parent": request.path,
                "post": ObjectId(post),
                "user": ObjectId(session['userID']),
                "parent": None,
                "comment": comment,
                "createdAt": datetime.now()
            })
            flash("Your comment has been posted successfully!", "success")
            return redirect(path)
        else:
            mongo.db.comments.insert_one({
                "parent": request.path,
                "post": ObjectId(post),
                "user": ObjectId(session['userID']),
                "parent": ObjectId(parent),
                "comment": comment,
                "createdAt": datetime.now()
            })
            flash("Your reply has been posted successfully!", "success")
            return redirect(path)  
    else:
        abort(401)
