from flask import Blueprint, render_template, redirect, url_for, request, flash
from .Program import db, app
from .Models import Employee
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/Login')
def login():
    return render_template('Login.html')


@app.route('/Signup', methods=['POST'])
def signup():
    email = request.form.get('Email')
    name = request.form.get('Name')
    password = request.form.get('Password')
    job_name = request.form.get('Job')
    age = request.form.get('Age')
    phone = request.form.get('Phone')
    location = request.form.get('Location')

    user = db.session.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists")
        return redirect(url_for('signup'))
    newUser = Employee(email=email, employee_name=name, password=generate_password_hash(password, method='sha256'),
                     job_name=job_name, age=age, phone=phone, location=location)
    db.session.add(newUser)
    db.session.commit()
    return redirect(url_for('app.login'))
