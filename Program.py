from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
import os
from Forms import WaiterForm
from flask_migrate import Migrate
from Models import *

app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY') or '076f2ce915e884096c9ae907479b316e'
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\dataBase\\jems_db.db'.format(os.getcwd())  # db file
db = SQLAlchemy(app)  # Database
# migrate = Migrate(app, db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disable the modification tracking system in Flask-SQLAlchemy


@app.route('/form_waiter1/', methods=['GET', 'POST'])
def form_new_waiter():
    waiter_form = WaiterForm()
    new_waiter = [Waiters(waiter_name=waiter_form.waiter_name.data, job_name=waiter_form.job_name.data,
                          age=waiter_form.age.data, location=waiter_form.location.data,
                          phone=waiter_form.phone.data)]
    if waiter_form.validate_on_submit():
        flash('The waiter has registered successfully')
        # add to db:
        for w in new_waiter:
            db.session.add(w)
        db.session.commit()
        return redirect(url_for('form_new_waiter'))
    if waiter_form.waiter_name.data == "":
        flash("You didn't insert a name!")
    if waiter_form.job_name.data == "":
        flash("You didn't insert a job name!")
    return render_template('form_waiter1.html', form=waiter_form)


@app.route('/about/')
def about():
    return render_template('About_jems_tips.html')


@app.route('/', methods=['POST', 'GET'])
def jems_beer_calculate_page():
    # Create Models
    waiter = WaitersTable
    shift = Money
    date = None  # Default
    if request.method == 'POST':
        # Request the data of first table: Money
        shift_dict = {"date": request.form.get('date_shift'), "manager": request.form.get('manager'),
                      "selected_shift": request.form.get('shift'), "total_cash": request.form.get('total_cash'),
                      "total_credit": request.form.get('total_credit'), "total_tip": 0, "total_hours": 0,
                      "cash_per_hour": 0, "credit_per_hour": 0}
        # Request the data of first table: WaiterTable
        waiters_dict = {"names": request.form.getlist('name'), "start_time_Waiter": request.form.getlist('start_time'),
                        "finish_time_waiter": request.form.getlist('finish_time'),
                        "total_waiter_time": request.form.getlist('total_time'), "total_cash_waiter": 0,
                        "total_credit_waiter": 0, "total_tip_waiter": 0}

        # INIT : The Money in the shift
        shift = Money(shift_dict["date"], shift_dict["manager"], shift_dict["selected_shift"],
                      shift_dict["total_hours"], shift_dict["total_cash"], shift_dict["total_credit"],
                      shift_dict["cash_per_hour"],
                      shift_dict["credit_per_hour"], shift_dict["total_tip"])
        shift.init_cash_credit_money()
        if shift.date != "":
            shift.date = datetime.fromisoformat(shift.date)
        else:
            flash("There is no date!")
            shift.date = None

        shift_exist = db.session.query(Money).filter(Money.date == shift.date.strftime("%Y-%m-%d"),
                                                     Money.selected_shift == shift.selected_shift).first()

        # Search max ID : Money, Waiter
        query_max_id_money = db.session.query(func.max(Money.id))
        last_id_money_db = query_max_id_money.scalar() or 0
        query_max_waiter_id = db.session.query(func.max(WaitersTable.id_waiter))
        last_waiter_id_db = query_max_waiter_id.scalar() or 1

        # INIT : The Waiters
        for i in range(len(waiters_dict.get("names"))):
            last_waiter_id_db = last_waiter_id_db + 1
            waiter = WaitersTable(
                last_waiter_id_db, waiters_dict["names"][i], waiters_dict["start_time_Waiter"][i],
                waiters_dict["finish_time_waiter"][i], waiters_dict["total_waiter_time"][i],
                waiters_dict["total_cash_waiter"], waiters_dict["total_credit_waiter"],
                waiters_dict["total_tip_waiter"], last_id_money_db + 1)
            waiter.init_waiter(waiter, shift)

        # Update the last MAX ID for "waiters ID"
        last_waiter_id_db = query_max_waiter_id.scalar()

        # Calculate the Money table and Waiters table:
        calculateTipPageData(shift, waiter, waiters_dict["names"])

        # SEND TO DB (database,"DB Browser (SQLite)"):
        update_db(shift_exist, shift, waiter, last_waiter_id_db, last_id_money_db)
    # send to html:
    else:
        init_start_page(shift, waiter)

    return render_template('Jems-tips1.html', date_shift=date, manager=shift.manager,
                           selected_shift=shift.selected_shift, total_hours=shift.total_hours,
                           total_cash=shift.total_cash, total_credit=shift.total_credit,
                           cash_per_hour=shift.cash_per_hour,
                           credit_per_hour=shift.credit_per_hour, total_tip=shift.total_tip,
                           name=waiter.waiters_name, start_time=waiter.start_time_waiter_list,
                           finish_time=waiter.finish_time_waiter_list, total_waiter_time=waiter.total_waiter_time_list,
                           total_cash_waiter=waiter.cash_waiter_list, total_credit_waiter=waiter.credit_waiter_list,
                           total_tips=waiter.all_tips_waiters_list
                           )


