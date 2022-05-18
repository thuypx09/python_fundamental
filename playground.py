from fee_calculator import FeeCalculator


calculator = FeeCalculator(start='09:12',end='10:13')

print(calculator.get_parked_hours())