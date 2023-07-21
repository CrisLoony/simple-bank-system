from datetime import date
from random import choice


def calculateAge(birthDate: date):
    days_in_year = 365.2425
    age = int((date.today() - birthDate).days / days_in_year)
    return age


def generate_acc_number(chars: int):
    options = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    account_number = ''
    for n in range(chars):
        account_number += choice(options)
        if n == chars - 2:
            account_number += '-'
    return account_number


def calc_interest(rate, value):
    interest = (rate * value) / 100
    total_value = value + interest
    return total_value


if __name__ == '__main__':
    print(calculateAge(date(1998, 6, 24)))
    print(generate_acc_number(9))
