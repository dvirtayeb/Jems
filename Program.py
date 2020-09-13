from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
from sqlalchemy.orm import sessionmaker
import os
import Config
from Forms import WaiterForm
from flask_migrate import Migrate
import Models
from Models import Money
from Models import WaitersTable
app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY') or '076f2ce915e884096c9ae907479b316e'
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\dataBase\\jems_db.db'.format(os.getcwd())  # db file
db = SQLAlchemy(app)  # Database
migrate = Migrate(app, db)
print(app.config['SQLALCHEMY_DATABASE_URI'])


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
    total_hours = 0
    Money.total_cash = 0
    Money.total_credit = 0
    Money.cash_per_hour = ''
    Money.credit_per_hour = ''
    Money.total_tip = ''
    WaitersTable.name = []
    WaitersTable.total_waiter_time = []
    WaitersTable.start_time_waiter = []
    WaitersTable.finish_time_waiter = []
    WaitersTable.cash = []
    WaitersTable.credit = []
    WaitersTable.all_tip = []
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
    total_hours = 0
    if request.method == 'POST':
        time_default = datetime(1, 1, 1).time()
        Money.total_cash = request.form.get('total_cash')
        if Money.total_cash != '':
            float(Money.total_cash)
        else:
            Money.total_cash = 0
        Money.total_credit = request.form.get('total_credit')
        if Money.total_credit != '':
            float(Money.total_credit)
        else:
            Money.total_credit = 0
        WaitersTable.name = request.form.getlist('name')
        for i in range(len(WaitersTable.name)):
            if WaitersTable.name[i] != '':
                WaitersTable.waiters_name.append(Models.WaitersTable.name[i])

        WaitersTable.start_time_waiter = request.form.getlist('start_time')
        WaitersTable.finish_time_waiter = request.form.getlist('finish_time')
        WaitersTable.total_waiter_time = request.form.getlist('total_time')

        for i in range(len(WaitersTable.name)):
            if WaitersTable.start_time_waiter[i] == '':
                WaitersTable.start_time_waiter[i] = time_default.strftime("%H:%M")
            if WaitersTable.finish_time_waiter[i] == '':
                WaitersTable.finish_time_waiter[i] = time_default.strftime("%H:%M")
            if WaitersTable.total_waiter_time[i] == '':
                WaitersTable.total_waiter_time[i] = 0
            else:
                total_hours = total_hours + float(WaitersTable.total_waiter_time[i])

        if total_hours > 0:
            Money.cash_per_hour = round(float(Money.total_cash) / total_hours, 1)
            Money.credit_per_hour = round(float(Money.total_credit) / total_hours, 2)
        Money.total_tip = Money.cash_per_hour + Money.credit_per_hour

        for i in range(len(WaitersTable.name)):
            if WaitersTable.total_waiter_time[i] != '':
                WaitersTable.total_cash_waiter = \
                    round(float(WaitersTable.total_waiter_time[i]) * float(Money.cash_per_hour), 1)
                WaitersTable.cash.append(WaitersTable.total_cash_waiter)
                WaitersTable.total_credit_waiter = \
                    round(float(WaitersTable.total_waiter_time[i]) * float(Money.credit_per_hour), 2)
                WaitersTable.credit.append(WaitersTable.total_credit_waiter)
                WaitersTable.total_tip_waiter = \
                    round(float(WaitersTable.total_cash_waiter) +
                          float(WaitersTable.total_credit_waiter), 2)
                WaitersTable.all_tip.append(WaitersTable.total_tip_waiter)
            else:
                WaitersTable.cash.append('')
                WaitersTable.credit.append('')
                WaitersTable.all_tip.append('')

        # send to db (database,"DB Browser (SQLite)"):
        day_tip = [Money(total_hours=total_hours, total_cash=Money.total_cash,
                         total_credit=Money.total_credit, cash_per_hour=Money.cash_per_hour
                         , credit_per_hour=Money.credit_per_hour, total_tip=Money.total_tip)]
        for money in day_tip:
            db.session.add(money)
        db.session.commit()
        for x in range(len(WaitersTable.waiters_name)):  # O(n^2)
            if WaitersTable.waiters_name != '':
                waiter = \
                    [WaitersTable(id_waiter=x, name=WaitersTable.name[x],
                                  start_time_waiter=datetime.strptime(WaitersTable.start_time_waiter[x]
                                                                        , "%H:%M").time(),
                                  finish_time_waiters=datetime.strptime(WaitersTable.finish_time_waiter[x]
                                                                            , "%H:%M").time(),
                                  total_waiter_time=WaitersTable.total_waiter_time[x],
                                  total_cash_waiter=WaitersTable.cash[x],
                                  total_credit_waiter=WaitersTable.credit[x],
                                  total_tip_waiter=WaitersTable.all_tip[x])
                     ]
                WaitersTable.waiters.append(waiter)
                print("the output is: ", waiter)
                for w in waiter:
                    db.session.add(w)
        db.session.commit()
    # send to html:
    return render_template('Jems-tips1.html',
                           total_hours=total_hours,
                           total_cash=Money.total_cash,
                           total_credit=Money.total_credit,
                           cash_per_hour=Money.cash_per_hour,
                           credit_per_hour=Money.credit_per_hour,
                           total_tip=Money.total_tip,

                           name=WaitersTable.name,
                           start_time=WaitersTable.start_time_waiter,
                           finish_time=WaitersTable.finish_time_waiter,
                           total_waiter_time=WaitersTable.total_waiter_time,
                           total_cash_waiter=WaitersTable.cash,
                           total_credit_waiter=WaitersTable.credit,
                           total_tips=WaitersTable.all_tip
                           )


# reset the app:
if __name__ == '__main__':
    app.run(debug=True)
