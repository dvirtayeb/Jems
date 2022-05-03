class Registry:
    waiters = []

    def __init__(self, waiters):
        self.waiters = waiters

    def add_waiter(self, waiter):
        self.waiters.append(waiter)

    def remove_waiter(self, waiter):
        self.waiters.remove(waiter)
