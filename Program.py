from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
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
    if waiter_form.validate_on_submit():
        flash('The waiter has registered successfully')
        return redirect(url_for('form_new_waiter'))
    return render_template('form_waiter1.html', form=waiter_form)


@app.route('/about/')
def about():
    return render_template('About_jems_tips.html')


@app.route('/')
def jems_beer():
    # total_hours = 0
    Models.Money.total_cash = 0
    Models.Money.total_credit = 0
    Models.Money.cash_per_hour = ''
    Models.Money.credit_per_hour = ''
    Models.Money.total_tip = ''
    Models.WaitersTable.name = []
    Models.WaitersTable.total_waiter_time = []
    Models.WaitersTable.start_time_waiter = []
    Models.WaitersTable.finish_time_waiter = []
    Models.WaitersTable.cash_waiter_list = []
    Models.WaitersTable.credit_waiter_list = []
    Models.WaitersTable.all_tips_waiters_list = []
    return render_template("jems-tips1.html", waiters=[],
                           name='',
                           start_time='',
                           finish_time='',
                           total_waiter_time='',
                           total_cash_waiter='',
                           total_credit_waiter='',
                           total_tips='')


@app.route('/', methods=['POST', 'GET'])
def jems_beer_update():
    counter = 0
    waiter = Models.WaitersTable
    money = Models.Money
    if request.method == 'POST':
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
        # Objects:
        money = Models.Money(total_hours, total_cash, total_credit, cash_per_hour, credit_per_hour, total_tip)
        # Set the total cash, total credit:
        money.set_total_cash_shift()
        money.set_total_credit_shift()
        for i in range(len(names)):
            counter = counter + 1
            waiter = Models.WaitersTable(counter, names[i], start_time_waiter[i], finish_time_waiter[i],
                                         total_waiter_time[i], total_cash_waiter, total_credit_waiter, total_tip_waiter)
            # check for all waiters if we got time and set the time to 00:00 if not:
            waiter.set_start_time_zero()
            waiter.set_finish_time_zero()
            # set hour time to 0 if we don't have it from the user
            waiter.set_total_time_waiter_zero()
            money.sum_total_hours(waiter.total_waiter_time)
            # arrayList of Waiters name:
            waiter.add_to_list_name()
            waiter.add_to_list_start_time()
            waiter.add_to_list_finish_time()
            waiter.add_to_list_total_waiter()
            waiter.waiters.append(waiter)

        # Calculate the cash per hour, credit per hour, total tip:
        if money.total_hours > 0:
            money.calculate_cash_per_hour()
            money.calculate_credit_per_hour()
        money.total_tip = money.cash_per_hour + money.credit_per_hour
        # Calculate the cash and credit for each waiter:
        for i in range(len(names)):
            waiter.waiters[i].calculate_tip_each_waiter(money)
        # send to db (database,"DB Browser (SQLite)"):
        day_tip = [Models.Money(total_hours=money.total_hours, total_cash=money.total_cash,
                                total_credit=money.total_credit, cash_per_hour=money.cash_per_hour,
                                credit_per_hour=money.credit_per_hour, total_tip=money.total_tip)]
        for y in day_tip:
            db.session.add(y)
        db.session.commit()
        # print(waiters)
        for waiter in waiter.waiters:
            print(waiter)
            if waiter.name != '':
                db.session.add(waiter)
            db.session.commit()
    # send to html:
    return render_template('Jems-tips1.html',
                           total_hours=money.total_hours,
                           total_cash=money.total_cash,
                           total_credit=money.total_credit,
                           cash_per_hour=money.cash_per_hour,
                           credit_per_hour=money.credit_per_hour,
                           total_tip=money.total_tip,
                           name=waiter.waiters_name,
                           start_time=waiter.start_time_waiter_list,
                           finish_time=waiter.finish_time_waiter_list,
                           total_waiter_time=waiter.total_waiter_time_list,
                           total_cash_waiter=waiter.cash_waiter_list,
                           total_credit_waiter=waiter.credit_waiter_list,
                           total_tips=waiter.all_tips_waiters_list
                           )


# reset the app:
if __name__ == '__main__':
    app.run(debug=True)
