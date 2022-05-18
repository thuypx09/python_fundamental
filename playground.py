from datetime import datetime

date = datetime(2022, 5, 18)

print(date.isoweekday())

from fee_calculator import FeeCalculator

fee = FeeCalculator(weekday='2022/5/12', start='00:01', end='23:59')
print(fee.get_fee())