from datetime import datetime
import os
from parking_history import ParkingHistory
import utils
from fee_calculator import FeeCalculator

want_to_use = True
while want_to_use:

    option = input('Enter one option: park/pickup/history/exit\n').lower()

    if option == 'exit':
        break
    if option not in ('park', 'pickup', 'history'):
        print('Option not available')
        continue

    car_id = input('Enter your car plate (e.g. 02C-12345):\n').upper()
    is_valid_car_id = utils.validate_car_id(car_id)
    while not is_valid_car_id:
        car_id = input('Invalid car plate. Please enter again:\n').upper()
        is_valid_car_id = utils.validate_car_id(car_id)

    # Original requirement: allow user to enter start time
    #   -> does not make sense, so I will get the current time as arrival
    if option == 'park':
        arrival = datetime.now().strftime('%Y-%m-%d %H:%M')
        history = ParkingHistory(history_line=arrival, car_id=car_id)

        file_exists = os.path.exists(f'parking_history/{car_id}.txt')
        if not file_exists:
            park_success = history.save_new_history()
        else:
            park_success = history.append_parking_history()
        if park_success:
            print('Thank you. Your parking has been saved. Now getting back to main screen...')

    if option == 'history':
        history = ParkingHistory(car_id=car_id)
        history.print_history()

    if option == 'pickup':
        history = ParkingHistory(car_id=car_id)
        if not history.check_is_parking():
            print('Your car is not parked here.')
            continue
        # Todo update
        start = history.get_last_arrival()
        end = ''
        date = datetime.now().strftime('%Y-%m-%d')

        # This code is to simulate when user pickup later (enter pickup time manually)
        while True:
            try:
                end = input('Please enter pickup time HH:MM (this is for pickup simulation):\n')
                end_int = int(end)
            except ValueError as e:
                continue
            last_parking_hour = int(history.get_last_arrival().split(':')[0])
            if end_int < last_parking_hour or end_int > 24:
                print(
                    f'Your parking time is: {history.get_last_arrival()}\nEnter value from {last_parking_hour} and 24')
                continue
            break

        # Assume that only single day parking is allowed
        calculator = FeeCalculator(start=start, end=end, weekday=date)
        parking_fee = calculator.get_fee()

        available_credit = history.get_available_credit()
        current_total = history.get_total_payment()
        min_payment = parking_fee - available_credit
        new_payment = 0
        if available_credit >= parking_fee:
            print(f'Parking fee is: {parking_fee}. You have ${available_credit} '
                  f'and will be deducted automatically.\nThank you! Getting back to main screen...')
            history.available_credit = available_credit - parking_fee
        if available_credit < parking_fee:
            print(f'Parking fee is ${parking_fee}')
            print(f'You have ${available_credit} of available credit. You need to pay at least: ${min_payment}')
            is_paying = True
            while is_paying:
                try:
                    new_payment = float(input('Please enter the amount you would like to pay:'))
                    if new_payment < min_payment:
                        raise ValueError
                    history.available_credit = new_payment - min_payment
                    print('Payment accepted.')
                    is_paying = False

                except Exception as e:
                    print('Value not allowed')

        history.total_payment = current_total + parking_fee

        end = datetime.now().strftime('%H:%M')
        history.history_line = f' - {end}'
        history.append_picking_history()
        history.update_available_credit()
        history.update_total_payment()
