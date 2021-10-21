from flask import Flask, render_template, url_for, request, flash, redirect, abort, jsonify, json
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from sqlalchemy import func
import os
from urllib.parse import urlparse, urljoin
from sqlalchemy.sql.expression import union_all
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from wtforms import fields
from Forms import *
# from flask_migrate import Migrate
from Models import *
# migrate = Migrate(app, db)

app = Flask(__name__)
CORS(app)
SECRET_KEY = os.environ.get('SECRET_KEY') or '076f2ce915e884096c9ae907479b316e'
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\Backend jems\\dataBase\\jems_db.db'.format(os.getcwd())  # db file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disable the modification tracking system in Flask-SQLAlchemy
db = SQLAlchemy(app)  # Database
marshmallow = Marshmallow() # helper to json

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

class CalculateTipsSchema(marshmallow.Schema):
    class Meta:
        fields = ("date", "managers", "selected_shift", "total_cash", "total_credit", "total_hours",
                      "cash_per_hour", "credit_per_hour","total_tip", "names", "start_time","finish_time",
                      "total_waiter_time", "total_cash_waiter", "total_credit_waiter", "total_tip_waiter")

calculate_schema = CalculateTipsSchema()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@login_manager.user_loader
def load_user(user_id):  # since the user_id is just the primary key of our user table, use it in the query for the user
    return db.session.query(Employee).get(int(user_id))

@app.route('/Signup', methods=['GET', 'POST'])
def signup():
    certificates = {"current_user_auth": False, "user_already_exists": False, "register": False}
    if current_user.is_authenticated:
        certificates["current_user_auth"] = True
        return certificates
    # waiter_form = WaiterSignupForm()
    if request.method == 'POST':
        waiter_form = request.json
        if waiter_form["auth"] == "password-admin":
            # need to create validate func
            if waiter_form.validate_on_submit():
                newUser = Employee(email=waiter_form.email.data, waiter_name=waiter_form["waiter_name"],
                                 password=generate_password_hash(waiter_form["password"], method='sha256'),
                                 job_name=waiter_form["job_name"], age=waiter_form["age"],
                                 phone=waiter_form["phone"], location=waiter_form["location"])
                user = db.session.query(Employee).filter_by(name=newUser.waiter_name).first()
                if user is not None:
                    # flash("user Name already exists")
                    certificates["user_already_exists"] = True
                    return certificates
                user = db.session.query(Employee).filter_by(email=newUser.email).first()
                if user is not None:
                    # flash("Email address already exists")
                    certificates["user_already_exists"] = True
                    return certificates
                db.session.add(newUser)
                db.session.commit()
                # flash("Registration Successful!")
                certificates["register"] = True
                return certificates
        # else:
        #     flash("Auth Password is not Correct!")
    return {"current_user_auth": False, "user_already_exists": False, "register": False}


# @app.route('/Signup', methods=['GET', 'POST'])
# def signup():
#     if current_user.is_authenticated:
#         return redirect(url_for('jems_beer_calculate_page'))
#     waiter_form = WaiterSignupForm()
#     if request.method == 'POST':
#         if waiter_form.auth.data == "password-admin":
#             print(waiter_form.validate_on_submit())
#             if waiter_form.validate_on_submit():
#                 newUser = Waiter(email=waiter_form.email.data, waiter_name=waiter_form.waiter_name.data,
#                                  password=generate_password_hash(waiter_form.password.data, method='sha256'),
#                                  job_name=waiter_form.job_name.data, age=waiter_form.age.data,
#                                  phone=waiter_form.phone.data, location=waiter_form.location.data)
#                 user = db.session.query(Waiter).filter_by(name=newUser.waiter_name).first()
#                 if user is not None:
#                     flash("user Name already exists")
#                     return redirect(url_for('signup'))
#                 user = db.session.query(Waiter).filter_by(email=newUser.email).first()
#                 if user is not None:
#                     flash("Email address already exists")
#                     return redirect(url_for('signup'))
#                 db.session.add(newUser)
#                 db.session.commit()
#                 flash("Registration Successful!")
#                 return redirect(url_for('login'))
#         else:
#             flash("Auth Password is not Correct!")
#     return render_template('Sign_up.html', form=waiter_form)


