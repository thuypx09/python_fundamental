from parking_history import ParkingHistory


class Car:

    def __init__(self, **kw):
        self.id = kw.get('id')
        self.history = kw.get('history')
        self.last_parking = kw.get('last_parking')