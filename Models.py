from django.db.models.expressions import Col

import Program
from Program import db
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, Float


# model for db:
class BaseModel(db.Model):
    __abstract__ = True
    
    def save(self):
        if self not in db.session:
            db.session.add(self)
        db.session.commit()

    def update(self, data: dict):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Waiters(db.Model):
    __table_name__ = 'waiters'
    waiter_name = Column('Name', String(20), nullable=True, primary_key=True)
    job_name = Column('Job_Name', String(20), nullable=True)
    age = Column('Age', Integer, nullable=True)
    location = Column('Location', String(20), nullable=True)
    phone = Column('Phone', String(20), nullable=True)

    def __init__(self, waiter_name, job_name, age, phone, location):
        self.waiter_name = waiter_name
        self.job_name = job_name
        self.age = age
        self.phone = phone
        self.location = location


class Money(db.Model):
    __table_name__ = 'money'
    id = Column('id', Integer, primary_key=True)
    total_hours = Column('Total - Hours', Float, nullable=True)
    total_cash = Column('Total - Cash', Float, nullable=True)
    total_credit = Column('Total - Credit', Float, nullable=True)
    cash_per_hour = Column('Cash per hour', Float, nullable=True)
    credit_per_hour = Column('Credit per hour', Float, nullable=True)
    total_tip = Column('total tip', Float, nullable=True)

    def __init__(self, total_hours, total_cash, total_credit, cash_per_hour, credit_per_hour, total_tip):
        self.total_hours = total_hours
        self.total_cash = total_cash
        self.total_credit = total_credit
        self.cash_per_hour = cash_per_hour
        self.credit_per_hour = credit_per_hour
        self.total_tip = total_tip


class WaitersTable(db.Model):
    __table_name__ = 'waiters_table'
    id_waiter = Column('id', Integer, primary_key=True)
    name = Column('Name', String, nullable=True)
    start_time_waiter = Column('Start-time', Time or Float, nullable=True)
    finish_time_waiter = Column('Finish-time', Time or Float, nullable=True)
    total_waiter_time = Column('Hours', Float, nullable=True)
    total_cash_waiter = Column('T-Cash-waiter', Float, nullable=True)
    total_credit_waiter = Column('T-Credit-waiter', Float, nullable=True)
    total_tip_waiter = Column('Total-money', Float, nullable=True)
    waiters_name = []
    waiters = []
    cash = []
    credit = []
    all_tip = []

    def __init__(self, id_waiter, name, start_time_waiter, finish_time_waiters, total_waiter_time, total_cash_waiter,
                 total_credit_waiter, total_tip_waiter):
        self.id_waiter = id_waiter
        self.name = name
        self.start_time_waiter = start_time_waiter
        self.finish_time_waiters = finish_time_waiters
        self.total_waiter_time = total_waiter_time
        self.total_cash_waiter = total_cash_waiter
        self.total_credit_waiter = total_credit_waiter
        self.total_tip_waiter = total_tip_waiter

    # "to String":
    def __repr__(self):
        return '<waiters: name: {}, start time: {}, end time: {}, total time: {},' \
               ' total cash: {}, total credit:{}, total tip:{}'\
            .format(self.name, self.start_time_waiter, self.finish_time_waiters,
                    self.total_waiter_time, self.total_cash_waiter, self.total_credit_waiter, self.total_tip_waiter)
