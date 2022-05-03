from datetime import datetime, time
from flask_login import UserMixin
from django.db.models.expressions import Col
from Program import db, login_manager
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, Float, Date, select

# @login_manager.user_loader()
# def load_user(user_id):
#     return Waiter.query.get(int(user_id))


# Waiter Model:
class Employee(UserMixin, db.Model):
    __table_name__ = 'employee'
    id = Column('ID', Integer, primary_key=True)
    email = Column('Email', String(30), nullable=False)
    employee_name = Column('Name', String(20), nullable=False)
    password = Column('Password', String(20), nullable=False)
    job_name = Column('Job_Name', String(20), nullable=True)
    age = Column('Age', Integer, nullable=True)
    location = Column('Location', String(20), nullable=True)
    phone = Column('Phone', String(20), nullable=True)

    def __init__(self, email, employee_name, password, job_name, age, phone, location):
        self.email = email
        self.employee_name = employee_name
        self.password = password
        self.job_name = job_name
        self.age = age
        self.phone = phone
        self.location = location

    # def is_authenticated(self):

    # def is_active(self):

    # def is_anonymous(self):

    # def get_id(self):

    def __repr__(self):
        return "{} {}".format(self.employee_name, self.age)

# page class:
class Page():
    def __init__(self, date, managers, selected_shift, total_cash, total_credit, total_hours,
                      cash_per_hour, credit_per_hour, total_tip,names, start_time, finish_time,
                     total_waiter_time, total_cash_waiter, total_credit_waiter, total_tip_waiter):
        self.date = date
        self.managers = managers
        self.selected_shift = selected_shift
        self.total_cash = total_cash
        self.total_credit = total_credit
        self.total_hours = total_hours
        self.cash_per_hour = cash_per_hour
        self.credit_per_hour = credit_per_hour
        self.total_tip = total_tip
        self.names = names
        self.start_time = start_time
        self.finish_time = finish_time
        self.total_waiter_time = total_waiter_time
        self.total_cash_waiter = total_cash_waiter
        self.total_credit_waiter = total_credit_waiter
        self.total_tip_waiter = total_tip_waiter


    def __repr__(self):
        return 'date: {}, manager: {}, selected_shift: {}, total_hours: {}, '\
        'total_cash: {}, total_credit: {}, cash_per_hour: {}, credit_per_hour: {}, total_tip: {}\n'\
        'names: {}\nstart_time: {}\nfinish_time: {}\ntotal_waiter_time: {},\n'\
        'total_cash_waiter: {}\ntotal_credit_waiter: {}\ntotal_tip_waiter: {}\n'\
            .format(self.date, self.managers, self.selected_shift, self.total_hours, self.total_cash, self.total_credit, self.cash_per_hour,
        self.credit_per_hour, self.total_tip, self.names, self.start_time, self.finish_time, self.total_waiter_time,
        self.total_cash_waiter, self.total_credit_waiter, self.total_tip_waiter)



# Money Model:
class Money(db.Model):
    __table_name__ = 'money'
    id = Column('id_money', Integer, primary_key=True)
    date = Column('date', Date, nullable=False)
    manager = Column('manager', String(20), nullable=True)
    selected_shift = Column('selected - shift', String(20))
    total_hours = Column('Total - Hours', Float, nullable=True)
    total_cash = Column('Total - Cash', Float, nullable=True)
    total_credit = Column('Total - Credit', Float, nullable=True)
    cash_per_hour = Column('Cash per hour', Float, nullable=True)
    credit_per_hour = Column('Credit per hour', Float, nullable=True)
    total_tip = Column('total tip', Float, nullable=True)

    def __init__(self, date, manager, selected_shift, total_hours, total_cash, total_credit, cash_per_hour,
                 credit_per_hour, total_tip):
        self.date = date
        self.manager = manager
        self.selected_shift = selected_shift
        self.total_hours = total_hours
        if self.total_hours is None or self. total_hours == "":
            self.total_hours = 0
        self.total_cash = total_cash
        self.set_total_cash_shift()
        self.total_credit = total_credit
        self.set_total_credit_shift()
        self.cash_per_hour = cash_per_hour
        self.credit_per_hour = credit_per_hour
        self.total_tip = total_tip

    def sum_total_hours(self, waiter):
        if waiter.total_waiter_time is None or waiter.total_waiter_time == "":
            waiter.total_waiter_time = 0
        self.total_hours = self.total_hours + float(waiter.total_waiter_time)

    def get_total_hours(self):
        return self.total_hours

    def set_total_hours(self, hours):
        if self.total_hours == hours:
            self.total_hours = 0
        else:
            self.total_hours = self.total_hours + hours

    def set_total_cash_shift(self):
        try:
            if self.total_cash != '' and self.total_cash is not None:
                if float(self.total_cash) >= 0:
                    self.total_cash = float(self.total_cash)
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            self.total_cash = -1

    def set_total_credit_shift(self):
        # print(self.total_credit)
        try:
            if self.total_credit != '' and self.total_credit is not None:
                if float(self.total_credit) >= 0:
                    self.total_credit = float(self.total_credit)
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            self.total_credit = -1

    def set_credit_per_hour(self):
        if self.credit_per_hour == "" or self.credit_per_hour is None:
            self.credit_per_hour = 0

    def set_cash_per_hour(self):
        if self.cash_per_hour == "" or self.cash_per_hour is None:
            self.cash_per_hour = 0

    def set_total_tips(self):
        if self.total_tip == "" or self.total_tip is None:
            self.total_tip = 0
        else:
            self.total_tip = round(self.cash_per_hour + self.credit_per_hour, 3)

    def calculate_cash_per_hour(self):
        if self.total_hours > 0:
            self.cash_per_hour = round(float(self.total_cash) / self.total_hours, 3)

    def calculate_credit_per_hour(self):
        if self.total_hours > 0:
            self.credit_per_hour = round(float(self.total_credit) / self.total_hours, 3)

    def init_cash_credit_money(self):
        self.set_total_hours(0)
        # self.set_total_cash_shift()
        # self.set_total_credit_shift()
        self.set_cash_per_hour()
        self.set_credit_per_hour()
        self.set_total_tips()

    def calculate_money(self):
        self.calculate_cash_per_hour()
        self.calculate_credit_per_hour()

    def __repr__(self):
        return 'date: {}, manager: {}, selected shift: {}, total hours: {},' \
               ' total cash: {}, total_credit: {}, cash_per_hour: {}, credit_per_hour: {},' \
               ' total_tip: {} '\
            .format(self.date, self.manager, self.selected_shift, self.total_hours, self.total_cash, self.total_credit,
                    self.cash_per_hour, self.credit_per_hour, self.total_tip)


