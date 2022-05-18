from datetime import datetime

QUOTE = {
    7: [[None, 20], [8, 2], [24, 5]],
    1: [[None, 20], [2, 10], [24, 5]],
    2: [[None, 20], [2, 10], [24, 5]],
    3: [[None, 20], [2, 10], [24, 5]],
    4: [[None, 20], [2, 10], [24, 5]],
    5: [[None, 20], [2, 10], [24, 5]],
    6: [[None, 20], [4, 3], [24, 5]]
}


class FeeCalculator:

    def __init__(self, **kw):
        self.start = kw.get('start')
        self.end = kw.get('end')
        self.weekday = kw.get('weekday')

    def get_fee(self):
        year, month, day = map(int, self.weekday.split('-'))
        weekday = datetime(year, month, day).weekday()
        pricing = (QUOTE.get(weekday))
        # Apply discount
        # Todo: convert to dictionary
        pricing[0][1] *= 0.9
        pricing[1][1] *= 0.9
        pricing[2][1] *= 0.5


        def get_hour(time):
            return int(time.split(':')[0])

        start = get_hour(self.start)
        end = get_hour(self.end)

        fee = 0

        if start < 8:
            fee += pricing[0][1]
        if end >= 8:
            parked_hours = min(17 - 8, end - 8)
            normal_charge = max(pricing[1][0], pricing[1][0] - parked_hours)
            doubled_charge = parked_hours - normal_charge
            fee += normal_charge * pricing[1][1] + doubled_charge * pricing[1][1] * 2
        if end >= 17:
            # Assume that only single day parking is allowed -> no over-park for this time range
            parked_hours = min(24 - 17, end - 17)
            fee += parked_hours * pricing[2][1]

        return fee
