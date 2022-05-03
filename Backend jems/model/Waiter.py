from model.Employee import Employee


class Waiter(Employee):
    def __init__(self, job_name, name, age, phone, location):
        super().__init__(job_name)
        self.name = name
        self.age = age
        self.phone = phone
        self.location = location

    def __init__(self, job_name, name, start_time_waiter, finish_time_waiters, waiter_time, total_cash_waiter,
                 total_credit_waiter):
        super().__init__(job_name)
        self.name = name
        self.start_time_waiter = start_time_waiter
        self.finish_time_waiters = finish_time_waiters
        self.waiter_time = waiter_time
        self.total_cash_waiter = total_cash_waiter
        self.total_credit_waiter = total_credit_waiter
