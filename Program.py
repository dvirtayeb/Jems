from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
import os
from Forms import WaiterForm
from flask_migrate import Migrate
import Models

app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY') or '076f2ce915e884096c9ae907479b316e'
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\dataBase\\jems_db.db'.format(os.getcwd())  # db file
db = SQLAlchemy(app)  # Database
migrate = Migrate(app, db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/form_waiter1/', methods=['GET', 'POST'])
def form_new_waiter():
    waiter_form = WaiterForm()
    new_waiter = [Models.Waiters(waiter_name=waiter_form.waiter_name.data, job_name=waiter_form.job_name.data,
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


@app.route('/')
def jems_beer():
    # reset_waiter = ResetWaiter()
    waiter = Models.WaitersTable
    money = Models.Money
    time_zero = datetime(1, 1, 1).time()
    money.total_cash = 0
    money.total_credit = 0
    money.cash_per_hour = ''
    money.credit_per_hour = ''
    money.total_tip = ''
    waiter.name = ''
    waiter.total_waiter_time = 0
    waiter.start_time_waiter = time_zero
    waiter.finish_time_waiter = time_zero
    waiter.cash_waiter_list = []
    waiter.credit_waiter_list = []
    waiter.all_tips_waiters_list = []
    return render_template("jems-tips1.html", waiters=[], name='', start_time='', finish_time='',
                           total_waiter_time='', total_cash_waiter='', total_credit_waiter='',
                           total_tips='')


@app.route('/', methods=['POST', 'GET'])
def jems_beer_update():
    waiter = Models.WaitersTable
    shift = Models.Money
    date = None
    if request.method == 'POST':
        date = request.form.get('date_shift')
        manager = request.form.get('manager')
        selected_shift = request.form.get('shift')
        total_cash = request.form.get('total_cash')
        total_credit = request.form.get('total_credit')
        names = request.form.getlist('name')
        start_time_waiter = request.form.getlist('start_time')
        finish_time_waiter = request.form.getlist('finish_time')
        total_waiter_time = request.form.getlist('total_time')
        total_cash_waiter = 0
        total_credit_waiter = 0
        total_tip_waiter = 0
        total_hours = 0
        cash_per_hour = 0
        credit_per_hour = 0
        total_tip = 0

        shift = Models.Money(date, manager, selected_shift, total_hours, total_cash, total_credit, cash_per_hour,
                             credit_per_hour, total_tip)
        shift.init_cash_credit_money()
        if shift.date != "":
            shift.date = datetime.fromisoformat(shift.date)
        else:
            flash("There is no date!")
            shift.date = None
        query_max_id_money = db.session.query(func.max(Models.Money.id))
        last_id_money_db = query_max_id_money.scalar() or 0
        query_max_waiter_id = db.session.query(func.max(Models.WaitersTable.id_waiter))
        last_waiter_id_db = query_max_waiter_id.scalar() or 1
        for i in range(len(names)):
            last_waiter_id_db = last_waiter_id_db + 1
            waiter = Models.WaitersTable(
                last_waiter_id_db, names[i], datetime.strptime(start_time_waiter[i], '%H:%M').time(), datetime.strptime(
                    finish_time_waiter[i], '%H:%M').time(), total_waiter_time[i], total_cash_waiter,
                total_credit_waiter, total_tip_waiter, last_id_money_db + 1)
            waiter.init_waiter(waiter, shift)
        last_waiter_id_db = query_max_waiter_id.scalar()
        # Calculate the cash per hour, credit per hour, total tip:
        if shift.total_hours > 0:
            shift.calculate_money()
        shift.total_tip = shift.cash_per_hour + shift.credit_per_hour
        # Calculate the cash and credit for each waiter:
        for i in range(len(names)):
            waiter.waiters[i].calculate_tip_each_waiter(shift)
        # send to db (database,"DB Browser (SQLite)"):
        day_tip = [Models.Money(date=shift.date, manager=shift.manager, selected_shift=shift.selected_shift,
                                total_hours=shift.total_hours, total_cash=shift.total_cash,
                                total_credit=shift.total_credit, cash_per_hour=shift.cash_per_hour,
                                credit_per_hour=shift.credit_per_hour, total_tip=round(shift.total_tip, 3))]
        for y in day_tip:
            db.session.add(y)
        db.session.commit()
        # print(waiters)
        for w in waiter.waiters:
            if w.name != '':
                print(w)
                last_waiter_id_db = last_waiter_id_db + 1
                db.session.add(w)
        db.session.commit()
    # send to html:
    return render_template('Jems-tips1.html', date_shift=date, manager=shift.manager,
                           selected_shift=shift.selected_shift, total_hours=shift.total_hours,
                           total_cash=shift.total_cash, total_credit=shift.total_credit,
                           cash_per_hour=shift.cash_per_hour,
                           credit_per_hour=shift.credit_per_hour, total_tip=round(shift.total_tip, 3),
                           name=waiter.waiters_name, start_time=waiter.start_time_waiter_list,
                           finish_time=waiter.finish_time_waiter_list, total_waiter_time=waiter.total_waiter_time_list,
                           total_cash_waiter=waiter.cash_waiter_list, total_credit_waiter=waiter.credit_waiter_list,
                           total_tips=waiter.all_tips_waiters_list
                           )


@app.route('/Date_Page', methods=['GET', 'POST'])
def show_date_tips_page():
    counter_w = 0
    report = "empty"
    waiter_model = Models.WaitersTable
    waiter_model.waiters_name = []
    waiter_model.start_time_waiter_list = []
    waiter_model.finish_time_waiter_list = []
    waiter_model.total_waiter_time_list = []
    waiter_model.cash_waiter_list = []
    waiter_model.credit_waiter_list = []
    waiter_model.all_tips_waiters_list = []
    show_date = request.form.get('show_date')
    shift = request.form.get('shift')
    if shift is None or shift == '':
        shift = "morning"
    if request.method == 'POST':
        report = "detail-not exist"
        if show_date == '':
            flash("You didn't insert a Date")
            return render_template('Date_Page.html', show_date=show_date, report=report)
        money_shift = Models.Money.query.filter_by(date=datetime.fromisoformat(show_date).date()).first()
        if money_shift is None:
            flash("Didn't found a Date")
            return render_template('Date_Page.html', show_date=show_date, report=report)
        if money_shift.date == datetime.fromisoformat(show_date).date():
            if money_shift.selected_shift == shift:
                waiters = Models.WaitersTable.query.filter_by(shift_id=money_shift.id).all()
                for waiter in waiters:
                    waiter_model.waiters_name.append(waiter.name)
                    waiter_model.start_time_waiter_list.append(waiter.start_time_waiter.strftime("%H:%M"))
                    waiter_model.finish_time_waiter_list.append(waiter.finish_time_waiter.strftime("%H:%M"))
                    waiter_model.total_waiter_time_list.append(waiter.total_waiter_time)
                    waiter_model.cash_waiter_list.append(waiter.total_cash_waiter)
                    waiter_model.credit_waiter_list.append(waiter.total_credit_waiter)
                    waiter_model.all_tips_waiters_list.append(waiter.total_tip_waiter)
                report = "detail-exist"
                return render_template('Date_Page.html', show_date=show_date, shift=shift, report=report,
                                       show_manager=money_shift.manager, show_selected_shift=money_shift.selected_shift,
                                       total_hours=money_shift.total_hours, total_cash=money_shift.total_cash,
                                       total_credit=money_shift.total_credit, cash_per_hour=money_shift.cash_per_hour,
                                       credit_per_hour=money_shift.credit_per_hour, total_tip=money_shift.total_tip,
                                       id=counter_w, name=waiter_model.waiters_name,
                                       start_time=waiter_model.start_time_waiter_list,
                                       finish_time=waiter_model.finish_time_waiter_list,
                                       total_waiter_time=waiter_model.total_waiter_time_list,
                                       total_cash_waiter=waiter_model.cash_waiter_list,
                                       total_credit_waiter=waiter_model.credit_waiter_list,
                                       total_tips=waiter_model.all_tips_waiters_list)

    if report == "detail-not exist":
        flash(" Didn't found a shift")
        # print(money_shift)
    return render_template('Date_Page.html', show_date=show_date, report=report)


# reset the app:
if __name__ == '__main__':
    app.run(debug=True)
