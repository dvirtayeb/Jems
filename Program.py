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
    waiter = Models.WaitersTable
    shift = Models.Money
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

        shift = Models.Money(total_hours, total_cash, total_credit, cash_per_hour, credit_per_hour, total_tip)
        shift.init_money()
        for i in range(len(names)):
            waiter = Models.WaitersTable(i+1, names[i], start_time_waiter[i], finish_time_waiter[i],
                                         total_waiter_time[i], total_cash_waiter, total_credit_waiter, total_tip_waiter)
            waiter.init_waiter(waiter, shift)

        # Calculate the cash per hour, credit per hour, total tip:
        if shift.total_hours > 0:
            shift.calculate_money()
        shift.total_tip = shift.cash_per_hour + shift.credit_per_hour
        # Calculate the cash and credit for each waiter:
        for i in range(len(names)):
            waiter.waiters[i].calculate_tip_each_waiter(shift)
        # send to db (database,"DB Browser (SQLite)"):
        day_tip = [Models.Money(total_hours=shift.total_hours, total_cash=shift.total_cash,
                                total_credit=shift.total_credit, cash_per_hour=shift.cash_per_hour,
                                credit_per_hour=shift.credit_per_hour, total_tip=shift.total_tip)]
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
                           total_hours=shift.total_hours,
                           total_cash=shift.total_cash,
                           total_credit=shift.total_credit,
                           cash_per_hour=shift.cash_per_hour,
                           credit_per_hour=shift.credit_per_hour,
                           total_tip=shift.total_tip,
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
