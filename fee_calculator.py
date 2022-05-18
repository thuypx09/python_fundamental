from datetime import datetime

# Todo: convert to dictionary
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
        weekday = datetime(year, month, day).isoweekday()
        pricing = (QUOTE.get(weekday))
        # Apply discount
        pricing[0][1] *= 0.9
        pricing[1][1] *= 0.9
        pricing[2][1] *= 0.5

        def get_hour(time):
            return int(time.split(':')[0])

        start = get_hour(self.start)
        end = get_hour(self.end)

        fee = 0
        first_period = start < 8
        second_period = 0
        third_period = 0

        if first_period:
            fee += pricing[0][1]
            start = 8

        if end < 17:
            second_period = end - start + 1
        if start >= 17:
            third_period = end - start + 1
        if start < 17 and end >= 17:  # Else
            second_period = 17 - start
            third_period = end - 17 + 1

        double_charge = max(second_period - pricing[1][0], 0)

        fee += double_charge * 2 * pricing[1][1] + (second_period - double_charge) * pricing[1][1]
        fee += third_period * pricing[2][1]  # single day parking -> no double charge for third period

        return round(fee, 2)

    def get_parked_hours(self):
        duration = str(datetime.strptime(self.end, '%H:%M') - datetime.strptime(self.start, '%H:%M'))
        if len(duration) == 7:
            duration = f'0{duration}'
        return duration[:5]
