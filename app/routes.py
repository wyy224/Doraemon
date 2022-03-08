import logging
import os
from sqlalchemy import true, false

import calendar
from datetime import datetime
from flask import render_template, redirect, flash, url_for, session, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db, Config
#from app.forms import LoginForm, SignupForm, YearForm, UpdateForm
#from app.models import User, Notes

#logger = logging.getLogger(__name__)
@app.route('/')
def base():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/icon')
def icon():
    return render_template('icon.html')
@app.route('/product')
def product():
    return render_template('product.html')
@app.route('/service')
def service():
    return render_template('service.html')
@app.route('/typography')
def typography():
    return render_template('typography.html')