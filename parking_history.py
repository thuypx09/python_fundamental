import os


class ParkingHistory:

    def __init__(self, **kw):
        self.car_id = kw.get('car_id')
        self.history_line = kw.get('history_line')
        self.total_payment = kw.get('total_payment')
        self.available_credit = kw.get('available_credit')

    def print_history(self):
        try:
            with open(f'parking_history/{self.car_id}.txt') as history:
                print(history.read())
        except FileNotFoundError as file_err:
            print(f'History not found. Car {self.car_id} never parked here.')

    def save_new_history(self):
        """ Save a completely new history """
        # Check file exist but car already parking
        is_parking = self.check_is_parking()
        if is_parking:
            print('Your car is parking, cannot park the same car. Getting back to main screen')
            return False

        with open(f'parking_history/{self.car_id}.txt', mode='w') as history:
            history.write(f'Total Payment: 0.00\n'
                          f'Available Credits: 0.00\n'
                          f'Parked Datas:\n'
                          f'{self.history_line}')

    def append_parking_history(self):
        """ Append a new parking without end time """
        is_parking = self.check_is_parking()
        if is_parking:
            print('Your car is parking, cannot park the same car. Getting back to main screen...')
            return False

        with open(f'parking_history/{self.car_id}.txt', mode='a') as history:
            history.write(f'\n{self.history_line}')

    def append_picking_history(self):
        """ Append a new parking without end time """
        with open(f'parking_history/{self.car_id}.txt', mode='a') as history:
            history.write(f'{self.history_line}')

    def update_available_credit(self):
        # Todo: check file existence
        contents = []
        # Todo: find a way to open and read file without overwriting original file
        with open(f'parking_history/{self.car_id}.txt', mode='r') as history:
            contents = history.readlines()

        contents[1] = f'Available Credits: {self.available_credit}\n'
        with open(f'parking_history/{self.car_id}.txt', mode='w') as history:
            history.writelines(contents)

    def get_available_credit(self):
        """ Get in the file """
        # Maybe we don't have to check this since file existence already checked somewhere else
        file_exists = os.path.exists(f'parking_history/{self.car_id}.txt')
        if not file_exists:
            return 0
        with open(f'parking_history/{self.car_id}.txt') as history:
            credit = history.readlines()[1].split(' ')[2]
            if credit == '0.00':
                return 0
            return float(credit)

    def update_total_payment(self):
        # Todo check file existence
        contents = []
        with open(f'parking_history/{self.car_id}.txt', mode='r') as history:
            contents = history.readlines()
        contents[0] = f'Total Payment: {self.total_payment}\n'
        with open(f'parking_history/{self.car_id}.txt', mode='w') as history:
            history.writelines(contents)

    def get_total_payment(self):
        """ Get in the file """
        # Don't need this check since already checked in main
        file_exists = os.path.exists(f'parking_history/{self.car_id}.txt')
        if not file_exists:
            return 0
        with open(f'parking_history/{self.car_id}.txt') as history:
            total_payment = history.readlines()[0].split(' ')[2]
            return float(total_payment)

    def get_last_arrival(self):
        """ Get arrival time of the last history line """
        with open(f'parking_history/{self.car_id}.txt') as history:
            contents = history.readlines()
            last_line = contents[-1]
            return last_line.split(' ')[1].strip()

    def check_is_parking(self):
        if not os.path.exists(f'parking_history/{self.car_id}.txt'):
            return False

        with open(f'parking_history/{self.car_id}.txt') as history:
            contents = history.readlines()
            last_line = contents[-1]
            LENGTH_OF_PARKING_DATA_LINE = 24
            return len(last_line.strip()) != LENGTH_OF_PARKING_DATA_LINE