# Waiter Table Model:
class WaitersTable(db.Model):
    __table_name__ = 'waiters_table'
    id_waiter = Column('id', Integer, primary_key=True, nullable=True)
    name = Column('Name', String, nullable=True)
    start_time = Column('Start-time', Time, nullable=True)
    finish_time = Column('Finish-time', Time, nullable=True)
    total_waiter_time = Column('Hours', Float, nullable=True)
    total_cash_waiter = Column('T-Cash-waiter', Float, nullable=True)
    total_credit_waiter = Column('T-Credit-waiter', Float, nullable=True)
    total_tip_waiter = Column('Total-money', Float, nullable=True)
    shift_id = Column('shift_id', Integer)
    time_zero = datetime.strptime("00:00:00", "%H:%M:%S").time()

    def __init__(self, id_waiter, name, start_time, finish_time, total_waiter_time, total_cash_waiter,
                 total_credit_waiter, total_tip_waiter, shift_id):
        self.id_waiter = id_waiter
        self.name = name
        self.start_time = start_time
        self.finish_time = finish_time
        self.total_waiter_time = total_waiter_time
        self.total_cash_waiter = total_cash_waiter
        self.total_credit_waiter = total_credit_waiter
        self.total_tip_waiter = total_tip_waiter
        self.shift_id = shift_id

    def get_name(self):
        return self.name

    def get_start_time_waiter(self):
        return self.start_time

    def get_finish_time_waiter(self):
        return self.finish_time

    def get_total_waiter_time(self):
        return self.total_waiter_time

    def get_total_cash_waiter(self):
        return self.total_cash_waiter

    def get_total_credit_waiter(self):
        return self.total_credit_waiter

    def get_total_tip_waiter(self):
        return self.total_tip_waiter

    def set_start_time_zero(self):
        if self.start_time == '' or self.start_time is None:
            self.start_time = self.time_zero
        else:
            try:
                self.start_time = datetime.strptime(self.start_time, '%H:%M').time()

            except ValueError:
                self.start_time = datetime.strptime(self.start_time, '%H:%M:%S').time()

    def set_finish_time_zero(self):
        if self.finish_time == '' or self.finish_time is None:
            self.finish_time = self.time_zero
        else:
            try:
                self.finish_time = datetime.strptime(self.finish_time, '%H:%M').time()
            except ValueError:
                self.finish_time = datetime.strptime(self.finish_time, '%H:%M:%S').time()

    def set_total_time_waiter(self, total_waiter_time):
        try:
            if float(total_waiter_time) >=0 :
                self.total_waiter_time = float(total_waiter_time)
            else:
                raise ValueError
        except ValueError:
            self.total_waiter_time = 0
        if self.total_waiter_time == '' or self.total_waiter_time is None:
            self.total_waiter_time = 0
        

    def set_total_cash_waiter(self):
        if self.total_cash_waiter == "" or self.total_cash_waiter is None:
            self.total_cash_waiter = 0

    def set_total_credit_waiter(self):
        if self.total_credit_waiter == "" or self.total_credit_waiter is None:
            self.total_credit_waiter = 0

    def set_total_tip_waiter(self):
        if self.total_tip_waiter == "" or self.total_tip_waiter is None:
            self.total_tip_waiter = 0

    def calculate_tip_each_waiter(self, shift, datalists):
        if self.total_waiter_time != 0 and self.total_waiter_time is not None:
            self.total_cash_waiter = round(float(self.total_waiter_time) * float(shift.cash_per_hour), 3)
            datalists["cash_waiter"].append(self.total_cash_waiter)
            self.total_credit_waiter = round(float(self.total_waiter_time) * float(shift.credit_per_hour), 3)
            datalists["credit_waiter"].append(self.total_credit_waiter)
            self.total_tip_waiter = round(float(self.total_cash_waiter) + float(self.total_credit_waiter), 3)
            datalists["all_tips_waiters"].append(self.total_tip_waiter)
        else:
            datalists["cash_waiter"].append("")
            datalists["credit_waiter"].append("")
            datalists["all_tips_waiters"].append("")

    def init_waiter(self, waiter_time, money):
        self.set_start_time_zero()
        self.set_finish_time_zero()
        self.set_total_time_waiter(waiter_time)
        self.set_total_cash_waiter()
        self.set_total_credit_waiter()
        self.set_total_tip_waiter()
        money.sum_total_hours(self)

    # "To String":
    def __repr__(self):
        return 'waiters:id:{}, name: {}, start time: {}, end time: {}, total time: {},' \
               ' total cash waiter: {}, total credit waiter:{}, total tip:{}, shift ID: {}\n'\
            .format(self.id_waiter, self.name, self.start_time, self.finish_time,
                    self.total_waiter_time, self.total_cash_waiter, self.total_credit_waiter, self.total_tip_waiter,
                    self.shift_id)
