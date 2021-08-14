from datetime import datetime, time
from flask_login import UserMixin
from django.db.models.expressions import Col
from Program import db, login_manager
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, Float, Date, select


# @login_manager.user_loader()
# def load_user(user_id):
#     return Waiter.query.get(int(user_id))


# Waiter Model
class Waiter(UserMixin, db.Model):
    __table_name__ = 'waiter'
    id = Column('ID', Integer, primary_key=True)
    email = Column('Email', String(30), nullable=False)
    waiter_name = Column('Name', String(20), nullable=False)
    password = Column('Password', String(20), nullable=False)
    job_name = Column('Job_Name', String(20), nullable=True)
    age = Column('Age', Integer, nullable=True)
    location = Column('Location', String(20), nullable=True)
    phone = Column('Phone', String(20), nullable=True)

    def __init__(self, email, waiter_name, password, job_name, age, phone, location):
        self.email = email
        self.waiter_name = waiter_name
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
        return "{}".format(self.waiter_name)


# Money Model
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
        self.total_cash = total_cash
        self.total_credit = total_credit
        self.cash_per_hour = cash_per_hour
        self.credit_per_hour = credit_per_hour
        self.total_tip = total_tip

    def sum_total_hours(self, waiter):
        self.total_hours = self.total_hours + float(waiter.total_waiter_time)

    def get_total_hours(self):
        return self.total_hours

    def set_total_hours(self, hours):
        self.total_hours = self.total_hours + hours

    def set_total_cash_shift(self):
        if self.total_cash != '':
            self.total_cash = float(self.total_cash)
        else:
            self.total_cash = 0

    def set_total_credit_shift(self):
        if self.total_credit != '':
            self.total_credit = float(self.total_credit)
        else:
            self.total_credit = 0

    def set_total_tips(self):
        self.total_tip = round(self.cash_per_hour + self.credit_per_hour, 3)

    def calculate_cash_per_hour(self):
        self.cash_per_hour = round(float(self.total_cash) / self.total_hours, 1)

    def calculate_credit_per_hour(self):
        self.credit_per_hour = round(float(self.total_credit) / self.total_hours, 2)

    def init_cash_credit_money(self):
        self.set_total_cash_shift()
        self.set_total_credit_shift()

    def calculate_money(self):
        self.calculate_cash_per_hour()
        self.calculate_credit_per_hour()

    def __repr__(self):
        return 'date: {}, manager: {}, selected shift: {}, total hours: {},' \
               ' total cash: {}, total_credit: {}, cash_per_hour: {}, credit_per_hour: {},' \
               ' total_tip: {} '\
            .format(self.date,  self.manager, self.selected_shift, self.total_hours, self.total_cash, self.total_credit,
                    self.cash_per_hour, self.credit_per_hour, self.total_tip)