@app.route('/Date_Page', methods=['GET', 'POST'])
def show_date_tips_page():
    counter_w = 0
    report_details = "empty"
    # INIT Waiter Model
    waiter_model = WaitersTable
    init_waiter_model(waiter_model)
    show_date = request.form.get('show_date')  # get date
    shift = request.form.get('shift')  # get Morning / Evening shift

    if shift is None or shift == '':  # default shift
        shift = "morning"

    # While click "Search"
    if request.method == 'POST':
        report_details = "detail-not exist"
        if show_date == '':
            flash("You didn't insert a Date")
            return render_template('Date_Page.html', show_date=show_date, report_details=report_details)

        # Search the Date shift in DB
        money_shift = Money.query.filter_by(date=datetime.fromisoformat(show_date).date()).first()

        # Date exist:
        if money_shift is not None:
            if money_shift.date == datetime.fromisoformat(show_date).date():
                if money_shift.selected_shift == shift:
                    waiters = WaitersTable.query.filter_by(shift_id=money_shift.id).all()
                    for waiter in waiters:
                        insert_waiter(waiter_model, waiter)
                    report_details = "detail-exist"
                    return render_template('Date_Page.html', show_date=show_date, shift=shift,
                                           report_details=report_details,
                                           show_manager=money_shift.manager,
                                           show_selected_shift=money_shift.selected_shift,
                                           total_hours=money_shift.total_hours,
                                           total_cash=money_shift.total_cash,
                                           total_credit=money_shift.total_credit,
                                           cash_per_hour=money_shift.cash_per_hour,
                                           credit_per_hour=money_shift.credit_per_hour, total_tip=money_shift.total_tip,
                                           id=counter_w, name=waiter_model.waiters_name,
                                           start_time=waiter_model.start_time_waiter_list,
                                           finish_time=waiter_model.finish_time_waiter_list,
                                           total_waiter_time=waiter_model.total_waiter_time_list,
                                           total_cash_waiter=waiter_model.cash_waiter_list,
                                           total_credit_waiter=waiter_model.credit_waiter_list,
                                           total_tips=waiter_model.all_tips_waiters_list)

    if report_details == "detail-not exist":
        flash(" Didn't found a shift")

    return render_template('Date_Page.html', show_date=show_date, report_details=report_details)


def init_start_page(money, waiter):
    time_zero = datetime(1, 1, 1).time()
    money.manager = ''
    money.total_cash = ''
    money.total_credit = ''
    money.total_hours = ''
    money.cash_per_hour = ''
    money.credit_per_hour = ''
    money.total_tip = ""
    waiter.name = ''
    waiter.total_waiter_time = 0
    waiter.start_time_waiter = time_zero
    waiter.finish_time_waiter = time_zero
    waiter.cash_waiter_list = []
    waiter.credit_waiter_list = []
    waiter.all_tips_waiters_list = []


# Insert into the Waiter Model lists #
def insert_waiter(waiter_model, waiter):
    waiter_model.waiters_name.append(waiter.name)
    waiter_model.start_time_waiter_list.append(waiter.start_time_waiter.strftime("%H:%M"))
    waiter_model.finish_time_waiter_list.append(waiter.finish_time_waiter.strftime("%H:%M"))
    waiter_model.total_waiter_time_list.append(waiter.total_waiter_time)
    waiter_model.cash_waiter_list.append(waiter.total_cash_waiter)
    waiter_model.credit_waiter_list.append(waiter.total_credit_waiter)
    waiter_model.all_tips_waiters_list.append(waiter.total_tip_waiter)


# INIT Waiter Model
def init_waiter_model(waiter_model):
    waiter_model.waiters_name = []
    waiter_model.start_time_waiter_list = []
    waiter_model.finish_time_waiter_list = []
    waiter_model.total_waiter_time_list = []
    waiter_model.cash_waiter_list = []
    waiter_model.credit_waiter_list = []
    waiter_model.all_tips_waiters_list = []


def calculateTipPageData(shift, waiter, names):
    # Money Table: Calculate the cash per hour, credit per hour, total tip:
    if shift.total_hours > 0:
        shift.calculate_money()
    shift.total_tip = round(shift.cash_per_hour + shift.credit_per_hour, 3)
    # Waiters Table: Calculate the cash and credit for each waiter:
    for i in range(len(names)):
        waiter.waiters[i].calculate_tip_each_waiter(shift)


def update_db(shift_exist, shift, waiter, last_waiter_id_db, last_id_money_db):
    # --- Update exist data in the DB --- :
    if shift_exist is not None:
        # Update Money table:
        db.session.query(Money).filter(Money.date == shift.date.strftime("%Y-%m-%d"),
                                       Money.selected_shift == shift.selected_shift).update(
            {"id": str(last_id_money_db + 1), "manager": shift.manager, "total_hours": str(shift.total_hours),
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
            for w in waiter.waiters:
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
        for w in waiter.waiters:
            if w.name != '':
                last_waiter_id_db = last_waiter_id_db + 1
                db.session.add(w)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
