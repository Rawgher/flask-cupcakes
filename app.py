"""Flask app for Cupcakes"""
from flask import Flask, jsonify, redirect, render_template, request
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

@app.route("/api/cupcakes")
def list_cupcakes():
    """Return JSON with information for all cupcakes"""
    all_ccs = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_ccs)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Return JSON with information for a specific cupcake"""
    this_cc = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=this_cc.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    """Add a cupcake to the db and respond with JSON"""
    new_cc = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=request.json.get('image') or None)
    db.session.add(new_cc)
    db.session.commit()

    return (jsonify(cupcake=new_cc.serialize()), 201)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Find a cupcake to update it in the db and respond with JSON"""
    this_cc = Cupcake.query.get_or_404(id)
    this_cc.flavor = request.json.get('flavor', this_cc.flavor)
    this_cc.size = request.json.get('size', this_cc.size)
    this_cc.rating = request.json.get('rating', this_cc.rating)
    this_cc.image = request.json.get('image', this_cc.image)
    db.session.commit()

    return jsonify(cupcake=this_cc.serialize())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Find a cupcake and delete it from the db"""
    this_cc = Cupcake.query.get_or_404(id)
    db.session.delete(this_cc)
    db.session.commit()

    return jsonify(message="deleted")