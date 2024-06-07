"""Flask app for Cupcakes"""
from flask import Flask, redirect, render_template, request
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# GET ROUTES --------------------------------------------------

@app.route("/")
def home():
    return 'Hi'