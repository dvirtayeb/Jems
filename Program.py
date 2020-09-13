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
    Models.Money.total_cash = 0
    Models.Money.total_credit = 0
    Models.Money.cash_per_hour = ''
    Models.Money.credit_per_hour = ''
    Models.Money.total_tip = ''
    Models.WaitersTable.name = []
    Models.WaitersTable.total_waiter_time = []
    Models.WaitersTable.start_time_waiter = []
    Models.WaitersTable.finish_time_waiter = []
    Models.WaitersTable.cash = []
    Models.WaitersTable.credit = []
    Models.WaitersTable.all_tip = []
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
        time_zero = datetime(1, 1, 1).time()
        Models.Money.total_cash = request.form.get('total_cash')
        if Models.Money.total_cash != '':
            float(Models.Money.total_cash)
        else:
            Models.Money.total_cash = 0
        Models.Money.total_credit = request.form.get('total_credit')
        if Models.Money.total_credit != '':
            float(Models.Money.total_credit)
        else:
            Models.Money.total_credit = 0
        Models.WaitersTable.name = request.form.getlist('name')
        for i in range(len(Models.WaitersTable.name)):
            if Models.WaitersTable.name[i] != '':
                Models.WaitersTable.waiters_name.append(Models.WaitersTable.name[i])
        Models.WaitersTable.start_time_waiter = request.form.getlist('start_time')
        Models.WaitersTable.finish_time_waiter = request.form.getlist('finish_time')
        Models.WaitersTable.total_waiter_time = request.form.getlist('total_time')
        for i in range(len(Models.WaitersTable.name)):
            if Models.WaitersTable.start_time_waiter[i] == '':
                Models.WaitersTable.start_time_waiter[i] = time_zero.strftime("%H:%M")
            if Models.WaitersTable.finish_time_waiter[i] == '':
                Models.WaitersTable.finish_time_waiter[i] = time_zero.strftime("%H:%M")
            if Models.WaitersTable.total_waiter_time[i] == '':
                Models.WaitersTable.total_waiter_time[i] = 0
            else:
                total_hours = total_hours + float(Models.WaitersTable.total_waiter_time[i])
        if total_hours > 0:
            Models.Money.cash_per_hour = round(float(Models.Money.total_cash) / total_hours, 1)
            Models.Money.credit_per_hour = round(float(Models.Money.total_credit) / total_hours, 2)
        Models.Money.total_tip = Models.Money.cash_per_hour + Models.Money.credit_per_hour
        for i in range(len(Models.WaitersTable.name)):
            if Models.WaitersTable.total_waiter_time[i] != '':
                Models.WaitersTable.total_cash_waiter = \
                    round(float(Models.WaitersTable.total_waiter_time[i]) * float(Models.Money.cash_per_hour), 1)
                Models.WaitersTable.cash.append(Models.WaitersTable.total_cash_waiter)
                Models.WaitersTable.total_credit_waiter = \
                    round(float(Models.WaitersTable.total_waiter_time[i]) * float(Models.Money.credit_per_hour), 2)
                Models.WaitersTable.credit.append(Models.WaitersTable.total_credit_waiter)
                Models.WaitersTable.total_tip_waiter = \
                    round(float(Models.WaitersTable.total_cash_waiter) +
                          float(Models.WaitersTable.total_credit_waiter), 2)
                Models.WaitersTable.all_tip.append(Models.WaitersTable.total_tip_waiter)
            else:
                Models.WaitersTable.cash.append('')
                Models.WaitersTable.credit.append('')
                Models.WaitersTable.all_tip.append('')

        # send to db (database,"DB Browser (SQLite)"):
        day_tip = [Models.Money(total_hours=total_hours, total_cash=Models.Money.total_cash,
                                total_credit=Models.Money.total_credit, cash_per_hour=Models.Money.cash_per_hour
                                , credit_per_hour=Models.Money.credit_per_hour, total_tip=Models.Money.total_tip)]
        for money in day_tip:
            db.session.add(money)
        db.session.commit()
        for x in range(len(Models.WaitersTable.waiters_name)):  # O(n^2)
            if Models.WaitersTable.waiters_name != '':
                waiter = \
                    [Models.WaitersTable(id_waiter=x, name=Models.WaitersTable.name[x],
                                         start_time_waiter=datetime.strptime(Models.WaitersTable.start_time_waiter[x]
                                                                             , "%H:%M").time(),
                                         finish_time_waiters=datetime.strptime(Models.WaitersTable.finish_time_waiter[x]
                                                                               , "%H:%M").time(),
                                         total_waiter_time=Models.WaitersTable.total_waiter_time[x],
                                         total_cash_waiter=Models.WaitersTable.cash[x],
                                         total_credit_waiter=Models.WaitersTable.credit[x],
                                         total_tip_waiter=Models.WaitersTable.all_tip[x])
                     ]
                Models.WaitersTable.waiters.append(waiter)
                print("the output is: ", waiter)
                for w in waiter:
                    db.session.add(w)
                db.session.commit()
    # send to html:
    return render_template('Jems-tips1.html',
                           total_hours=total_hours,
                           total_cash=Models.Money.total_cash,
                           total_credit=Models.Money.total_credit,
                           cash_per_hour=Models.Money.cash_per_hour,
                           credit_per_hour=Models.Money.credit_per_hour,
                           total_tip=Models.Money.total_tip,
                           name=Models.WaitersTable.name,
                           start_time=Models.WaitersTable.start_time_waiter,
                           finish_time=Models.WaitersTable.finish_time_waiter,
                           total_waiter_time=Models.WaitersTable.total_waiter_time,
                           total_cash_waiter=Models.WaitersTable.cash,
                           total_credit_waiter=Models.WaitersTable.credit,
                           total_tips=Models.WaitersTable.all_tip
                           )


# reset the app:
if __name__ == '__main__':
    app.run(debug=True)
