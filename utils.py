import datetime
import string


def validate_time(time):
    try:
        datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
        return True
    except ValueError as e:
        print('Please enter correct date format: YYYY-MM-DD HH:MM in 24h format')
        return False


def validate_car_id(id):
    # I don't know regex...
    # Validate this pattern 01E-00001

    if len(id) != 9:
        return False

    alphabet = string.ascii_letters
    second = id[2] in alphabet
    third = '-' in id
    try:
        first = type(int(id[0:2])) == int
        fourth = type(int(id.split('-')[1])) == int
    except ValueError as e:
        return False
    # Todo: validate frequent parking number
    return first and second and third and fourth


def validate_frequent_parking_num(number):
    pass
