from flask import Flask, render_template, request, session, redirect, url_for, abort
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_humanize import Humanize
import os
import json

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
app.config["SECRET_KEY"] = os.getenv('APP_SECRET')
mongo = PyMongo(app)
humanize = Humanize(app)

with open("params.json", "r") as c:
    params = json.load(c)["params"]

from project.filters import get_val_filter
from project.routes import admin, auth, base, errors