# Waiter Table Model
class WaitersTable(db.Model):
    __table_name__ = 'waiters_table'
    id_waiter = Column('id', Integer, primary_key=True, nullable=True)
    name = Column('Name', String, nullable=True)
    start_time_waiter = Column('Start-time', Time, nullable=True)
    finish_time_waiter = Column('Finish-time', Time, nullable=True)
    total_waiter_time = Column('Hours', Float, nullable=True)
    total_cash_waiter = Column('T-Cash-waiter', Float, nullable=True)
    total_credit_waiter = Column('T-Credit-waiter', Float, nullable=True)
    total_tip_waiter = Column('Total-money', Float, nullable=True)
    shift_id = Column('shift_id', Integer)
    time_zero = datetime.strptime("00:00:00", "%H:%M:%S").time()
    waiters = []
    waiters_name = []
    start_time_waiter_list = []
    finish_time_waiter_list = []
    total_waiter_time_list = []
    cash_waiter_list = []
    credit_waiter_list = []
    all_tips_waiters_list = []

    def __init__(self, id_waiter, name, start_time_waiter, finish_time_waiter, total_waiter_time, total_cash_waiter,
                 total_credit_waiter, total_tip_waiter, shift_id):
        self.id_waiter = id_waiter
        self.name = name
        self.start_time_waiter = start_time_waiter
        self.finish_time_waiter = finish_time_waiter
        self.total_waiter_time = total_waiter_time
        self.total_cash_waiter = total_cash_waiter
        self.total_credit_waiter = total_credit_waiter
        self.total_tip_waiter = total_tip_waiter
        self.shift_id = shift_id

    def get_name(self):
        return self.name

    def get_start_time_waiter(self):
        return self.start_time_waiter

    def get_finish_time_waiter(self):
        return self.finish_time_waiter

    def get_total_waiter_time(self):
        return self.total_waiter_time

    def get_total_cash_waiter(self):
        return self.total_cash_waiter

    def get_total_credit_waiter(self):
        return self.total_credit_waiter

    def get_total_tip_waiter(self):
        return self.total_tip_waiter

    def set_start_time_zero(self):
        if self.start_time_waiter == '':
            self.start_time_waiter = self.time_zero
        else:
            try:
                self.start_time_waiter = datetime.strptime(self.start_time_waiter, '%H:%M').time()

            except ValueError:
                self.start_time_waiter = datetime.strptime(self.start_time_waiter, '%H:%M:%S').time()

    def set_finish_time_zero(self):
        if self.finish_time_waiter == '':
            self.finish_time_waiter = self.time_zero
        else:
            try:
                self.finish_time_waiter = datetime.strptime(self.finish_time_waiter, '%H:%M').time()
            except ValueError:
                self.finish_time_waiter = datetime.strptime(self.finish_time_waiter, '%H:%M:%S').time()

    def set_total_time_waiter_zero(self):
        if self.total_waiter_time == '':
            self.total_waiter_time = 0

    def add_to_list_start_time(self):
        if self.start_time_waiter != '':
            self.start_time_waiter_list.append(self.start_time_waiter)

    def add_to_list_finish_time(self):
        if self.finish_time_waiter != '':
            self.finish_time_waiter_list.append(self.finish_time_waiter)

    def add_to_list_total_waiter(self):
        if self.total_waiter_time != '':
            self.total_waiter_time_list.append(self.total_waiter_time)

    def add_to_list_name(self):
        if self.name != '':
            self.waiters_name.append(self.name)

    def calculate_tip_each_waiter(self, shift):
        if self.total_waiter_time != 0:
            self.total_cash_waiter = round(float(self.total_waiter_time) * float(shift.cash_per_hour), 1)
            self.cash_waiter_list.append(self.total_cash_waiter)
            self.total_credit_waiter = round(float(self.total_waiter_time) * float(shift.credit_per_hour), 2)
            self.credit_waiter_list.append(self.total_credit_waiter)
            self.total_tip_waiter = round(float(self.total_cash_waiter) + float(self.total_credit_waiter), 2)
            self.all_tips_waiters_list.append(self.total_tip_waiter)
        else:
            self.cash_waiter_list.append('')
            self.credit_waiter_list.append('')
            self.all_tips_waiters_list.append('')

    def clear_all_lists(self):
        self.waiters_name = []
        self.start_time_waiter_list = []
        self.finish_time_waiter_list = []
        self.total_waiter_time_list = []
        self.cash_waiter_list = []
        self.credit_waiter_list = []
        self.all_tips_waiters_list = []

    def init_waiter(self, waiter, money):
        self.set_start_time_zero()
        self.set_finish_time_zero()
        self.set_total_time_waiter_zero()
        money.sum_total_hours(waiter)
        self.add_to_list_name()
        self.add_to_list_start_time()
        self.add_to_list_finish_time()
        self.add_to_list_total_waiter()
        self.waiters.append(waiter)

    # "To String":
    def __repr__(self):
        return 'waiters:id:{}, name: {}, start time: {}, end time: {}, total time: {},' \
               ' total cash waiter: {}, total credit waiter:{}, total tip:{}, shift ID: {}\n'\
            .format(self.id_waiter, self.name, self.start_time_waiter, self.finish_time_waiter,
                    self.total_waiter_time, self.total_cash_waiter, self.total_credit_waiter, self.total_tip_waiter,
                    self.shift_id)
