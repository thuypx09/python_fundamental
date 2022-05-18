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


def is_equal_or_later_time(start, end):
    is_valid_length = len(end) == 5
    if not is_valid_length and ':' not in end:
        return False
    start_hour = int(start.split(':')[0])
    end_hour = int(end.split(':')[0])
    start_minute = int(start.split(':')[1])
    end_minute = int(end.split(':')[1])

    return start_hour < end_hour or (start_hour == end_hour and end_minute >= start_minute)


def validate_frequent_parking_num(number):
    pass