@app.route('/Login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return {"msg": "already login"}
    if request.method == 'POST':
        login_details = request.json
        user = db.session.query(Employee).filter_by(email=login_details["email"]).first()
        if not user or not check_password_hash(user.password, login_details["password"]):
            return {"msg": False}
        else:
            login_user(user)
            next_page = request.args.get('next')
            if not is_safe_url(next_page):
                return abort(400)
            return {"msg": True}

    return {"msg": False}


# @app.route('/Login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('jems_beer_calculate_page'))
#     # formLogin = WaiterLoginForm()
#     if request.method == 'POST':
#         login_details = request.json
#         user = db.session.query(Employee).filter_by(email=login_details["email"]).first()
#         if not user or not check_password_hash(user.password, login_details["password"]):
#             flash('Please check your login details and try again')
#             return {"email": "", "password": ""}
#         if formLogin.validate_on_submit():
#             flash("Logged in successfully.")
#             login_user(user)
#             next_page = request.args.get('next')
#             if not is_safe_url(next_page):
#                 return abort(400)
#             return redirect(next_page) if next_page else redirect(url_for('jems_beer_calculate_page'))

#     return render_template('Login.html', form=formLogin)


# @app.route('/Logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))


# @app.route('/Account')
# @login_required
# def account():
#     return render_template('Account.html')


# @app.route('/About')
# def about():
#     return render_template('About_jems_tips.html')

@app.route('/CalculateTips/managers')
def get_managers():
    shift = Money
    managers = dict(db.session.query(Employee).filter(Employee.job_name == "manager").all())
    print(managers)
    return managers

@app.route('/CalculateTips', methods=['POST', 'GET'])
# @login_required
def jems_beer_calculate_page():
    # Create Models
    waiter = WaitersTable
    shift = Money
    managers_employees = db.session.query(Employee).filter(Employee.job_name == "manager").all()
    managers = []
    for employee in managers_employees:
        managers.append(employee.employee_name)
    data_lists = {"waiters": [], "waiters_name": [], "start_time_waiter": [], "finish_time_waiter": [],
    "total_waiter_time": [], "cash_waiter": [],"credit_waiter": [], "all_tips_waiters": []}
    if request.method == 'POST':
        page_details = request.json
        shift = Money(page_details["date"], page_details["manager"], page_details["selected_shift"],
                      0, page_details["total_cash"], page_details["total_credit"],
                      page_details["cash_per_hour"],
                      page_details["credit_per_hour"], page_details["total_tip"])
        shift.init_cash_credit_money()
        if shift.date != "" and shift.date is not None:
            shift.date = datetime.fromisoformat(shift.date)
        else:
            shift.date = None
        shift_exist = None
        if shift.date is not None:
            shift_exist = db.session.query(Money).filter(Money.date == shift.date.strftime("%Y-%m-%d"),
                                                     Money.selected_shift == shift.selected_shift).first()

        # Search max ID : Money, Waiter
        query_max_id_money = db.session.query(func.max(Money.id))
        last_id_money_db = query_max_id_money.scalar() or 0
        query_max_waiter_id = db.session.query(func.max(WaitersTable.id_waiter))
        last_waiter_id_db = query_max_waiter_id.scalar() or 1

        # INIT : The Waiters
        for i in range(0,len(page_details["names"])):
            last_waiter_id_db = last_waiter_id_db + 1
            waiter_time = page_details["total_waiter_time"][i]
            waiter = WaitersTable(
                last_waiter_id_db, page_details["names"][i], page_details["start_time"][i],
                page_details["finish_time"][i], waiter_time,
                page_details["total_cash_waiter"][i], page_details["total_credit_waiter"][i],
                page_details["total_tip_waiter"][i], last_id_money_db + 1)
            waiter.init_waiter(waiter_time, shift)
            addtolists(data_lists, waiter)
            
        # Update the last MAX ID for "waiters ID"
        last_waiter_id_db = query_max_waiter_id.scalar()

        # Calculate the Money table and Waiters table:
        calculate_page_data(shift, data_lists, page_details["names"])

        # SEND TO DB (database,"DB Browser (SQLite)"):
        update_tables_db(shift_exist, shift, data_lists["waiters"], last_waiter_id_db, last_id_money_db)
        # Serializable to json:
        for i in range(0, len(data_lists["start_time_waiter"])):
            data_lists["start_time_waiter"][i] = str(data_lists["start_time_waiter"][i])
            data_lists["finish_time_waiter"][i] = str(data_lists["finish_time_waiter"][i])
        page = Page(shift.date, managers, shift.selected_shift, shift.total_cash, shift.total_credit,
         shift.total_hours, shift.cash_per_hour, shift.credit_per_hour,shift.total_tip, data_lists["waiters_name"],
         data_lists["start_time_waiter"], data_lists["finish_time_waiter"], data_lists["total_waiter_time"], 
         data_lists["cash_waiter"], data_lists["credit_waiter"], data_lists["all_tips_waiters"])
        print("Page: ", type(page), ", Details: ", page)
        page_json = calculate_schema.dump(page)

        return jsonify(page_json)
        
    # send to html:
    page = Page(None, managers, "morning", "", "", "", "", "", "",
    ["", "", "", "","", "", "", "","", "", "", ""], ["", "", "", "","", "", "", "","", "", "", ""], 
    ["", "", "", "","", "", "", "","", "", "", ""], ["", "", "", "","", "", "", "","", "", "", ""], 
    ["", "", "", "","", "", "", "","", "", "", ""], ["", "", "", "","", "", "", "","", "", "", ""], 
    ["", "", "", "","", "", "", "","", "", "", ""])
    page_json = calculate_schema.dump(page)
    print("page_json respone('GET'):", page_json)
    return jsonify(page_json)

@app.route('/ShiftsLog', methods=['GET', 'POST'])
# @login_required
def show_date_tips_page():
    report_details = "empty"
    # INIT Waiter Model
    waiter_model = WaitersTable
    data_lists = {"waiters": [], "waiters_name": [], "start_time_waiter": [], "finish_time_waiter": [],
    "total_waiter_time": [], "total_cash_waiter": [],"total_credit_waiter": [], "total_tips_waiter": []}
    init_waiter_model(waiter_model)
    if request.method == 'POST':
        data = request.json
        print(data)
        if data["shift"] is None or data["shift"] == '':  # default shift
            data["shift"] = "morning"

        # While click "Search"
        if request.method == 'POST':
            report_details = "detail-not exist"
            if data["date"] == '':
                return {"shift": "", "date": "", "data_exist": False,"msg": "you did not insert a date."}

            # Search the Date shift in DB
            money_shift = Money.query.filter_by(date=datetime.fromisoformat(data["date"]).date()).first()
            # Date exist:
            if money_shift is not None:
                if money_shift.date == datetime.fromisoformat(data["date"]).date():
                    if money_shift.selected_shift == data["shift"]:
                        waiters = WaitersTable.query.filter_by(shift_id=money_shift.id).all()
                        for waiter in waiters:
                            insert_waiter(data_lists, waiter)
                        report_details = "detail-exist"

                        page = Page(data["date"], money_shift.manager, data["shift"], money_shift.total_cash, money_shift.total_credit,
                        money_shift.total_hours, money_shift.cash_per_hour, money_shift.credit_per_hour,money_shift.total_tip, data_lists["waiters_name"],
                        data_lists["start_time_waiter"], data_lists["finish_time_waiter"], data_lists["total_waiter_time"], 
                        data_lists["total_cash_waiter"], data_lists["total_credit_waiter"], data_lists["total_tips_waiter"])
                        page_json = calculate_schema.dump(page)
                        union_shift_data = dict(page_json, **({"shift_exist": True, "msg": "Shift found", "shift": "morning"})) 
                        print(union_shift_data)
                        return jsonify(union_shift_data)

    if report_details == "detail-not exist":
        return {"shift_exist": "detail-not exist", "msg": "Shift did not found", "date": "", "shift": "morning"}

    return {"shift_exist": False, "msg": "", "date": "", "shift": "morning"}


# def init_start_page(money, waiter):
#     time_zero = datetime(1, 1, 1).time()
#     money.manager = ''
#     money.total_cash = ''
#     money.total_credit = ''
#     money.total_hours = ''
#     money.cash_per_hour = ''
#     money.credit_per_hour = ''
#     money.total_tip = ""
#     waiter.name = ''
#     waiter.total_waiter_time = 0
#     waiter.start_time_waiter = time_zero
#     waiter.finish_time_waiter = time_zero

def addtolists(data_lists, waiter):
    data_lists["waiters"].append(waiter)
    data_lists["waiters_name"].append(waiter.name)
    data_lists["start_time_waiter"].append(waiter.start_time)
    data_lists["finish_time_waiter"].append(waiter.finish_time)
    data_lists["total_waiter_time"].append(waiter.total_waiter_time)

# Insert into the Waiter Model lists #
def insert_waiter(data_lists, waiter):
    data_lists["waiters_name"].append(waiter.name)
    data_lists["start_time_waiter"].append(waiter.start_time.strftime("%H:%M"))
    data_lists["finish_time_waiter"].append(waiter.finish_time.strftime("%H:%M"))
    data_lists["total_waiter_time"].append(waiter.total_waiter_time)
    data_lists["total_cash_waiter"].append(waiter.total_cash_waiter)
    data_lists["total_credit_waiter"].append(waiter.total_credit_waiter)
    data_lists["total_tips_waiter"].append(waiter.total_tip_waiter)


# INIT Waiter Model
def init_waiter_model(waiter_model):
    waiter_model.waiters_name = []
    waiter_model.start_time_waiter_list = []
    waiter_model.finish_time_waiter_list = []
    waiter_model.total_waiter_time_list = []
    waiter_model.cash_waiter_list = []
    waiter_model.credit_waiter_list = []
    waiter_model.all_tips_waiters_list = []


def calculate_page_data(shift, data_lists, names):
    # Money Table: Calculate the cash per hour, credit per hour, total tip:    
    if shift.total_hours > 0:
        shift.calculate_money()
    shift.total_tip = round(float(shift.cash_per_hour) + float(shift.credit_per_hour), 3)

    # Waiters Table: Calculate the cash and credit for each waiter:
    for i in range(len(names)):
        data_lists["waiters"][i].calculate_tip_each_waiter(shift, data_lists)


def update_tables_db(shift_exist, shift, waiters, last_waiter_id_db, last_id_money_db):
    if shift_exist is not None:  # --- Update exist data in the DB --- :
        # Update Money table:
        print(shift.manager)
        db.session.query(Money).filter(Money.date == shift.date.strftime("%Y-%m-%d"),
                                       Money.selected_shift == shift.selected_shift).update(
            {"id": str(last_id_money_db + 1),"date": shift.date, "manager": shift.manager,
            "selected_shift": shift.selected_shift, "total_hours": str(shift.total_hours),
             "total_cash": str(shift.total_cash), "total_credit": str(shift.total_credit),
             "cash_per_hour": str(shift.cash_per_hour), "credit_per_hour": str(shift.credit_per_hour),
             "total_tip": str(round(shift.total_tip, 2))})
        # --- Update WaiterTable --- :
        shift_exist_updated = db.session.query(Money).filter(Money.date == shift.date.strftime("%Y-%m-%d"),
                                                             Money.selected_shift == shift.selected_shift).first()
        # 1.Delete last waiters
        db.session.query(WaitersTable).filter(WaitersTable.shift_id == shift_exist.id).delete(
            synchronize_session="fetch")
        shift_exist_Waiters_table = db.session.query(WaitersTable).filter(WaitersTable.shift_id == shift_exist.id) \
            .first()
        # 2.Insert new waiters
        if shift_exist_Waiters_table is None:
            for w in waiters:
                if w.name != '':
                    db.session.add(w)
        else:  # Update the id of the shift
            db.session.query(WaitersTable).filter(WaitersTable.shift_id == shift_exist.id).update(
                {"shift_id": shift_exist_updated.id})
        db.session.commit()

    else:  # Create new Column in the DB
        day_tip = [Money(date=shift.date, manager=shift.manager, selected_shift=shift.selected_shift,
                         total_hours=shift.total_hours, total_cash=shift.total_cash,
                         total_credit=shift.total_credit, cash_per_hour=shift.cash_per_hour,
                         credit_per_hour=shift.credit_per_hour, total_tip=round(shift.total_tip, 3))]
        for y in day_tip:
            db.session.add(y)
        db.session.commit()
        for w in waiters:
            if w.name != '':
                last_waiter_id_db = last_waiter_id_db + 1
                db.session.add(w)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
